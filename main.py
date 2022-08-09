import time
import sys 
import os
from bs4 import BeautifulSoup
from discordwebhook import Discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import input

### Discord setup
discord = Discord(url=input.discordURL())

### Chrome Driver Setup
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

def restart():
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    os.execv(sys.executable, ['python'] + sys.argv)

def main():
    try:
        while True:
            for item in input.itemList():
                # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
                ### Variablize Items
                name = str(item[0])
                url = "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemId%2Ceq%2C%22"+ item[1] + "%22&sort=ItemPrice%3AAscending&page=0"
                priceAlert = int(item[2])
                
                driver.get(url)
                time.sleep(5)
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
                    print("")

                    if unitPrice <= priceAlert:
                        discord.post(content="BUY " + name + " at " + str(f'{unitPrice:,}') + " ( Alert Set at : " +  str(f'{priceAlert:,}') + " )")

                # driver.quit()
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        driver.quit()
        restart()
            
    
if __name__ == "__main__":
    main()
