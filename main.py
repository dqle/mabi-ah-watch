import time
import sys 
import os
from bs4 import BeautifulSoup
from datetime import datetime
from discordwebhook import Discord
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import input

### Discord setup
discord = Discord(url=input.discordURL())

### Edge Driver Setup
options = Options()
options.headless = True
options.add_argument("--log-level=3")
driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options= options)

### Create empty dictionary to keep track of item alert
itemAlertDict = {}

### Time to resend alert to discord bot in seconds -- this is based on mabibase 5 min refresh rate
timeAlert = 300

def restart():
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    os.execv(sys.executable, ['python'] + sys.argv)

def main():
    try:
        while True:
            for item in input.itemList():
                ### Variablize Items
                name = str(item[0])
                itemID = item[1]
                url = "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemId%2Ceq%2C%22"+ itemID + "%22&sort=ItemPrice%3AAscending&page=0"
                priceAlert = int(item[2])
                
                driver.get(url)
                time.sleep(6)
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
        driver.quit()
        restart()

            
    
if __name__ == "__main__":
    main()
