# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 23:44:28 2020

@author: Simon_INTC
"""

class today_trade_record():
    
    def __init__(self, stock_number, trade_record, ma_120 = 0.0):
        self.stock_number = stock_number
        #type Series
        self.today_trade_record = trade_record
        self.ma120 = float(f"{ma_120:.2f}")
        
    def get_trade_info(self, fields):
        ret_fields = []
        for f in fields:
            ret_fields.append(str(self.today_trade_record[f]))
        return ret_fields
    
    def get_stock_number(self):
        self.stock_number
    
    def set_company_name(self, company_name):
        self.company_name = company_name
        
    def get_company_name(self):
        return self.company_name
        
    def set_ma120(self, ma_120):
        formatted_MA120 = float(f"{ma_120:.2f}")
        self.ma120 = formatted_MA120
        
    def get_ma120(self):
        return str(self.ma120)