
from  kiteconnect import KiteConnect
import datetime , requests


def send_to_telegram(message):

    apiToken = '6058041177:AAHhrqXPDRa1vghxQu_dTyTXTar1JRgNjCo'
    chatID = '1083941928'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)
        
def is_function_used_today(FunctionName):
    today = datetime.date.today()
    
    with open("Logs/" + FunctionName + ".txt", "a+") as file:
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            
            if str(today) in line:
                
                return True
        
        # file.write(str(today) + "\n")
        return False

def CompareTime(TimeInput):

    current_time = datetime.datetime.now().time()
    given_time_str = TimeInput # Replace this with the desired time
    given_time = datetime.datetime.strptime(given_time_str, "%H:%M:%S").time()
    # print(current_time , given_time)
    
    if given_time <= current_time:
        return True 
    else :  return False
    
    
def ZerodhaApiLogin(Credentials):
    file = open("Access_Tokens/"+Credentials["user_id"] + '.txt', 'r')

    Credentials['access_token'] = file.read()
    api = KiteConnect(api_key=Credentials["api_key"])
    api.set_access_token(Credentials["access_token"])
    api.profile()
    return {"Cred" :Credentials , "API":api}
