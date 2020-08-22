# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:47:44 2020

@author: Simon_INTC
"""

import requests
from bs4 import BeautifulSoup
import os
import csv

# Get the all public company names from TWSE
def getList():
    all_companies=[]
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    table = soup.find("table", {"class" : "h4"})
    for row in table.find_all("tr"):
        data = []
        for col in row.find_all('td'):
            col.attrs = {}
            data.append(col.text.strip().replace('\u3000', ' '))
        if len(data) == 1:
            pass
        else:
            all_companies.append(data[0])
    #remove title
    del all_companies[0]
    return all_companies

def build_stock_number_company_dictionary(intoFile = False):
    stock_no_name_list = getList()
    stock_no_name_dict = {} 
    for one_stock in stock_no_name_list:
        stock_number, company_name = one_stock.split(" ", 1) 
        print("%s, %s", (stock_number, company_name.strip()))
        stock_no_name_dict[stock_number] = company_name.strip()
    if intoFile:
        try:
            with open("stock_code_name.csv", 'w') as f:
                for key, value in stock_no_name_dict.items():
                    f.write("%s, %s\n"%(key, value))
        except IOError:
            print("I/O Error.")
    return stock_no_name_dict
    
def query_stock_company_name(stock_number):
    current_path = os.path.dirname(os.path.realpath(__file__))
    stock_no_name_dict = None
    company_name = None
    if os.path.isfile(current_path+"/stock_code_name.csv"):
        #read from csv file
        with open(current_path+"/stock_code_name.csv", mode='r') as infile:
            reader = csv.reader(infile)
            stock_no_name_dict = {rows[0]:rows[1] for rows in reader}
    else:
        stock_no_name_dict = build_stock_number_company_dictionary(True)
    try:
        company_name = stock_no_name_dict[stock_number].strip()
    except KeyError:
        company_name = "Unknown"
    return company_name
    
def query_stock_company_names(stock_numbers):
    name_code_mapping = {}
    for stock_number in stock_numbers:
        if stock_number not in name_code_mapping.keys():
            name_code_mapping[stock_number] = query_stock_company_name(stock_number)
    return name_code_mapping
        
if __name__=="__main__":
    #stock_dict = build_stock_number_company_dictionary(True)
    #print(stock_dict)
    #with open('all_stocks.csv', mode='r') as infile:
    #    reader = csv.reader(infile)
    #    mydict = {rows[0]:rows[1] for rows in reader}
    #print(mydict)
    #df.to_csv("all_stocks.csv", index=False)
    #create_code_name_map(df)
    stock_number_list = ["0050","2002", "2330"]
    name_code = query_stock_company_names(stock_number_list)
    print(name_code)