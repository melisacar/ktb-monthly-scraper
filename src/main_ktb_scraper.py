import requests
import ssl
import urllib3
from bs4 import BeautifulSoup


# Map month numbers.
months_mapping = {
    1: "2024 Yılı Ocak Ayı",
    2: "2024 Yılı Şubat Ayı",
    3: "2024 Yılı Mart Ayı",
    4: "2024 Yılı Nisan Ayı",
    5: "2024 Yılı Mayıs Ayı",
    6: "2024 Yılı Haziran Ayı",
    7: "2024 Yılı Temmuz Ayı",
    8: "2024 Yılı Ağustos Ayı",
    9: "2024 Yılı Eylül Ayı",
    10: "2024 Yılı Ekim Ayı",
    11: "2024 Yılı Kasım Ayı",
    12: "2024 Yılı Aralık Ayı"
}

def disable_ssl_warnings():
    """
    Disables SSL certificate verification and suppresses InsecureRequestWarning.
    """
    ssl._create_default_https_content = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exception.InsecureRequestWarning)

def fetch_page_content(url):
    """
    Fetches the content of the given URL.
    Returns the response object if successful, else None.
    """
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.content
    else: 
        print(f"Failed to retrieve the page. Status code is {resp.status_code}")
        return None

def parse_excel_links(html_content):
    """
    Parses the HTML content to find all Excel file links.
    Returns the last href found (the most recent one).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all(
        'a',
        class_="art_loop"
    )
    #hrefs = 
    return None

url = "https://yigm.ktb.gov.tr/TR-366207/2024.html"
html_content = fetch_page_content(url)
print(html_content)