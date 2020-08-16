# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:47:44 2020

@author: Simon_INTC
"""


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
            data.append(col.text.strip().replace('\u3000', ''))
        
        if len(data) == 1:
            pass # title 股票, 上市認購(售)權證, ...
        else:
            all_companies.append(data)
    return all_companies

def build_public_company_list():
    all_companies = getList()
    all_companies_df = pd.DataFrame(columns=all_companies[0])

    for one_stock in all_companies[1:]:
        to_append = pd.Series(one_stock, index=all_companies_df.columns)
        all_companies_df = all_companies_df.append(to_append, ignore_index=True)
    return all_companies_df

def create_code_name_map(all_companies_df):
    stock_code_name_dict = {}
    code_and_name = all_companies_df.iloc[:,0]
    for can in code_and_name:
        idx = 0
        for c in can:
            if c.isdigit() or c.isalpha():
                idx+=1
            else:
                break
        print(idx)
        #update dictionary
        
    
if __name__=="__main__":
    df = build_public_company_list()
    df.to_csv("all_stocks.csv", index=False)
    create_code_name_map(df)