# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 10:33:50 2020

@author: Simon_INTC
"""

import requests
import pandas as pd
from datetime import datetime, date
import time
from stock_history_repos import Stock_history_repos
from today_record import today_trade_record

class Stock_history_retriever():
    
    def __init__(self, stock_number, load_hist = True):
        self.stock_number = stock_number
        self.duration = 730
        self.base_url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY"
        self.months=["00","01","02","03","04","05","06","07","08","09","10","11","12"]
        self.days = ["00", "01","02","03","04","05","06","07","08","09","10","11","12", \
                    "13","14","15","16","17","18","19","20","21","22","23","24",\
                    "25","26","27","28","29","30","31"]
        self.years = ["2020", "2019"]
        if load_hist:
            self.stock_hist_repos = Stock_history_repos(self.stock_number)
    
    def __month_delta(self, sd, ed):
        flag = True
        if sd > ed:
            sd, ed = ed, sd
            flag = False
        
        year_diff = ed.year-sd.year
        end_month = year_diff * 12 + ed.month
        delta = end_month - sd.month
        return -delta if flag is False else delta
    
    def __transform_date(self, roc_date):
        y, m, d = roc_date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d  #民國轉西元
    
    def __transform_data(self, data):
        data[0] = datetime.strptime(self.__transform_date(data[0]), '%Y/%m/%d')
        data[1] = int(data[1].replace(',', ''))  #把千進位的逗點去除
        data[2] = int(data[2].replace(',', ''))
        data[3] = float(data[3].replace(',', ''))
        data[4] = float(data[4].replace(',', ''))
        data[5] = float(data[5].replace(',', ''))
        data[6] = float(data[6].replace(',', ''))
        data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
        data[8] = int(data[8].replace(',', ''))
        return data
    
    def __transform(self, data):
        return [self.__transform_data(d) for d in data] 

    def __get_stock_history(self, date):
        #Actually this acquires the price of this month.
        bottom_url = "?date=%s&stockNo=%s" % ( date, str(self.stock_number))
        full_url = self.base_url+bottom_url
        print(full_url)
        r = requests.get(full_url)
        data = r.json()
        return self.__transform(data['data'])  #進行資料格式轉換

    def get_stock_number(self):
        return self.stock_number
    
    def retrieve_data(self, start_yymm, end_yymm):
        # start_yymm, example : 201901
        # end_yymm, example : 202006
        start_date = date(int(start_yymm[0:4]), int(start_yymm[4:]), 1)
        end_date = date(int(end_yymm[0:4]), int(end_yymm[4:]), 1)
        month_diff = self.__month_delta(start_date, end_date)
        return month_diff
        
    def retrieve_month_price(self, date):
        s = pd.DataFrame(self.__get_stock_history(date))
        s.columns = ['date', 'shares', 'amount', 'open', 'high', 'low', 'close', 'change', 'turnover']
                #"日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數" 
        stock = []
        for i in range(len(s)):
            stock.append(self.stock_number)
        s['stockno'] = pd.Series(stock ,index=s.index)  #新增股票代碼欄，之後所有股票進入資料表才能知道是哪一張股票

        datelist = []
        for i in range(len(s)):
            datelist.append(s['date'][i])

        mlist = []
        for item in s['date']:
            mlist.append(item.month)
        s['month'] = mlist  #新增月份欄位
        return s

    # Preprocess method only
    def grab_two_years(self):
        print("Warning, this is pre-process methond only.")
        
        df_list = []
        
        #rest of years:
        for y in self.years[1:]:
            for m in self.months[1:]:
                df_list.append(self.retrieve_month_price(y+m+"01"))
                time.sleep(15)
                
        #year 2020
        for m in self.months[1:]:
            if int(m) <= datetime.today().month:
                one_month_deals = self.retrieve_month_price(self.years[0]+m+"01")
                #print(one_month_deals)
                df_list.append(one_month_deals)
            time.sleep(15)
  
        deal_history_total = pd.concat(df_list)
        deal_history_total.to_csv("Total_history_"+self.stock_number+".csv", index=False)
        return deal_history_total
    
    def grab_this_month(self):
        #what month is it now?
        this_month = datetime.today().month
        this_year = datetime.today().year
        this_day = datetime.today().day
        return self.retrieve_month_price(str(this_year)+self.months[this_month] \
                                         +self.days[this_day])

    def grab_today_record(self):
        today_record = self.grab_this_month().iloc[-1, :]
        # fix datetime error, remove time in the field.
        today_record[0] = datetime.strftime(today_record['date'],'%Y-%m-%d')
        last_record_in_repos = self.stock_hist_repos.get_last_record()
        if str(today_record['date']) != str(last_record_in_repos['date']) :
            # Update history records in CSV file first.
            self.stock_hist_repos.update_today(self.stock_number,today_record, write=True)
            today_T_record = today_trade_record(self.stock_number, today_record, \
                                              self.stock_hist_repos.get_120_avg_price())
        else:
            today_T_record = today_trade_record(self.stock_number, \
                                                self.stock_hist_repos.get_last_record(), \
                                                    self.stock_hist_repos.get_120_avg_price())
        return today_T_record
    
    def grab_to_show(self, show_fileds):
        # return dictionary with stock_no: [show_fields]
        show_list = []
        today_record = self.grab_today_record()
        show_list.append(str(self.stock_number))
        trade_info = today_record.get_trade_info(show_fileds)
        for ti in trade_info:
            show_list.append(ti)
        show_list.append(today_record.get_ma120())
        return show_list
    
if __name__ == '__main__':
    stock_history_obj = Stock_history_retriever("2412")
    print(stock_history_obj.grab_two_years())
    stock_history_obj.grab_this_month().
    print(stock_history_obj.grab_this_month()["close"])

