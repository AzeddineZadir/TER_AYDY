import re
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

import time



def getScrappedUrls():
	scrapingUrls = ["https://fr.hotels.com/search.do?destination-id=504261&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=506438&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=10954767&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=10675457&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=506950&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=10955008&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=512768&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=513331&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=1692156&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=510502&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=528019&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER"
       ]
	
	
	
	return scrapingUrls


options = Options()
#Evite que le navigateur firefox s'ouvre
options.add_argument('--headless')

scrapingUrls = getScrappedUrls()

i = 0
for surl in scrapingUrls :

	driver = webdriver.Firefox(options=options)




	if len(sys.argv) < 2:
	    print("Error.\nUsage: python3 hotelScraper.py url-from-hotels.com city_scrapped")
	    sys.exit(1)




	listURL = [ ]
	firefox_dev_binary = FirefoxBinary(r'/usr/bin/firefox')
	#driver = webdriver.Firefox(firefox_binary=firefox_dev_binary, executable_path="geckodriver")

	driver.get(surl)


	allLinks = driver.find_elements_by_xpath('//a[@class="guest-reviews-link reviews-link"]')

	for links in allLinks:
		# print(links.get_attribute("href"))
		listURL.append(links.get_attribute("href"))




	
	f = open("./comments/"+sys.argv[2]+".csv", "a")

	f.write("commentaire$text\n")

	for url in listURL:
		driver.get(url)
		time.sleep(10)
		avis = driver.find_elements_by_xpath('//blockquote[@class="expandable-content description"]')


		print(len(avis))
		for reviews in avis:
			tmp = re.sub('\n',' ',reviews.text )
			f.write("comments  " + str(i) +'$')

			f.write(tmp)
			# print(tmp)
			f.write("\n")
			i=i+1

	f.close()
	driver.quit()






