import asyncio
from aiohttp import ClientSession
import re
from bs4 import BeautifulSoup
import urllib.request
import random
from datetime import datetime
startTime = datetime.now()
import csv
import time

# - a list of urls/ domains
# - Max requests for each url (by domain)
# - Max crawl depth for each url
# - Search pattern (regex)
# - Wait time between requests (by domain)
# Output:
# - Either a delimited list or import/ input to a database
# -- one row for each domain from the input list
# --- url
# --- pattern (if not found, empty)
# --- url pattern was found on (if not found, empty)


url_list = [
  "https://www.seologs.com/",
  "http://myipneighbors.com/",
  "https://allthingsblogging.com/",
  "http://badijones.com/"
]

headers = {
    'User-Agent': 'Mozilla/5.0'
}


result_list = []

regex_input = input("Enter your regex: ")
csv_file = input("Enter csv file name: ")

waiting_time = input("Please enter waiting time(In second): ")
max_depth = input("Please enter max search depth: ")
max_request = input("Please enter max request: ")

if not regex_input: regex_input = 'wp-content/themes[^" \n\r]+'

if csv_file:
    with open('%s'%csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            url_list.append(row[0])

if waiting_time: 
    waiting_time = int(waiting_time)
else:
    waiting_time = None

if max_depth:
    max_depth = int(max_depth)
else:
    max_depth = 1

if max_request: 
    max_request = int(max_request)
else:
    max_request = 100


#filename_input = input("Enter your regex")
#wp-content/themes[^" \n\r]+

async def fetc_data(url,regex):
    async with ClientSession(headers=headers) as session:
        async with session.get(url, headers=headers) as response:
            response = await response.read()
            obj = re.search(r'%s'%regex,response.decode('utf-8'))
            result = {}
            link = url
            try:
                result["Domain Name"] = url
                result["Found Object"] = ','.join([obj.group()])
                result["URL"] = url
                result["Pattern"] = regex
                result["Found"] = True
                result_list.append(result)
                if obj.group():
                    return
            except Exception as e:
                pass

            if max_depth == 2:
                soup = BeautifulSoup(response.decode('utf-8'),"html.parser") 
                print("Number of url found in second level",len(soup.find_all('a', href=True)))
                req = 0
                urls = list(set(soup.find_all('a', href=True)))
                for link in urls:
                    if waiting_time:
                        time.sleep(waiting_time) 
                    if url in str(link["href"]) and req <= max_request and '.mp3' not in str(link["href"]):
                        req = req + 1
                        link = link["href"]  
                        print("Crawling now(Second Level): ",link)
                        async with session.get(link, headers=headers) as response:
                            response = await response.read()
                            obj = re.search(r'%s'%regex,response.decode('utf-8'))
                            result = {}
                            try:
                                result["Domain Name"] = url
                                result["Found Object"] = ','.join([obj.group()])
                                result["URL"] = link
                                result["Pattern"] = regex
                                result["Found"] = True
                                result_list.append(result)
                                if obj.group():
                                    return
                            except Exception as e:
                                pass

            if max_depth == 3:
                soup = BeautifulSoup(response.decode('utf-8'),"html.parser")
                print("Number of url found in Second level", len(soup.find_all('a', href=True)))
                req = 0 
                urls = list(set(soup.find_all('a', href=True)))
                for link in urls:
                    if waiting_time:
                        time.sleep(waiting_time)                    
                    if url in str(link["href"]) and req <= max_request and '.mp3' not in str(link["href"]):
                        req = req + 1
                        link = link["href"]
                        async with session.get(link, headers=headers) as response:
                            print("Crawling now(Second Level): ",link)
                            response = await response.read()
                            obj = re.search(r'%s'%regex,response.decode('utf-8'))
                            result = {}
                            try:
                                result["Domain Name"] = url
                                result["Found Object"] = ','.join([obj.group()])
                                result["URL"] = link
                                result["Pattern"] = regex
                                result["Found"] = True
                                result_list.append(result)
                                if obj.group():
                                    return
                            except Exception as e:
                                pass

                            soup = BeautifulSoup(response.decode('utf-8'),"html.parser")
                            print("Number of url found in Third level: ",len(soup.find_all('a', href=True)))
                            req = 0
                            urls = list(set(soup.find_all('a', href=True)))
                            for link in urls:
                                if waiting_time:
                                    time.sleep(waiting_time)                                
                                if url in str(link["href"]) and req <= max_request and '.mp3' not in str(link["href"]): 
                                    req = req + 1 
                                    link = link["href"] 
                                    print("Crawling now(Third Level): ",link)
                                    async with session.get(link, headers=headers) as response:
                                        response = await response.read()
                                        obj = re.search(r'%s'%regex,response.decode('utf-8'))
                                        result = {}
                                        try:
                                            result["Domain Name"] = url
                                            result["Found Object"] = ','.join([obj.group()])
                                            result["URL"] = link
                                            result["Pattern"] = regex
                                            result["Found"] = True
                                            result_list.append(result)
                                            if obj.group():
                                                return 
                                        except Exception as e:
                                            pass
            for result in result_list:
                if result["Domain Name"] != url:
                    result = {}
                    result["Domain Name"] = url
                    result["Found Object"] = 'Not Found'
                    result["URL"] = ""
                    result["Pattern"] = regex
                    result["Found"] = False
                    result_list.append(result)

                    
loop = asyncio.get_event_loop()
count = 0

for url in url_list:
    count += 1
    print ("count:",count)
    try:
        loop.run_until_complete(fetc_data(url, regex_input))
    except Exception as e:
        print("Errror", e)
        pass

try:
    keys = result_list[0].keys()
    with open('output-%s.csv'%startTime, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        result_list = [dict(t) for t in set([tuple(d.items()) for d in result_list])]
        dict_writer.writerows(result_list)
except Exception as e:
    print ("no result found")