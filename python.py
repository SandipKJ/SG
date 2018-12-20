#!/usr/bin/env python
import itertools
import pandas as pd
from pandas import ExcelWriter
import os
import sys
import xlrd
import subprocess
import json
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
app = Flask(__name__)


CORS(app)
chart_dict = {}
resp_dict = {}

@app.route('/chart',methods=['GET'])
def createChart():
    return json.dumps(chart_dict)

@app.route('/xls', methods=['GET'])
def test():
    fileNameSelected = request.args.get('fileName')
    filePath = "C:/Users/SPX_HOM_GEN/Downloads/" + fileNameSelected
    print(filePath)
    ling = pd.read_excel(filePath)
    df = ling.to_json()
    sf = ling.head(0).to_json()
    print(type(ling.columns.values))
    a = list(ling)
    return json.dumps(a)

@app.route('/find-duplicates-with-column', methods=['GET'])
def findDuplicates():
    fileNameSelected = request.args.get('fileName');
    filepath="C:/Users/SPX_HOM_GEN/Downloads/" + fileNameSelected;
    columns = request.args.get('columns')
    if(filepath.find('.xlsx') != -1):
        xls = xlrd.open_workbook(filepath,on_demand=True)
        df = pd.read_excel(filepath,index=False)
    elif(filepath.find('.csv') != -1):
        df = pd.read_csv(filepath,low_memory=False)
    else:
        return "File format is not as expected";

    data = df.shape[0]

    if(df.duplicated().any()):
        df_duplicates = df[df.duplicated(subset=columns.split(','),keep='first')]
        writer = ExcelWriter('C:/Users/SPX_HOM_GEN/Downloads/EXPORT_MAESTRO_REG_new.xlsx')
        df.to_excel(writer,'Original')
#        df['CITY'].replace(to_replace=['PARIS 9'], value='PARIS',inplace=True)
        df_duplicates.to_excel(writer,'NoDuplicates')

        df.drop_duplicates(subset=columns.split(','),inplace=True)
        df_duplicates.to_excel(writer,'OnlyDuplicates')
        writer.close()

    else :
        print("No duplicates found");

    new_data = pd.read_csv("C:/Users/SPX_HOM_GEN/Downloads/EXPORT_MAESTRO_REG_NoDuplicates.csv", low_memory=False)
    print("Unique rows: {0}".format(len(new_data)))

    nat = pd.read_csv("C:/Users/SPX_HOM_GEN/Downloads/EXPORT_MAESTRO_REG_Duplicates.csv", low_memory=False)
    print("Total duplicate rows: {0}".format(len(nat)))

    dupl = len(nat)/data * 100
    nodupl = (100-dupl)
    chart_dict["duplicates"] = "%.2f" %dupl
    chart_dict["no_duplicates"] = "%.2f" %nodupl
    resp_dict["Dup"] = len(nat)
    resp_dict["Unique"] = len(new_data)
    return json.dumps(resp_dict)
    # return "true"

@app.route('/init', methods=['GET'])
def sample_function1(*args):
#    print("Hi there!")
    words = sentence.split()
    counts = {}
    for word in words:
        if word not in counts:
            counts[word] = 0
        counts[word] += 1
    print(type(counts))
#    print(counts)
    return jsonify(counts)

if __name__ == '__main__':
#    port = 8000 #the custom port you want
    app.run(host='127.0.0.1',port='5002')
