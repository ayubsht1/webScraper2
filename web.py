import requests
from bs4 import BeautifulSoup
import time

def get_proxies_revised():
    url = "https://spys.one/en/free-proxy-list/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")
        proxy_table = soup.find("table", class_="spy1xx")  # Try to find the main proxy table

        if proxy_table:
            proxies = []
            rows = proxy_table.find_all("tr")[2:]  # Skip header rows
            for row in rows:
                columns = row.find_all("td")
                if len(columns) >= 2:
                    # This is a simplified assumption - the actual structure is more complex
                    ip_port_element = columns[0].find("font", class_="spy14") or columns[0].find("a")
                    if ip_port_element and ":" in ip_port_element.get_text(strip=True):
                        proxies.append(ip_port_element.get_text(strip=True))
            return proxies
        else:
            print("Proxy table not found.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve or parse proxies: {e}")
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

    proxies_list = get_proxies_revised()
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