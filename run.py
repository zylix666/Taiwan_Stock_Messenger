# -*- coding: utf-8 -*-
#!/usr/bin/env python3.7

"""
Created on Wed Jul  1 18:16:13 2020

@author: Simon_INTC
"""

import sys

from stock_history_retriever import Stock_history_retriever
from Messenger_Line import Messenger_Line
from utils import query_stock_company_names

sys.path.append(".")

import logging
logging.basicConfig(level=logging.DEBUG,
    filename="TW_stock_log.txt", \
    format='[%(asctime)s %(levelname)-8s] %(message)s', \
	datefmt='%Y%m%d %H:%M:%S')



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    stock_number_list = ["0050","2002", "2330"]
    name_code = query_stock_company_names(stock_number_list)
    logger.debug("Stock number and company name mapping loaded!")

    show_fields = ["close", "change"]
    stock_to_show_dict = {}

    for stock_no in stock_number_list:
        logger.debug("Retrieve the stock - " + stock_no + " history.")
        shr_obj = Stock_history_retriever(stock_no, load_hist=True)
        # shr_obj.grab_two_years()
        logger.debug("Retrieve the stock - " + stock_no + " today's record.")
        show_list = shr_obj.grab_to_show(show_fields)
        logger.info("Grabbed today's stock trade record. Update showing data")
        stock_to_show_dict.update({stock_no: show_list})

    logger.info("Initial messenger.")
    messenger_obj = Messenger_Line(name_code, stock_to_show_dict)
    message = messenger_obj.compose_messge()
    token = "YOUR LINE NOTIFY TOKEN"
    logger.debug(message)
    messenger_obj.lineNotifyMessage(token, message)
    
