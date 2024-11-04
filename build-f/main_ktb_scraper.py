#Downloads pdfs.
import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


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
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

    pdf_links = []

    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and '.pdf' in href:
            pdf_links.append(href)  

    print(pdf_links[-1])
    return pdf_links[-1] if pdf_links else None


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
    Extracts the month number from the month string (e.g. "TEMMUZ 2024"). 
    Returns the month number as an integer.
    """
    for month, name in months_mapping.items():
         if name.upper() in month_string.upper(): 
            print(month)
            return month
    return None

def find_newest_month_html(html_content):
    """
    Checks the month texts from HTML content and returns the largest month number.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    month_numbers = []

    td_elements = soup.find_all('a')

    for td in td_elements:
        href = td.get('href')
        if href and '.pdf' in href:
            month_string = td.get_text()
            #print(month_string)
            month_number = extract_month_number(month_string)
            if month_number:
                month_numbers.append(month_number)
    #print(max(month_numbers))
    return max(month_numbers, default=None)



# Downloading func.
def download_pdf_file(href, base_url):
    """
    Downloads the PDF file from the given href.
    Returns the content of the file if successful, else None.
    """
    full_url = urljoin(base_url, href)  
    #print(full_url)
    response = requests.get(full_url, verify=False)

    if response.status_code == 200:
        pdf_filename = href.split("/")[-1].split("?")[0]
        pdf_path = f"./{pdf_filename}"

        with open(pdf_path, "wb") as f:
            f.write(response.content)

            print(f"Downloaded: {pdf_filename}")
        return True
    else:
        print(f"Failed to retrieve {href}, status code: {response.status_code}")
        return False
    
########################################################################################
url = "https://istanbul.ktb.gov.tr/TR-368430/istanbul-turizm-istatistikleri---2024.html"
base_url = "https://istanbul.ktb.gov.tr" 
disable_ssl_warnings()

html_content = fetch_page_content(url)
hrefs = parse_pdf_links(html_content)

newest_month = find_newest_month_html(html_content)
#print(newest_month)
if hrefs: 
    download_pdf_file(hrefs, base_url)  
else:
    print("No PDF link found.")
########################################################################################