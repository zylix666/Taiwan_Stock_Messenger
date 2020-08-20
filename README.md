# Taiwan_Stock_Messenger
 This is a program to crawl the stock trade information, format the data and post via instant message service.

## Intuitions
 * Grab the stock prices from website. (twse.com.tw as the example here.)
 * Processing : Compute the MA120( average price of the past 120 days)
 * Message : Format the information and compose message  posting to the group. (Based on Line Notify service here.)

## Block Diagram
![block diagram](https://github.com/zylix666/Taiwan_Stock_Messenger/blob/master/images/block_diagram.png "Block Diagram")

## How to run
You can run by command, 
> python run.py

or put in the crontab in the system.

## Utility
Retrieve the stock number and company name and save it for future use.
This is not the frequent running code.

## Screenshot
![Screen captured](https://github.com/zylix666/Taiwan_Stock_Messenger/blob/master/images/Screenshot.jpg "Screenshot")