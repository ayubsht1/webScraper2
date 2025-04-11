import requests
import random
from bs4 import BeautifulSoup
import time

# Step 1: Get Proxies from spys.one
def get_proxies():
    url = "https://spys.one/en/free-proxy-list/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        # Removed xf5=1 to get all types of proxies (Transparent, Anonymous, Elite)
        response = requests.post(url, headers=headers, data={"xpp": "5", "xf1": "0", "xf2": "0", "xf4": "0"})
        soup = BeautifulSoup(response.text, "html.parser")
        proxy_table = soup.find_all("tr", {"class": "spy1xx"}) + soup.find_all("tr", {"class": "spy1x"})
        
        proxies = []
        for row in proxy_table:
            columns = row.find_all("td")
            if len(columns) > 0:
                ip_port_script = columns[0].get_text(strip=True)
                if ":" in ip_port_script:
                    proxies.append(ip_port_script)
        return proxies
    except Exception as e:
        print("Failed to retrieve proxies:", e)
        return []

# Step 2: Try each proxy to fetch Craigslist page
def scrape_with_proxy(url):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)"
    ]

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
    }

    proxies_list = get_proxies()
    print(f"Total proxies found: {len(proxies_list)}")

    for proxy in proxies_list:
        print(f"Trying proxy: {proxy}")
        try:
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
            if response.status_code == 200:
                print("✅ Success!")
                soup = BeautifulSoup(response.text, 'html.parser')
                print(soup.prettify()[:1000])  # print just a snippet
                return
            else:
                print(f"❌ Blocked: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Proxy failed: {proxy} | Error: {e}")
        time.sleep(2)

    print("No working proxies found.")

# Run the script
scrape_with_proxy("https://lucknow.craigslist.org")
