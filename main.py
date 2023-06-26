import time
import sys 
import os
import subprocess
import random
import requests
import input
import pymongo
import json
import schedule
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from discordwebhook import Discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

### Load Environment Variable from input.env file
load_dotenv()
DISCORD_BUY_WEBHOOK = os.getenv("DISCORD_BUY_WEBHOOK")
DISCORD_SYSTEM_WEBHOOK = os.getenv("DISCORD_SYSTEM_WEBHOOK")
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASWORD = os.getenv("MONGODB_PASWORD")

### Discord setup
discord = Discord(url=DISCORD_BUY_WEBHOOK)
discordSystem = Discord(url=DISCORD_SYSTEM_WEBHOOK)
discordSystem.post(content= "-----------------------------------------------")

#PIA Regions -- use `piactl get regions`
regions = ["us-salt-lake-city", "us-honolulu", "us-california", "us-west", "us-west-streaming-optimized", "us-silicon-valley", "us-seattle", "us-new-mexico", "us-wyoming", "us-mississippi", "us-montana", "us-north-dakota", "us-denver", "us-louisiana", "us-oklahoma", "us-south-dakota", "us-arkansas", "us-kansas", "us-missouri", "us-oregon", "us-north-carolina", "us-south-carolina", "us-kentucky", "us-tennessee", "us-west-virginia", "us-alabama", "us-atlanta", "us-virginia", "us-idaho", "us-nebraska", "us-indiana", "us-michigan", "us-chicago", "us-minnesota", "us-ohio", "us-iowa", "us-wisconsin", "us-florida", "us-washington-dc", "us-connecticut", "us-new-york", "us-rhode-island", "us-baltimore", "us-east", "us-east-streaming-optimized", "us-massachusetts", "us-new-hampshire", "us-pennsylvania", "us-vermont", "us-maine", "panama", "ca-vancouver", "ca-ontario", "ca-toronto", "ca-montreal"]

### Start PIA VPN
subprocess.run(["C:\Program Files\Private Internet Access\piactl.exe", "disconnect"])
subprocess.run(["C:\Program Files\Private Internet Access\piactl.exe", "set", "region", random.choice(regions)])
subprocess.run(["C:\Program Files\Private Internet Access\piactl.exe", "connect"])
currentRegion = subprocess.run(["C:\Program Files\Private Internet Access\piactl.exe", "get", "region"], capture_output=True, text=True).stdout.strip()

### Verify external IP is PIA VPN
myIP      = "172.250.195.187"
waitIPCount = 0
while (requests.get('https://www.wikipedia.org').headers['X-Client-IP']) == myIP:
    waitIPCount += 1
    print("wait count is {}".format(waitIPCount))
    time.sleep(6)
    if waitIPCount == 10:
        discordSystem.post(content= ":x: Timed out waiting for PIA IP.")
        discordSystem.post(content= ":rewind: Exiting App and reconnecting to PIA VPN.")
        quit()
discordSystem.post(content= ":white_check_mark: PIA VPN IP Check Passed")

### Verify MabiBase is accessible
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
currentRegion = subprocess.run(["C:\Program Files\Private Internet Access\piactl.exe", "get", "region"], capture_output=True, text=True).stdout.strip()
mabibaseResponse = requests.get("https://na.mabibase.com/items/search", headers=headers).status_code
# mabibaseResponseText = requests.get("https://na.mabibase.com/items/search", headers=headers).text

if mabibaseResponse == 200 or mabibaseResponse == 301:
    discordSystem.post(content= ":white_check_mark: MabiBase Accessibility Check Passed")
    discordSystem.post(content= ":information_source: HTTP Response is {}".format(mabibaseResponse))
else:
    if mabibaseResponse == 403:
        discordSystem.post(content= ":x: MabiBase Banned.")
    else:
        discordSystem.post(content= ":x: MabiBase is not accessible.")
        discordSystem.post(content= ":information_source: HTTP Response is {}".format(mabibaseResponse))
    discordSystem.post(content= ":information_source: PIA VPN Region is `{}`".format(currentRegion))
    discordSystem.post(content= ":rewind: Exiting App and reconnecting to PIA VPN.")
    quit()

### MongoDB Connection
def get_collection():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://{}:{}@mabi-ah.hdehgcc.mongodb.net/?retryWrites=true&w=majority".format(MONGODB_USER,MONGODB_PASWORD)
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = pymongo.MongoClient(CONNECTION_STRING)
 
   # Get the database
   database = client['mabi_ah_watch']

   # Get the collection
   return database['ah_items']

def get_all_items_in_collection(collection):
    return list(collection.find({},{"_id" : 0}))

### Schedule job to print to discord of what the AH Watcher is watching on top of the hour
def send_list_to_discord():
    itemList = get_all_items_in_collection(get_collection())
    discordSystem.post(content= "Currently Watching: ```{}```".format(json.dumps(itemList, indent=2)))
schedule.every().hour.at(":00").do(send_list_to_discord)


### Chrome Driver Setup
print("Initializing webdriver...")
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

### Create empty dictionary to keep track of item alert
itemAlertDict = {}

### Time to resend alert to discord bot in seconds -- this is based on mabibase 5 min refresh rate
timeAlert = 300

def main():
    discordSystem.post(content= ":white_check_mark: Application Started Successfully")
    try:
        while True:
            schedule.run_pending()
            #Grab new collection
            collection = get_collection()
            itemList = get_all_items_in_collection(collection)
            for item in itemList:
                ### Variablize Items
                name = item["name"]
                itemID = item["id"]
                priceAlert = int(item["price"])
                url = "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemId%2Ceq%2C%22"+ itemID + "%22&sort=ItemPrice%3AAscending&page=0"

                driver.get(url)
                time.sleep(10)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                firstRow = soup.find_all("tr" , class_='MuiTableRow-root')[1]
                # print(firstRow.text)

                #Check if item is listed on AH
                if firstRow.text != "No results found.":
                    price = firstRow.find_all("div")[1].text.replace("G","").split()
                    unitPrice = int(price[0].replace(",",""))
                    # totalPrice = int(price[1].replace(",",""))
                    print("name: " + name)
                    print("unit price is: "  +  str(f'{unitPrice:,}') )
                    # print("total price is: " +  str(f'{totalPrice:,}') )
                    print("alert price at: " +  str(f'{priceAlert:,}') )

                    if unitPrice <= priceAlert:
                        if itemID in itemAlertDict.keys():
                            timeDelta = datetime.now() - itemAlertDict.get(itemID)
                            print(name + " - " + str(timeAlert - timeDelta.total_seconds()) + "s until next alert")
                            if timeDelta.total_seconds() > timeAlert:
                                itemAlertDict.pop(itemID)
                        else:
                            itemAlertDict[itemID] = datetime.now()
                            discord.post(content= name + " at " + str(f'{unitPrice:,}') + " ( Alert Set at : " +  str(f'{priceAlert:,}') + " )")

                    print("---")
    except Exception as e:
        print(e)
        discordSystem.post(content= ":x: Application Errored - Shutting Down")
        quit()
    
if __name__ == "__main__":
    main()
