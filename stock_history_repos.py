# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 23:14:22 2020

@author: Simon_INTC
"""

import os
import pandas as pd

class Stock_history_repos():
    
    def __init__(self, stock_number):
        self.stock_number = stock_number
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.pre_file_name = self.dir_path + "/Total_history_"
        self.post_file_name = ".csv"
        self.stock_history = self.__load_files()
        
    def __load_files(self):
        full_name = self.pre_file_name \
                    + self.stock_number   \
                    + self.post_file_name
        if os.path.isfile(full_name):
            #read file
            print("file name "+full_name)
            df = pd.read_csv(full_name, header=0)
            return df
        else:
            print("Cannot find the stock history file : %s"%full_name)
            return
        print("history file loaded.")
        
    def get_last_record(self):
        return self.stock_history.iloc[-1, :]

    def get_120_avg_price(self):
        #The definition of MA120 including today.
        #Append today price
        #last_120_day_price_list=self.stock_history.iloc[-119:,:]['close'].append(pd.Series([today_price]))
        last_120_day_price_list=self.stock_history.iloc[-120:,:]['close']
        return (last_120_day_price_list.mean())
            
    def update_today(self, stock_no, today_info, write=False):
        # today_info is a Series type data
        updated_stock_history = self.stock_history.append(today_info, ignore_index=True)
        self.stock_history = updated_stock_history
        if write:
            updated_stock_history.to_csv(self.pre_file_name \
                              + stock_no   \
                              + self.post_file_name, index=False)
                
if __name__ == "__main__":
    stock_number_list = ["2892", "2884", "0050","2002"]
    stock_history_repo = Stock_history_repos(stock_number_list)
    stock_history_repo.get_120_avg_price()
                
            
    