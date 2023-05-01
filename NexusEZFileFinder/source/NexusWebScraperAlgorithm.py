import re
import requests
from bs4 import BeautifulSoup

base_url = "https://www.nexusmods.com/fallout3/mods/25020"
num_pages = 10

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.content
    else:
        print(f"Error {r.status_code} when requesting {url}")
        return None
    
def scrape_nexus_mods(base_url, num_pages):
    mod_id = int(re.findall(r'mods/(\d+)', base_url)[-1])
    if mod_id <= 0:
        print("Invalid mod ID. Mod ID must be greater than 0.")
        return []
    base_url = re.sub(r'mods/\d+', 'mods/', base_url)
    urls = []
    for i in range(mod_id + 1, mod_id + num_pages + 1):
        url = f"{base_url}{i}?tab=files"
        urls.append(url)
    for i in range(mod_id - 1, max(0, mod_id - num_pages - 1), -1):
        url = f"{base_url}{i}?tab=files"
        urls.append(url)
    return urls


def scrape_manual_download(url): 
    with requests.Session() as session:
        page = session.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        accordion_items = soup.find('div', {'class': 'accordionitems'})
        if accordion_items:
            manual_download = accordion_items.find_all('li', {'class': 'stat-uploaddate'})
            dates = []
            for item in manual_download:
                data_text = item.text.replace("Date uploaded", "").strip()
                print(data_text)
                dates.append(data_text)
                date_time = re.findall(r'\d+ [a-zA-Z]+ \d{4}, \d+:\d+ [AaPp][Mm]', data_text)
                if date_time:
                    print(f"Scraping {url}... ({date_time[0]})" "\n")
                    session.close()

            return dates
                
        else:
            print(f"No Manual Download section found for {url}")
            return []

def scrape_links(url, average_day, most_common_month, most_common_year):
    soup = BeautifulSoup(get_html(url), 'html.parser')
    accordion_items = soup.find('div', {'class': 'accordionitems'})
    if accordion_items:
        manual_download = accordion_items.find_all('li', {'class': 'stat-uploaddate'})
        dates = []
        for item in manual_download:
            data_text = item.text.replace("Date uploaded", "").strip()
            dates.append(data_text)
        month_counts = {}
        for date in dates:
            month = date.split()[1]
            year = date.split()[2]
            if month in month_counts and year == month_counts[month][0]:
                month_counts[month][1].append(date)
            else:
                month_counts[month] = (year, [date])
        if most_common_month in month_counts and most_common_year == month_counts[most_common_month][0]:
            month_dates = month_counts[most_common_month][1]
            if average_day in [int(date.split()[0]) for date in month_dates]:
                average_day_url = url
                return average_day_url
            else:
                # choose the next nearest date
                nearest_date = min(month_dates, key=lambda date: abs(int(date.split()[0]) - average_day))
                print(f"Desired date {most_common_month} {average_day}, {most_common_year} not available. Choosing nearest date {nearest_date}")
                nearest_date_url = url
                return nearest_date_url

                
def create_final_id(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    file_container = soup.find('div', class_='tabbed-section tabbed-block files-tabs', id='file-container-main-files')
    hrefs = file_container.find_all('a')
    final_file_ids = []
    for href in hrefs:
        href_val = href.get('href')
        if href_val:
            if "/Core/Libs/" in href_val:
                final_file_id = href_val.split("?id=")[-1].split("&")[0]
                if final_file_id.isdigit():
                    final_file_ids.append(final_file_id)
            elif "&file_id=" in href_val:
                final_file_id = href_val.split("&file_id=")[-1]
                if final_file_id.isdigit():
                    final_file_ids.append(final_file_id)
    return final_file_ids

def main(base_url):

    urls = scrape_nexus_mods(base_url, num_pages)
    dates = []
    url_array = []

    for url in urls:
        print(f"Scraping {url}...")
        url_array.append(url) 
        soup = scrape_manual_download(url)
        if soup:
            dates += soup
    if not dates:
        print("No dates found.")
    else:
        month_counts = {}
        for date in dates:
            month = date.split()[1]
            year = date.split()[2]
            if month in month_counts and year == month_counts[month][0]:
                month_counts[month][1].append(date)
            else:
                month_counts[month] = (year, [date])
        most_common_month = max(month_counts, key=lambda k: len(month_counts[k][1]))
        most_common_year = month_counts[most_common_month][0]
        month_dates = month_counts[most_common_month][1]
        average_day = sum(int(date.split()[0]) for date in month_dates) // len(month_dates)
        print(f"Most common month and year: {most_common_month} {most_common_year}")
        print(f"Average day in {most_common_month} {most_common_year}: {average_day}")

        for url in url_array:
            soup = scrape_manual_download(url)
            if soup:
                final_url = scrape_links(url, average_day, most_common_month, most_common_year)
                if final_url:
                    print('FINAL URL: ' + final_url)
                    final_id = create_final_id(final_url)
                    if final_id:
                        final_file_id = min(final_id)
                        final_file_id = int(final_file_id)
                        if final_file_id > 50:
                            final_file_id -= 50
                        else:
                            final_file_id = 1
                        print('FINAL ID: ')
                        print(final_file_id)


    return final_file_id