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

Symbol = "MIDCPNIFTY23N209425CE"


ltpType = "NFO:"
StrikeDifference = 0

exchange = "NFO"
 
if "FINNIFTY" in Symbol:
            QtySlicer =40
            StrikeDifference = 50
            MaxQuantity = 1800

elif "BANKNIFTY" in Symbol:
            QtySlicer =15
            StrikeDifference = 100
            MaxQuantity = 900
        
elif "MIDCPNIFTY" in Symbol:
            QtySlicer =75
            StrikeDifference = 25
            MaxQuantity = 4200
            
elif "NIFTY" in Symbol:
        QtySlicer =50
        StrikeDifference = 50
        MaxQuantity = 1800
       
        
elif "SENSEX" in Symbol:  
        exchange = "BFO"
        QtySlicer =10
        StrikeDifference = 100
        MaxQuantity = 1000
        ltpType = "BFO:"

instrument_token = ZerodhaApis[0]['API'].ltp(ltpType+Symbol)[ltpType+Symbol]['instrument_token']
currentDate = "2023-11-17 09:15:00"
startDate = "2023-11-16 09:15:00"
while True:
    
    high =[]
    low =[]
    close =[]
    open =[]
    data = ZerodhaApis[0]['API'].historical_data( instrument_token, startDate, currentDate, "3minute", continuous=False, oi=False)
    # print(data)
    # print(data)
    for i in data:
        close.append(float(i['close']))
        high.append(float(i['high']))
        low.append(float(i['low']))
        open.append(float(i['open']))

    EMA = talib.EMA(np.array(high),33)
    # print(EMA)
    # print(EMA[-1])
    RSI = talib.RSI(np.array(close) , 14)
    DMI = talib.PLUS_DI(np.array(high) , np.array(low ) , np.array(close) ,14)
    # print(DMI[-1])
    # print(RSI[-1])
    if (EMA[-1] < close[-1] and close[-1]>open[-1] and RSI[-1] > 49 and DMI[-1]> 19):
        print("yes")
        print(currentDate)
        while True:
            
            price = ZerodhaApis[0]['API'].ltp(ltpType+Symbol)[ltpType+Symbol]['last_price']
            print(price)
            if price > close[-1] +1.5:
                print("Trade")
                break
            time.sleep(0.5)
        
    else :
        print("NO")

# Given date and time
        given_date_time = datetime.datetime.strptime(currentDate, "%Y-%m-%d %H:%M:%S")

        # Increase by 1 second
        new_date_time = given_date_time + datetime.timedelta(seconds=1)

        currentDate = (new_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        print(currentDate)

        time.sleep(0.1)

qty = 100
StopLoss = 5
api = ZerodhaApis[0]['API']
StopLossOrders =[]
while (qty >MaxQuantity):

                    api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_BUY,
                                            quantity=MaxQuantity,
                                            order_type=api.ORDER_TYPE_MARKET,
                                            
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                    qty = qty- MaxQuantity
                
if qty > 0:
                            
                        api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_BUY,
                                            quantity=qty,
                                            order_type=api.ORDER_TYPE_MARKET,
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                        print("Order Placed")

qty = 100
while (qty > MaxQuantity):

                    order=  api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=MaxQuantity,
                                            order_type=api.ORDER_TYPE_SL,
                                            trigger_price=price -StopLoss,
                                            price= price -StopLoss - Variables['TriggerDifference'], 
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                    qty = qty- MaxQuantity
                    StopLossOrders.append(order)
                
if qty > 0:
                            
                        order=    api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=qty,
                                            order_type=api.ORDER_TYPE_SL,
                                            trigger_price=price -StopLoss,
                                            price= price -StopLoss - Variables['TriggerDifference'],
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                        print("Order Placed")
                        StopLossOrders.append(order)
 
while True:
    time.sleep(0.3)
    if api.ltp(ltpType+Symbol).get(ltpType+Symbol).get('last_price') > price + Variables['FirstTargetMultiplier']:
        for order in StopLossOrders :
                api.modify_order(
                    order_id= order , variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=qty,
                                            order_type=api.ORDER_TYPE_SL,
                                            trigger_price=price ,
                                            price= price  - Variables['TriggerDifference'],
                                            validity=api.VALIDITY_DAY)
        price = price + Variables['TrainingStopLoss']
        
    
   

    
    
