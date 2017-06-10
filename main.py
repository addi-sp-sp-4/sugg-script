import os
import requests
from bs4 import BeautifulSoup
import json
import time
import date_converter

if not os.path.isfile('data/cookie.txt'):
    cookie = raw_input("Please enter your cookie here: ")
    f = open('data/cookie.txt', 'w')
    f.write(cookie)
    f.close()
    
else:
    f = open('data/cookie.txt')
    cookie = f.read()
    f.close()

url = raw_input("Enter your URL: ")

output = 'output/' + raw_input('Enter your outfile: ').replace('/', '_')
headers = {

    "Cookie": cookie,
    "User-Agent": "Suggestion bot v1"

}

print "Getting page..."
r = requests.get(url, headers=headers)

if os.name == 'posix':
    soup = BeautifulSoup(r.content, 'lxml')
else:
    soup = BeautifulSoup(r.content, 'html.parser')


last_exc_url_elements = soup.findAll('a', {'data-tip': 'top'})

data = {}

print "Getting exchange info and history..."

for element in last_exc_url_elements:
    original_id = element.get('data-original-id')
        
    exchange_json_url = 'https://backpack.tf/item/{}/last_exchanged'.format(original_id)
    exchange_json = requests.get(exchange_json_url, headers=headers)
    print "Exchange info retrieved for item with id {}".format(original_id)
    
    json_obj = json.loads(exchange_json.content)

    properties = {}
    if json_obj['exists'] and not json_obj['never']:
        if json_obj['duped']:
            properties['duped'] = True
        else:
            properties['duped'] = False

        if json_obj['days'] >= 91:
            print "Sale older than 90 days, disregarding..."
            print ""
            continue
            
        properties['last_traded'] = json_obj['days']
        
    else:
        print "Never traded yet, disregarding..."
        print ""
        continue

    history = {}

    history_url = "https://backpack.tf/item/{}".format(original_id)
    
    history_page = requests.get(history_url, headers=headers)

    print "History received for item with id {}".format(original_id)
    
    if os.name == 'posix':
        history_soup = BeautifulSoup(history_page.content, 'lxml')
    else:
        history_soup = BeautifulSoup(history_page.content, 'html.parser')

    table_parent = history_soup.find('div', {'class': 'history-sheet'})

    table = table_parent.find('table')

    skipped = False

    time_rn = time.time()
    time_in_three_months = 2629743.83 * 3
    for row in table.findAll('tr'):
        if not skipped:
            skipped = True
            continue
        
        user_id = row.find('a', {'class': 'user-link'}).get('data-id')
        last_seen = row.find('a', {'data-tip': 'bottom'}).get('href')[33:]
        
        if time_rn - int(last_seen) < time_in_three_months:
            
            day = date_converter.timestamp_to_string(int(last_seen), "%d/%m/%Y")
            last_seen = int(date_converter.string_to_timestamp(day, "%d/%m/%Y")) + 7200
            
            history[last_seen] = user_id

    properties['history'] = history
    data[original_id] = properties
    print ""
    
f = open(output, 'a')

for item in data:

    for history in data[item]['history']:
        begin_date = date_converter.timestamp_to_string(int(history), "%m/%d")
        end_date = date_converter.timestamp_to_string(int(history) - 86400, "%m/%d")
        link = "http://backpack.tf/profiles/{}#!/compare/{}/{}".format(data[item]['history'][history], history - 86400, history)
        f.write("{} | {} - {} \n".format(link, begin_date, end_date))
        print link

f.close()
