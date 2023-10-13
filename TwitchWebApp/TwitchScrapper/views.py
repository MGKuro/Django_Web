from django.shortcuts import HttpResponse
import os
from dotenv import load_dotenv
import requests
from django.conf import settings
from google.oauth2 import service_account
import gspread
import json
import datetime

def Empty(request):
    return HttpResponse("Use /start to begin scrapping Twitch API")

################### START SCRAPPING ###########################

def Start_Scrapping(request):

    project_folder = os.path.expanduser('~/TwitchWebApp')
    load_dotenv(os.path.join(project_folder, '.env'))

    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
        scopes=settings.GOOGLE_SHEETS_SCOPES
    )
    gc = gspread.authorize(creds)

    ### Variables ###
    Toka_Client_ID = os.getenv("Toka_Client_ID")
    Toka_App_Secret = os.getenv("Toka_App_Secret")
    APP_TOKEN = os.getenv("APP_TOKEN")
    ACC_TOKEN = os.getenv("ACC_TOKEN")
    Refresh_Token = os.getenv("Refresh_Token")

    oauth_url = "https://id.twitch.tv/oauth2/token?client_id=%s&client_secret=%s&grant_type=client_credentials" % (Toka_Client_ID, Toka_App_Secret)
    refresh_url = "https://id.twitch.tv/oauth2/token?client_id=%s&client_secret=%s&grant_type=refresh_token&refresh_token=%s" % (Toka_Client_ID, Toka_App_Secret, Refresh_Token)

    ### Functions ####

    #Get new Token
    def Get_Token(URL, Token_Variable):
        res = requests.post(URL)
        res_json = res.json()
        access_token = res_json['access_token']
        str_combined = f"Bearer {access_token}"
        new_token = str_combined
        if Token_Variable == 'ACC_TOKEN':
            refresh = res_json['refresh_token']


        if Token_Variable == 'APP_TOKEN':
            with open(os.path.join(project_folder, '.env'), 'r') as env_file:
              lines = env_file.readlines()

            # Find and replace the existing key with the new value
            updated_lines = []
            for line in lines:
               if line.startswith(f'APP_TOKEN='):
                   updated_lines.append(f'APP_TOKEN={new_token}\n')
               else:
                   updated_lines.append(line)

            # Write the updated content back to the .env file
            with open(os.path.join(project_folder, '.env'), 'w') as env_file:
               env_file.writelines(updated_lines)

        elif Token_Variable == 'ACC_TOKEN':
            with open(os.path.join(project_folder, '.env'), 'r') as env_file:
              lines = env_file.readlines()

            # Find and replace the existing key with the new value
            updated_lines = []
            for line in lines:
               if line.startswith(f'ACC_TOKEN='):
                   updated_lines.append(f'ACC_TOKEN={new_token}\n')
               else:
                   updated_lines.append(line)

            updated_lines2 = []
            for line in lines:
               if line.startswith(f'Refresh_Token='):
                   updated_lines2.append(f'Refresh_Token={refresh}\n')
               else:
                   updated_lines2.append(line)

            with open(os.path.join(project_folder, '.env'), 'w') as env_file:
               env_file.writelines(updated_lines)


        return True

    def Write_Data(sheet,data):
        # Open the Google Sheet by its title
        sheet = gc.open(sheet).sheet1

        # Get the last row with data
        last_row = len(sheet.col_values(1)) + 1  # Assuming data is in column A

        # Write data to the sheet
        sheet.insert_rows(data, last_row)

    #Validate Token
    def Validate_App_Token(APPT):
        Authorized = False
        req = requests.get("https://id.twitch.tv/oauth2/validate", headers={"Authorization": APP_TOKEN})
        if req.status_code == 401:
            Get_Token(oauth_url, 'APP_TOKEN')
        elif req.status_code == 200:
            Authorized = True
        return Authorized

    def Validate_User_Token(ACCT):
        Authorized = False
        req = requests.get("https://id.twitch.tv/oauth2/validate", headers={"Authorization": ACCT})
        if req.status_code == 401:
            Get_Token(refresh_url, 'ACC_TOKEN')
        elif req.status_code == 200:
            Authorized = True
        return Authorized


    ########## Start Functions ##############################################
    if(Validate_App_Token(APP_TOKEN)):

        if(Validate_User_Token(ACC_TOKEN)):

            result = []

            #Get Top Games
            res = requests.get("https://api.twitch.tv/helix/games/top", headers={"Authorization": APP_TOKEN, "Client-Id": Toka_Client_ID})
            data = res.json()['data']
            today = datetime.date.today().strftime("%d/%m/%y")
            time = datetime.datetime.now() - datetime.timedelta(hours=3)
            time = time.time().strftime("%H:%M:%S")
            result = [list(item.values())+[today]+[time] for item in data]
            Write_Data("Get_Top_Games",result)

            result = []

            #Get Channel Information
            res = requests.get("https://api.twitch.tv/helix/channels?broadcaster_id=70107099", headers={"Authorization": ACC_TOKEN, "Client-Id": Toka_Client_ID})
            data = res.json()['data']
            today = datetime.date.today().strftime("%d/%m/%y")
            time = datetime.datetime.now() - datetime.timedelta(hours=3)
            time = time.time().strftime("%H:%M:%S")
            result = [[item["broadcaster_id"],item["broadcaster_login"],item["broadcaster_name"],item["broadcaster_language"],item["game_id"],item["game_name"],item["title"],item["delay"]]+[today]+[time] for item in data]
            Write_Data("Get_Channel_Information",result)

            result = []

            #Get Broadcaster Subrscriber
            res = requests.get("https://api.twitch.tv/helix/subscriptions?broadcaster_id=701070991", headers={"Authorization": ACC_TOKEN, "Client-Id": Toka_Client_ID})
            total = res.json()['total']
            data = res.json()['data']
            today = datetime.date.today().strftime("%d/%m/%y")
            time = datetime.datetime.now() - datetime.timedelta(hours=3)
            time = time.time().strftime("%H:%M:%S")
            result = [list(item.values())+[total]+[today]+[time] for item in data]
            Write_Data("Get_Broadcaster_Subscriptions",result)

            result = []

            #Get Channel Followers
            res = requests.get("https://api.twitch.tv/helix/channels/followers?broadcaster_id=701070991", headers={"Authorization": ACC_TOKEN, "Client-Id": Toka_Client_ID})
            total = res.json()['total']
            data = res.json()['data']
            today = datetime.date.today().strftime("%d/%m/%y")
            time = datetime.datetime.now() - datetime.timedelta(hours=3)
            time = time.time().strftime("%H:%M:%S")
            result = [list(item.values())+[total]+[today]+[time] for item in data]
            Write_Data("Get_Channel_Followers",result)

            result = []

            #Get Channel Chatters
            res = requests.get("https://api.twitch.tv/helix/chat/chatters?broadcaster_id=701070991&moderator_id=701070991", headers={"Authorization": ACC_TOKEN, "Client-Id": Toka_Client_ID})
            total = res.json()['total']
            data = res.json()['data']
            today = datetime.date.today().strftime("%d/%m/%y")
            time = datetime.datetime.now() - datetime.timedelta(hours=3)
            time = time.time().strftime("%H:%M:%S")
            result = [list(item.values())+[total]+[today]+[time] for item in data]
            Write_Data("Get_Chatters",result)

            result = []

            #Get Top Games ACC
            res = requests.get("https://api.twitch.tv/helix/games/top", headers={"Authorization": ACC_TOKEN, "Client-Id": Toka_Client_ID})
            data = res.json()['data']
            today = datetime.date.today().strftime("%d/%m/%y")
            time = datetime.datetime.now() - datetime.timedelta(hours=3)
            time = time.time().strftime("%H:%M:%S")
            result = [list(item.values())+[today]+[time] for item in data]
            Write_Data("Get_Top_Games_ACC",result)





            return HttpResponse("Executed.")
        else:
            return HttpResponse("User Token not valid. Updating...")


    else:
        return HttpResponse("App token no valid. Updating...")
