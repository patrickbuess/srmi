import re
import requests
from lxml.html import fromstring


# FUNCTION TO ITERATE THROUGH LISTING INFOS
def get_list_content_pairs(doc):
    main = doc.find("dl", class_="attributes-grid")
    return(main.find_all("div", class_="column"))


# FUNCTION TO REPLACE MULTIPLE SUBSTRINGS IN STRING
def replaceMultiple(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)


# FUNCTION TO GET PROXY LIST
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies
