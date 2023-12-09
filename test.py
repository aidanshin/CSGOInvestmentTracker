from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import os 
import asyncio


class Item:
    def __init__(self, name = None, listing_supply = 0, listing_price = 0, demand_supply=0, demand_price=0):
        self.name = name
        self.listing_supply = listing_supply
        self.listing_price = listing_price
        self.demand_supply = demand_supply
        self.demand_price = demand_price
    
    def displayContent(self):
        return f"Name: {self.name}, Listing Price: ${self.listing_price}, Demand Price: ${self.demand_price}, Listing Quantity: {self.listing_supply}, Demand Quantity: {self.demand_supply}"


async def scrape_data(urls):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    driver = webdriver.Chrome(options=options)
    items = {}
    # i = 0
    
    
    for url in urls:
        driver.get(url)

        await asyncio.sleep(5)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'lxml')

        item = Item()

        data_failure = False

        try:
            item.name = soup.find('h1', class_="hover_item_name").text.strip().replace("|", "")
        except Exception:
            print("Item Name Not Found.")
            data_failure = True
            urls.append(url)
            await asyncio.sleep(120)
        
        try: 
            item_order_summary = soup.find_all('div', class_="market_commodity_order_summary")

            if item_order_summary[0].text == "There are no active listings for this item.":
                item.listing_price = 0
                item.listing_supply = 0
            else:
                for_sale_content = item_order_summary[0].text.split()
                item.listing_price = for_sale_content[5].split("$")[1]
                item.listing_supply = for_sale_content[0]

            if item_order_summary[1].text == "There are no active buy orders for this item.":
                item.demand_price = 0
                item.demand_supply = 0
            else:
                buy_order_content = item_order_summary[1].text.split()
                item.demand_price = buy_order_content[5].split("$")[1]
                item.demand_supply = buy_order_content[0]

        except Exception:
            print("Failed to get For Sale Content.")
            data_failure = True
            urls.append(url)
            await asyncio.sleep(120)
        

        if not data_failure:
            print(item.displayContent())
            items[item.name] = item

            if os.path.exists(f"items/{item.name}.txt"):
                    item_file = open(f"items/{item.name}.txt", "a", encoding="utf-8") 
                    item_file.write(f"{item.listing_price} {item.demand_price} {item.listing_supply} {item.demand_supply} {int(time.time())}\n")
                    item_file.close()
            else:
                item_file = open(f"items/{item.name}.txt", "w", encoding="utf-8")
                item_file.write("LP DP LQ DQ T\n")
                item_file.write(f"{item.listing_price} {item.demand_price} {item.listing_supply} {item.demand_supply} {int(time.time())}\n")
                item_file.close()
        
        # urls.pop(urls.index(url))
        # print(urls)
        # print(len(urls))
        await asyncio.sleep(random.randint(5,10))
        # i += 1
        # if i == 1:
        #     i = 0
        #     break
    driver.quit()
    return items

async def calculate_investments(items):
    initial_investment_total = 0
    current_total = 0
    individual_profits = []
    # i = 0
    for line in open("myitems.txt","r").readlines()[1:]:
        try:
            item_name, quantity, cost = line.strip().split(",")
            item = items.get(item_name)
            initial_investment = float(quantity) * float(cost)
            current_price = float(quantity) * float(item.listing_price)
            individual_profits.append([item_name, round(initial_investment, 2), round(current_price,2), round(current_price-initial_investment, 2), f"{round(((current_price-initial_investment)/initial_investment) * 100)}%", time.ctime()])
            initial_investment_total += initial_investment
            current_total += current_price
            # i += 1
            # if i == 1:
            #     break
        except Exception:
            print("Item Data not available.")


    profit = current_total - initial_investment_total

    individual_profits.sort(key=lambda row:row[3], reverse=True)

    myprofits = open("myprofits.txt", "a")
    myprofits.write(f"{round(profit, 2)} {round(current_total, 2)} {round(initial_investment_total,2)} {int(time.time())}\n")
    myprofits.close()

    # print(f"\nProfit: ${round(profit, 2)}, Revenue: ${round(current_total, 2)}, Investment: ${round(initial_investment_total,2)}, Time: {time.ctime()}")
    response_profit = f"Profit: ${round(profit, 2)}, Revenue: ${round(current_total, 2)}, Investment: ${round(initial_investment_total,2)}, Time: {time.ctime()}\n"
    return individual_profits, response_profit


async def display_item_profits(individual_profits):
    # response_individual_profit = "NAME, INITIAL INVESTMENT, CURRENT PRICE, PROFIT, PERCENT, TIME\n"
    # print("NAME, Initial Investment, Current Price, Profit, Percent, Time")

    ind_profits_analysis = open("itemanalysis.txt", "w", encoding="utf-8")
    ind_profits_analysis.write("NAME, INITIAL INVESTMENT, CURRENT PRICE, PROFIT, PERCENT, TIME\n")
    try:
        for item_profits in individual_profits:
            ind_profits_analysis.write(", ".join(str(item_data) for item_data in item_profits) + "\n")
    except Exception as e:
        print(f"Error printing item profit analysis: {e}")
    ind_profits_analysis.close()


    # try: 
    #     for item_profits in individual_profits:
    #         response_individual_profit += ", ".join(str(item_data) for item_data in item_profits) + "\n"
    #     return response_individual_profit
    # except Exception as e:
    #     print(e)
    #     print("Error printing")
    #     return "Error in Calculating Individual Profits"


async def scrape() -> str:
    urls = [file.strip() for file in open("urls.txt", "r").readlines()]
    items = await scrape_data(urls)
    individual_profits, response = await calculate_investments(items)
    await display_item_profits(individual_profits)
    return response 
    