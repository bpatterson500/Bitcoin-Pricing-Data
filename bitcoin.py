#Author: Bill Patterson
# A simple script that makes a request to the Coindesk API 
# and displays the current time and price
# Might add matplotlib plot of pricing data

"""
Copyright <2018> <Bill Patterson>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import requests
import json
import matplotlib.pyplot
import matplotlib.dates
from datetime import date
from datetime import timedelta

# Function to get the current time and price of bitcoin
def current():
  url = "https://api.coindesk.com/v1/bpi/currentprice.json"
  request = requests.get(url)
  if (request.ok):
    jData = json.loads(request.content)
  #for key in jData:
    #print(str(key) + " : " + str(jData[key]) +'\n')
    print("Time: " + jData["time"]["updated"])
    print("Price: " + jData["bpi"]["USD"]["rate"] + " USD")
  else:
    request.raise_for_status()
  
# Function to get the price data for Bitcoin for the past 7 days and 
# plot the data using matplotlib
def historical():
  url = "https://api.coindesk.com/v1/bpi/historical/close.json?"
  today = date.today()
  start = today - timedelta(days = 6)
  url += "start=" + str(start) + "&end=" + str(today)
  #print(url)
  request = requests.get(url)
  if (request.ok):
    jData = json.loads(request.content)
    prices = jData["bpi"]
    date_list = []
    value_list = []
    for i in range(1,7):
      _date = today - timedelta(days = i)
      date_list.append(_date)
      value_list.append(prices[str(_date)])
      print(str(_date) + " : " + str(prices[str(_date)]))
    dates = matplotlib.dates.date2num(date_list)
    matplotlib.pyplot.plot_date(dates, value_list, '-o')
    matplotlib.pyplot.xlabel("Date")
    matplotlib.pyplot.ylabel("Price")
    matplotlib.pyplot.show()

# Main routine of the program
def main():
  choice = input("Would you like the current Bitcoin price or historical data?[curr/hist]: ")
  if (choice != "curr" and choice != "hist"):
    raise ValueError("Must enter either curr or hist")
  if (choice == "curr"):
    current()
  if (choice == "hist"):
    historical()

main()
