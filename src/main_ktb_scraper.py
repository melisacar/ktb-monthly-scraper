import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
import pandas as pd


# Map month numbers.
months_mapping = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık"
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

def parse_pdf_links(html_content):
    """
    Parses the HTML content to find all PDF file links.
    Returns the last href found (the most recent one).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    # Find the specific article class.
    links = soup.find_all('a', style='font-family: Georgia; font-size: 14px;')
    
    if not links:
        print("No link with class 'font-family: Georgia; font-size: 14px;' found.")
        return None
    
    elements = soup.find_all(
        'a'
    )
    hrefs = [element.get('href') for element in elements if element.get('href') and '.pdf' in element.get('href')]
     # If hrefs list empty, return None
    if not hrefs:
        print("No links found.")
        return None
    return hrefs           ##### Returns only the last href.!!!! Here is Agustos 2024




# Control
#print(hrefs)
####################################################################
    # HTML Control.
#if html_content:
#    print(html_content.decode('utf-8'))  # HTML content.
#else:
#    print("Failed to fetch HTML content.")

    # Control.
#if html_content:
#    hrefs = parse_excel_links(html_content)
#    print(hrefs)  # Hrefs list.
# else:
#    print("Failed to fetch HTML content.")
####################################################################


def extract_month_number(month_string):
    """
    Extracts the month number from the month string (e.g. "TEMMUZ SONU"). 
    Returns the month number as an integer.
    """
    for month, name in months_mapping.items():
        if month_string.strip().upper() == name:
            return month
    return None

def find_newest_month_html(html_content):
    """
    Checks the month texts from HTML content and returns the largest month number.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    month_numbers = []

    td_elements = soup.find_all('a', style='font-family: Georgia; font-size: 14px;')
    for td in td_elements:
        if '.pdf' in td.get('href'):  # Sadece PDF bağlantıları
            month_string = td.get_text()
            print(month_string)
            month_number = extract_month_number(month_string)
            if month_number:
                month_numbers.append(month_number)

    return month_numbers


# Add to main function at the end.
url = "https://istanbul.ktb.gov.tr/TR-368430/istanbul-turizm-istatistikleri---2024.html"


html_content = fetch_page_content(url)
hrefs = parse_pdf_links(html_content)


newest_month = find_newest_month_html(html_content)
#print(newest_month)