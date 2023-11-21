from Login_Zerodha import login_in_zerodha
from kiteconnect import KiteConnect
import json , os , time , requests,datetime , threading , sys
import  ExtraFunctions
import Cred
import pandas as pd
import numpy as np
import talib
ZerodhaApis = []

ZerodhaAccounts = []

global TradeFunctionStart



def addZerodhaAccount(Credentials):
    ZerodhaAccounts.append(Credentials)

addZerodhaAccount(Cred.Crosshair)


for ZerodhaAccount in ZerodhaAccounts :
    LoginArray = []
    try :
        ExtraFunctions.ZerodhaApiLogin(ZerodhaAccount)
    except Exception as e:
        LoginArray.append(ZerodhaAccount)
        
    Threads = []
    
    for ZerodhaAccount in LoginArray:
        T = threading.Thread(target=login_in_zerodha , args= [ZerodhaAccount])
        T.start()
        Threads.append(T)
    for Thread in Threads :
     Thread.join()

    ZerodhaApis.append(ExtraFunctions.ZerodhaApiLogin(ZerodhaAccount))




# # Example usage
high =[]
low =[]
close =[]
open =[]
data = ZerodhaApis[0]['API'].historical_data( 12470786, "2023-11-15 09:15:00", "2023-11-17 12:33:00", "3minute", continuous=False, oi=False)
# print(data)
print(data)
for i in data:
    close.append(float(i['close']))
    high.append(float(i['high']))
    low.append(float(i['low']))
    open.append(float(i['open']))

EMA = talib.EMA(np.array(high),33)
print(EMA)
print(EMA[-1])
RSI = talib.RSI(np.array(close) , 14)
DMI = talib.PLUS_DI(np.array(high) , np.array(low ) , np.array(close) ,14)
print(DMI[-1])
print(RSI[-1])

if (EMA[-1] < close[-1] and close[-1]>open[-1] and RSI[-1] > 49 and DMI[-1]> 19):
    print("yes")
else :print("NO")

# 1. Candle must close above 33 ema high [candle body not wick]. done
# 2. Strike Price Must Be Between 45 - 85.
# 3. It Will Buy Above 1.50 Points above the closing price of breakout candle on 33 ema.
# 4. After entering trade if price gone 3 points up then sl will be move to cost.
# 5. Sl will be of 5 points.
# 6. Target Will Be Unlimited if 5 points achieved then sl will be move to target 1, then if target 2
# achieved sl will be moved to 2nd target.
# 7. Only Fresh Breakout of trade above 33 ema will be considered as tradeable.
# 8. Trade should execute only when breakout candle is closed not in between. done
# 9. Time Frame = 3 Min done
# 10. Trade Must be valid till 2nd candle after breakout candle means next 2 candle after breakout
# candle after that trade will be failed.
# 11. The Breakout candle must be green it should not be red , if red then do not enter the trade. done
# 12. Rsi must be above 49 before trade executed.
# 13. +Di must be above 19 before trade executed. done
# 14. Timing 9:15 Am To 3:00 Pm.