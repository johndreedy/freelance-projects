import requests
from bs4 import BeautifulSoup
from datetime import datetime

game_name = "fallout3"
date_specified = 'Jan 2009'

url = f'https://www.nexusmods.com/{game_name}/mods/toprecent/?offset=0&time=59'

session = requests.Session()
response = session.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
tabcontent = soup.find('div', class_='tabcontent top-list')
dates = tabcontent.find_all('time', class_='date')

# create an empty list to hold the dates
date_array = []

# loop through all dates and append them to the date_array
for date in dates:
    if "Uploaded:" in date.span.text:
        date_text = date.text.strip().replace("Uploaded: \n", "Uploaded: ")
        # parse the date string as a datetime object
        date_obj = datetime.strptime(date_text, "Uploaded: %d %b %Y")
        date_array.append(date_obj)

# sort the date_array by date/month/year in ascending order
date_array.sort()

# get the newest date in the array
newest_date = date_array[-1]

# loop through mod URLs and check if each one exists
mod_tiles = soup.find_all('li', class_='mod-tile')
for tile in mod_tiles:
    date_elem = tile.find('time', class_='date')
    if date_elem is not None and "Uploaded:" in date_elem.span.text:
        date_text = date_elem.text.strip().replace("Uploaded: \n", "Uploaded: ")
        # parse the date string as a datetime object
        date_obj = datetime.strptime(date_text, "Uploaded: %d %b %Y")
        if date_obj == newest_date:
            url_elem = tile.find('a', class_='mod-image')
            if url_elem is not None:
                mod_url = url_elem.get('href')
                # increment the mod URL by 1 and check if the mod exists
                mod_num = int(mod_url.split('/')[-1])
                while True:
                    mod_num += 1
                    mod_url = f"https://www.nexusmods.com/{game_name}/mods/" + str(mod_num)
                    mod_response = requests.get(mod_url)
                    mod_soup = BeautifulSoup(mod_response.content, 'html.parser')
                    wrapper_div = mod_soup.find('div', id='mainContent', class_='wrapper')
                    if wrapper_div is not None and 'The mod you were looking for couldn\'t be found' in wrapper_div.text:
                        # decrement the mod URL by 1 and print the final URL
                        mod_num -= 1
                        final_url = f"https://www.nexusmods.com/{game_name}/mods/" + str(mod_num)
                        print(final_url)
                        break
                # print mod_num incremented in increments of 0.25%
                mod_num = int(mod_num)
                mod_num_perc = mod_num / 100
                for i in range(401):
                    new_mod_url = f"https://www.nexusmods.com/{game_name}/mods/" + str(int(mod_num_perc * i * 0.25)) + "?tab=files"
                    print(new_mod_url)
                    mod_response = requests.get(new_mod_url)
                    mod_soup = BeautifulSoup(mod_response.content, 'html.parser')
                    accordionitems = mod_soup.find_all('div', class_='accordionitems')
                    for item in accordionitems:
                        stat_uploaddates = item.find_all('li', class_='stat-uploaddate')
                        for date in stat_uploaddates:
                            print(date.text.strip())
                            if date_specified in date.text:
                                break
                        else:
                            continue
                        break
                    else:
                        continue
                    break

                # check if the current month is the same as the specified month, and exit the loop if it is

