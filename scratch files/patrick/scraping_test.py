from bs4 import BeautifulSoup
import urllib.request
import re

url = "https://www.comparis.ch/immobilien/marktplatz/details/show/20698032"
urls = ["https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten",
        "https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten?page=1",
        "https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten?page=2",
        "https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten?page=3",
        "https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten?page=4",
        "https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten?page=5",
        "https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten?page=6"]
urls = ["https://www.comparis.ch/immobilien/marktplatz/st-gallen/mieten"]


urlList = []


# GET URLS OF EVERY LISTING
for i in urls:
    try:
        page = urllib.request.urlopen(i) # connect to website
    except:
        print("An error occured.")

    soup = BeautifulSoup(page, 'html.parser')

    for a in soup.select('a.title'):
        urlList.append("https://www.comparis.ch"+a['href'])


print(urlList)

addresses = []

# GET INFOS ON LISTINGS
for i in urlList:
    try:
        page = urllib.request.urlopen(i) # connect to website
    except:
        print("An error occured.")

    soup = BeautifulSoup(page, 'html.parser')

    for a in soup.select('div.item-price.large strong'):
        addresses.append(a)

print(addresses)

# page_response = requests.get(page, timeout=5)
# page_content = BeautifulSoup(page_response.content, "html.parser")
# textContent = []
# for i in range(0, 20):
#     paragraphs = page_content.find_all("p")[i].text
#     textContent.append(paragraphs)
# print(textContent)
