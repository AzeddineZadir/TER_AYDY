import re
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

import time



def getScrappedUrls():
	scrapingUrls = ["https://fr.hotels.com/search.do?destination-id=504261&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=10954767&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=10675457&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=506950&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=10955008&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=512768&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=513331&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
        "https://fr.hotels.com/search.do?destination-id=1692156&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=510502&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=528019&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=506438&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=526515&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=494438&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=494528&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=510339&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=514337&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=1635224&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=521847&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=1634572&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=1634279&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=543279&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=511324&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=505244&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=1634556&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",	
		"https://fr.hotels.com/search.do?destination-id=530828&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=529812&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=1075991&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",	
		"https://fr.hotels.com/search.do?destination-id=535554&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=1634618&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",	
		"https://fr.hotels.com/search.do?destination-id=1634547&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=1634565&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=541701&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",	
		"https://fr.hotels.com/search.do?destination-id=521861&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=512620&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",
		"https://fr.hotels.com/search.do?destination-id=506856&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER",		
		
		]

	
	
	
	
	
	return scrapingUrls

def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(30)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height



options = Options()
#Evite que le navigateur firefox s'ouvre
options.add_argument('--headless')

scrapingUrls = getScrappedUrls()

i = 0

driver = webdriver.Firefox(options=options)



surl ="https://fr.hotels.com/search.do?destination-id=1634556&q-check-in=2021-04-12&q-check-out=2021-04-13&q-rooms=1&q-room-0-adults=2&q-room-0-children=0&sort-order=BEST_SELLER"


if len(sys.argv) < 1:
    print("Error.\nUsage: python3 hotelScraper.py url-from-hotels.com city_scrapped")
    sys.exit(1)
listURL = [ ]
firefox_dev_binary = FirefoxBinary(r'/usr/bin/firefox')
#driver = webdriver.Firefox(firefox_binary=firefox_dev_binary, executable_path="geckodriver")
driver.get(surl)
# scroller  jusqua target 
scroll_down()

allLinks = driver.find_elements_by_xpath('//a[@class="guest-reviews-link reviews-link"]')
time.sleep(20)
print(len(allLinks))

for links in allLinks:
	nb = len(links.get_attribute("href"))
	print(f"nombre hotels {nb}")
	listURL.append(links.get_attribute("href"))
nb_hotels = len(listURL)
print()

f = open("./comments/"+sys.argv[1]+".csv", "a")
f.write("commentaire$text\n")
for url in listURL:
		driver.get(url)
		# scroll_down()
		time.sleep(30)
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

