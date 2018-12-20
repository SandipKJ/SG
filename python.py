#!/usr/bin/env python

import itertools
import pandas as pd
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

@app.route('/xls', methods=['GET'])
def test():
    fileNameSelected = request.args.get('fileName');
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
    list = request.args.get('columns').split(',')
    if(filepath.find('.xlsx') != -1):
        xls = xlrd.open_workbook(filepath,on_demand=True)
        #print (xls.sheet_names())
        pd.read_excel(filepath,xls.sheet_names()[0]).to_csv("C:/Users/SPX_HOM_GEN/Downloads/duplicates.csv",index=False)
        df = pd.read_csv("C:/Users/SPX_HOM_GEN/Downloads/duplicates.csv",low_memory=False)
    elif(filepath.find('.csv') != -1):
        df = pd.read_csv(filepath,low_memory=False)
    else:
        return "File format is not as expected";
    if(df.duplicated().any()):
        df_duplicates = df[df.duplicated(subset=list,keep=False)]
        df_duplicates.to_csv('C:/Users/SPX_HOM_GEN/Downloads/EXPORT_MAESTRO_REG_Duplicates.csv')
        df.drop_duplicates(subset=list,inplace=True)
        df.to_csv('C:/Users/SPX_HOM_GEN/Downloads/EXPORT_MAESTRO_REG_NoDuplicates.csv')
        # return "true";
    else :
        print("No duplicates found");
    
    return "true"

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
