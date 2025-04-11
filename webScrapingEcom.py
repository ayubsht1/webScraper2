import requests
import random
from bs4 import BeautifulSoup

proxies_list = {
'154.117.220.13:3128',
'207.246.234.115:4669'
}

user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)"
]

url = 'https://lucknow.craigslist.org'
proxy = random.choice(list(proxies_list))
headers = {'User-Agent': random.choice(user_agents),
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
           }

try:
    response = requests.get(url, headers=headers, proxies={"http":proxy, "https":proxy}, timeout=100)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())
    else:
        print(f"Request blocked or failed. Status Code: {response.status_code}")
except Exception as e:
    print(f"Proxy failed: {proxy}\nError: {e}")
