"""
A stock analysis-code, utilizing pandas and matplotlib. Values in R$, reminder that this code is not for real investing usage and does not represent
the reality of the stock market. I'm not responsible for losses in case of usage.
Program requires the download of the database located in https://www.kaggle.com/felsal/ibovespa-stocks.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import math
#Defining a path so the user is free to decide where to stock his database within their computer.
path = input("Enter the path for your directory (.csv file) ")
retval = os.getcwd()
os.chdir(path)
os.listdir(path)
os.getcwd()
print(f'The current working directory is {retval}')
#Pandas library dataframes
df = pd.read_csv('b3_stocks_1994_2020.csv')
df_2 = pd.read_csv('selic.csv')
df_3 = pd.read_csv('usd2brl.csv')
#Empty lists used for list comprehension and therefore further functions along the code.
#All lists are used more than once in the code, which adds for the importance of the correct utilization.
index = []
stocks = []
prices = []
years = []
graphs = []
vols = []
profts = []
qnts = []
count = 1
#Defines the slice of the string related to a unique stock and it's code (ABEV3,PETR4,FBOK34...)
def slice_stock():
    global x
    global stock
    stock = input('Insert the name of the stock you want: ')
    x = df[(df['ticker'] == stock)]
    if not x.empty:
        print(x)
        stocks.append(stock)
        slice_year()
    else:
        print("Error, this stock doesn't exist in DataBase, try again.")
        slice_stock()
#Works with slice_stock to slice data inside the database.
def slice_year():
    global y, df_4, selic_year, amount
    year = input('Insert the year you want start to work: ')
    y = x.loc[x.datetime.str.contains(year, regex=True)].head(365)
    selic_year = df_2.loc[df_2.datetime.str.contains(year, regex=True)].head(365)
    for n in range(1, (len(y['datetime']) + 1)):
        i = n
        index.append(i)
    y['index'] = index
    y.set_index('index', inplace=True)
    df_4 = pd.DataFrame(y)
    prices.append(y['open'][1])
    years.append(y['open'][1])
    if not y.empty:
        print(y)
        amount = int(input('Insert the value you have for this stock: '))
        if amount >= y['open'][1]:
            volatility()
        elif amount < y['open'][1]:
            print("Error, you don't have enough money, try again. ")
            del (index[0:len(index)])
            slice_year()
    else:
        print("Error, this year doesn't exist, try again.")
        del(index[0:len(index)])
        slice_year()
    df_4.set_index('datetime', inplace=True)
    graphs.append(df_4)
#Volatility() defines the volatility of the stocks chosen, will be plotted by the function graph() in a
#Timespan of a fiscal year counting from the starting year in slice_year()
def volatility():
    global var, average
    var = []
    for i in index:
        if i == len(index):
            break
        else:
            daily = (y['open'][i + 1] - y['open'][i]) / y['open'][i]
            var.append(daily)
        average = sum(var) / len(var)
    sd = []
    for i in var:
        sd.append((average - i) ** 2)

    vol = (sum(sd) / len(sd)) * math.sqrt(252)
    print(f'The volatility of the selected stock is = {round(vol * 100, 4)}%')
    vols.append(round(vol * 100, 4))

dict = {'Stocks': stocks, 'Prices': prices, 'Years': years}
#Graph() defines the plotting of the graphs shown in the program by using matplotlib.pyplot.
def graph():
    for n in range(0, count - 1):
        graphs[n][['high', 'low']].plot(figsize=(16, 9), title=dict['Stocks'][n] + ' - Volatility = ' + str(vols[n]) + '%', grid=True)
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')

        plt.show()
        plt.close()
#The following two functions define the profit calculation and further data about the stocks and amount chosen.
def profit():
    global qnt, v, prof
    qnt = amount // y['open'][1]
    v = y['close'][len(y['close'])] - y['open'][1]
    profts.append(v)
    qnts.append(qnt)

def p_profit():
    total_profit = []
    for n in range(0, len(qnts)):
        prof = amount + profts[n] * (qnts[n])
        print(f'You can buy {qnts[n]} {stocks[n]} stocks.\nIf you buy {qnts[n]} stocks you will have R${prof}. ')
        total_profit.append(prof)
    print(f'Your final amount is R${sum(total_profit)}. ')


print('Hi, this is your Stock Simulator and here is our DataBase: ')
print(df)
#Beginning of the "practical" part of the code. Henceforth, all functions will be run. 
choose = input('Do you want to proceed?(y/n) ').upper()
if choose == 'Y':
    slice_stock()
elif choose == 'N':
    print('Bye!')
    quit()
else:
    print('Error')
    quit()
#The loop while follows the statement that no more than 4 bluechip stocks can be bought, in order to be more practical
#the code is restricted to 4 different stocks at one stance of the code.
while count <= 4:
    if count < 4:
        count = count + 1
        del (index[0:10000])
        choose = input('Do you want to buy another stock?(y/n) ').upper()
        if choose == 'Y':
            profit()
            slice_stock()
        elif choose == 'N':
            print('Ok, we are going to stop here. ')
            print('That is the analysis of your stocks. ')
            profit()
            p_profit()
            graph()
            quit()
    elif count == 4:
        amount = int(input('Insert the value you have: '))
        if sum(prices) > amount:
            print("You don't have enough money, try again changing your amount or your stocks. ")
            quit()
        elif sum(prices) < amount:
            print('That is the analysis of your stocks. ')
            graph()
        else:
            print("You can't buy more stocks. ")
        break
    else:
        pass