import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')

# yahoo finace site url-->https://finance.yahoo.com/
#share price x path -->//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]
client = discord.Client()

@client.event
async def on_ready():
 print('We have logged in as {0.user}'.format(client))
 general_channel = client.get_channel(Enter your channel ID here)
 await general_channel.send("Hello Guys!")

#, options = chrome_options
option = webdriver.ChromeOptions()
option.add_argument("--headless")

#driver = webdriver.Chrome()
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
wait = WebDriverWait(driver,10)   

#def alert():
 #user_price = input("Enter the price reminder-->₹")

 #if bse_share_price.text >= user_price:
    #print("Target Reached")

@client.event
async def on_message(message):
    if message.content.startswith('#begin'): 
        channel = message.channel
        await channel.send("Loading..")
        url = 'https://finance.yahoo.com/'
        driver.get(url)
        time.sleep(5)
        await channel.send("Ready to Roll !")

        def check(user):
            return user == message.author and message.channel == channel
           
        while True:
            i=0
            await channel.send('Enter the company name ↴')
            msg = await client.wait_for("message")
            company = msg.content
            #search_bar.clear()
            search_bar = driver.find_element_by_name('yfin-usr-qry')
            #company = input("Enter the company name-->")

            search_bar.send_keys(str(company))
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'modules_resultsContainer__3P2fJ')))
            #equity_type = driver.find_element_by_xpath('//*[@id="result-quotes-%s"]/div[2]/span' % (i))
            
            try:
                while True:
                    equity_type = driver.find_element_by_xpath('//*[@id="result-quotes-%s"]/div[2]/span' % (i))
                    if str(equity_type.text) == "Equity - NSI":
                        search_bar.send_keys(Keys.ENTER)
                        break
                    else:
                        search_bar.send_keys(Keys.DOWN)
                        i=i+1
            except NoSuchElementException:
                await channel.send('This company doesnt exist!')
                continue

                
              
            wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')))
            company_title_1 = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
            print(company_title_1.text)
            
            equity_type1 = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[2]/span')
            print(equity_type1.text)
            
            bse_share_price = driver.find_element_by_css_selector('span.Fw\(b\):nth-child(1)')
            print(bse_share_price.text)
            
            percentage = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[2]')
            print(percentage.text)
            
            myEmbed = discord.Embed(title="Search Result" , description=company_title_1.text,color = 0x00ff00)
            myEmbed.add_field(name="Equity Type:",value=equity_type1.text,inline=False)
            myEmbed.add_field(name="Current price :",value="₹%s"%(bse_share_price.text),inline=False)
            myEmbed.add_field(name="Percentage :",value=percentage.text,inline=False)
            myEmbed.set_footer(text="Price Alert")
            myEmbed.set_author(name="Yahoo Finance")
            await channel.send(embed = myEmbed)
            
            await channel.send("Is this the company?Enter[Y/N]")
           
            msg1 = await client.wait_for("message")
            choice = msg1.content
            if choice =='Y':
                break
    
    elif message.content.startswith('#greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))

    elif message.content.startswith('#quit'):
        channel = message.channel
        await channel.send('Bye Bye!')
        driver.quit()        

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
