from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dictor import dictor
import time
import json
import os


print("Setting things up")


#setting up proxy to intercept network traffic
dict = {'port': 8090}
server = Server(path="browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat", options=dict) #path to your browsermob-proxy bin
server.start()
time.sleep(1)
proxy = server.create_proxy()
time.sleep(1)
options = FirefoxOptions()
options.add_argument("--headless") #headless mode to avoid gui
profile = webdriver.FirefoxProfile()
selenium_proxy = proxy.selenium_proxy()
profile.set_proxy(selenium_proxy)#to be fixed, deprecation warning
driver = webdriver.Firefox(firefox_profile=profile, options=options)


print("enter site to extract coupons")
link = input() #url of the website
tmp = link.split(".")
title = tmp[1] #separates title


#network interception starts using browserproxymob
print('loading site')
proxy.new_har(options={'captureContent':True})
driver.get(link)
print('network interception active')
time.sleep(10) #wait time, increase or decrease this according to your network speed
with open('%s.har' %title, 'w') as har_file: #dump of entire network activity
    parsed = json.dump(proxy.har, har_file)

with open('%s.har' %title, 'r') as handle:
    parsed = json.load(handle)

proxy.close() #closing proxy
server.stop()
driver.close() #selenium close
driver.quit()

prettyfile = (json.dumps(parsed, indent=4, sort_keys=True)) #prettyprinting json

os.remove('%s.har' %title) #removing har file

with open("%s_neat.json" %title, "w") as prettyjson:
    prettyjson.write(prettyfile)

print("network activity dumped and cleaned")

print("searching for coupons")



#Searching for relevant data
with open("%s_neat.json" %title, "r") as handle2:
    nicefile = json.load(handle2) 

keyz = ["gravity", "code", "coupon"] #keywords which we want in our final file
notkeyz = ["function"] #keywords we don't need in our final file

with  open("%s_textonly.json" %title, "w") as txtfile: 
        txt = dictor(nicefile, 'log.entries.%d.response.content.text' %i, default='') #finding relevant data in complex json tree
        if all(x in txt for x in keyz):
            if any(y in txt for y in notkeyz):
                pass
            else:    
                txtc = txt.encode('unicode_escape') #hack to include escape characters in the final file
                txtd = txtc.decode('utf-8') 
                txtfile.write(txtd)

os.remove("%s_neat.json" %title) #deleting file we don't need

print("")
print("Please search for coupon codes in %s_textonly.json" %title)
