This script is written in python 3.6

To install the requirements:
	pip3 install -r requirements.txt

To run the script:
	python3 domain_scraper.py 

The script will ask you some inputs:
	1. Enter your regex: 
		You can enter your custom regex or it will use default one : 
			wp-content/themes[^" \n\r]+
	2. Enter csv file name:
		You have to enter the csv file name which contains domain list with .csv extentions. Otherwise it will check these urls:
			https://www.seologs.com/
			http://myipneighbors.com/
			http://badijones.com/
			https://allthingsblogging.com/

	3. Please enter waiting time(In second):
		If you give the waiting time, the script will wait for your given time before crawling any domain. If don't give any value, it will crawl without any delay.

	4. Please enter max search depth (Int Number): 
		you can go maximum 3 levels deep. so you can give any value between 1-3. It will go 2 levels deep by default.

	5. Please enter max request (Int Number): 
		This is the maximum domains number to scrap.If you don't give any value it will crawl all  domains from csv file.

