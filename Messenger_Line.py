# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 23:49:46 2020

@author: Simon_INTC
"""
import requests

class Messenger_Line():
    
    def __init__(self, name_code_mapping, stock_show_info_dict):
        self.name_code_mapping = name_code_mapping
        self.stock_show_info_dict = stock_show_info_dict
    
    def compose_messge(self):
        text_head = "今日收盤價: \n"
        text_body = ""
        for stock_no in self.stock_show_info_dict:
            #print(str(stock_no)+" " + \
            #    self.name_code_mapping[stock_no] + \
            #    " : " + str(self.close_price_dict[stock_no])+ "半年均價 : " + str(ma120_dict[stock_no])+ "\n")
            text_body = text_body + self.stock_show_info_dict[stock_no][0]+" " + \
                self.name_code_mapping[stock_no] + \
                " : " + self.stock_show_info_dict[stock_no][1]+ \
                    " 漲跌 : " + self.stock_show_info_dict[stock_no][2]+ \
                    " 半年均價 : " + self.stock_show_info_dict[stock_no][3] + "\n"
        return (text_head+text_body)
    
    def lineNotifyMessage(self, token, msg):
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
            }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code
    
if __name__=="__main__":
    close_prices = {"2002":20.7, "2892":22.3, "0050": 80.5}
    name_code = {"2002": "中鋼", "2892":"第一金", "0050":"台灣50"}
    messenger_obj = Messenger_Line(name_code, close_prices)
    message = "測試 : "+messenger_obj.compose_messge()
    token = "YOUR LINE NOTIFY TOKEN"
    print(message)
    messenger_obj.lineNotifyMessage(token, message)