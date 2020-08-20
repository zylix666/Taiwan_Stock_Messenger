# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:47:44 2020

@author: Simon_INTC
"""


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
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
            pass # title 股票, 上市認購(售)權證, ...
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
        print("%s, %s", (stock_number, company_name))
        stock_no_name_dict[stock_number] = company_name
    if intoFile:
        try:
            with open("all_stocks.csv", 'w') as f:
                for key, value in stock_no_name_dict.items():
                    f.write("%s, %s\n"%(key, value))
        except IOError:
            print("I/O Error.")
    return stock_no_name_dict
    
if __name__=="__main__":
    stock_dict = build_stock_number_company_dictionary(True)
    print(stock_dict)
    with open('all_stocks.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
    print(mydict)
    #df.to_csv("all_stocks.csv", index=False)
    #create_code_name_map(df)
