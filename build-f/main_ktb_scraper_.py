# Reads pdfs.
import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
import urllib.parse
from urllib.parse import urljoin

#from tabula import read_pdf
from tabulate import tabulate
import pdfplumber


# Map month numbers
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
    """ Disables SSL certificate verification and suppresses InsecureRequestWarning """
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_page_content(url):
    """ Fetches the content of the given URL. Returns the response object if successful, else None. """
    resp = requests.get(url, verify=False)
    if resp.status_code == 200:
        return resp.content
    else: 
        print(f"Failed to retrieve the page. Status code is {resp.status_code}")
        return None

def parse_pdf_links(html_content):
    """ Parses the HTML content to find all PDF file links. Returns the last href found. """
    soup = BeautifulSoup(html_content, "html.parser")
    pdf_links = [a_tag.get('href') for a_tag in soup.find_all('a') if a_tag.get('href') and '.pdf' in a_tag.get('href')]
    return pdf_links[-1] if pdf_links else None

def extract_month_number(month_string):
    """ Extracts the month number from the month string (e.g., "TEMMUZ 2024"). """
    for month, name in months_mapping.items():
        if name.upper() in month_string.upper():
            return month
    return None

def find_newest_month_html(html_content):
    """ Checks the month texts from HTML content and returns the largest month number. """
    soup = BeautifulSoup(html_content, "html.parser")
    month_numbers = [extract_month_number(td.get_text()) for td in soup.find_all('a') if td.get('href') and '.pdf' in td.get('href') and extract_month_number(td.get_text())]
    return max(month_numbers, default=None)

def read_pdf_from_url(hrefs, base_url):
    """
    Reads the PDF content from the given href.
    Prints the extracted text.
    """
    full_url = urljoin(base_url, hrefs)
    response = requests.get(full_url, verify=False)

    if response.status_code == 200:
        pdf_content = BytesIO(response.content)
        
        with pdfplumber.open(pdf_content) as pdf:
            page_number = 3 
            table_one_page = pdf.pages[page_number]
            table_one_txt = table_one_page.extract_text_simple()
            print(f"4. Sayfa İçeriği:\n{table_one_txt}")
    else:
        print(f"PDF alınamadı {full_url}, durum kodu: {response.status_code}")          
                

# Main script execution
url = "https://istanbul.ktb.gov.tr/TR-368430/istanbul-turizm-istatistikleri---2024.html"
base_url = "https://istanbul.ktb.gov.tr"
disable_ssl_warnings()

html_content = fetch_page_content(url)
if html_content:
    hrefs = parse_pdf_links(html_content)
    newest_month = find_newest_month_html(html_content)
    
    if hrefs:
        read_pdf_from_url(hrefs, base_url)  # Directly reads and extracts PDF content without saving
    else:
        print("No PDF link found.")
else:
    print("Failed to fetch HTML content.")

