from bs4 import BeautifulSoup
import requests
import csv
from datetime import date

namecsv = 'List of New Games Released ' + str(date.today()) + '.csv'
url_filter = 'https://store.steampowered.com/search/?sort_by=Released_DESC&untags=493&category1=998&unvrsupport=401&supportedlang=english&page='
pages_to_search = 8

def generate_csv(csvname, base_url, numofpages):
    with open(csvname, 'w', encoding='utf-8', newline='') as csvfile:
        writecsv = csv.writer(csvfile, delimiter=',')
        writecsv.writerow(['Name of Game', 'Release Date', 'Price', 'Link To Game']) #base row 
        for num in range( 1 , numofpages+1 ):
            url = base_url + str(num)
            print('Went To ', url)
            get_online_html = requests.get(url)
            soup = BeautifulSoup(get_online_html.content, 'lxml')
            get_list = soup.find(id = 'search_resultsRows') #narrows it down to the right section
            game_entry = get_list.find_all('a', href=True) #actual list of games 
            for i in game_entry: #iterates per game in current page
                url_link = i['href']
                game_title = i.find('span', class_='title').get_text()
                release_date = i.find('div', class_='col search_released responsive_secondrow').get_text()
                if i.find('div', class_= 'col search_price discounted responsive_secondrow'): #if game is discounted
                    discounted = i.find('div', class_= 'col search_price discounted responsive_secondrow')
                    game_price = discounted.get_text(strip=True) #unfortunately currently gets both original price and discounted price in a joined string. idk how to fix
                else:
                    game_price = i.find('div', class_='col search_price responsive_secondrow').get_text(strip=True) 
                if len(game_price) == 0 or game_price == 'Free' or game_price == 'Free To Play' or game_price == 'Free to Play': #skips entry if the game is free or not out yet(doesnt have a price)
                    continue
                writecsv.writerow([ game_title , release_date , game_price, url_link ]) #write to csv!!
    print('Generated', csvname)

generate_csv(namecsv,url_filter,pages_to_search)
