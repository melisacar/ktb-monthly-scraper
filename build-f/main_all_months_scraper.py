import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.parse import urljoin
import pdfplumber

# Map month numbers
months_mapping = {
    1: "OCAK",
    2: "ŞUBAT",
    3: "MART",
    4: "NİSAN",
    5: "MAYIS",
    6: "HAZİRAN",
    7: "TEMMUZ",
    8: "AĞUSTOS",
    9: "EYLÜL",
    10: "EKİM",
    11: "KASIM",
    12: "ARALIK"
}

def disable_ssl_warnings():
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_page_content(url):
    resp = requests.get(url, verify=False)
    if resp.status_code == 200:
        return resp.content
    else: 
        print(f"Failed to retrieve the page. Status code is {resp.status_code}")
        return None

def parse_pdf_links(html_content):
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

def get_year_from_page(pdf, page_number):
    """
    Extracts the year from the specified page, looking for the last occurrence in the 'AYLAR' row.
    """
    table_one_txt = pdf.pages[page_number].extract_text_simple()
    #print(table_one_txt)
    if table_one_txt:
        lines = table_one_txt.split('\n')

    for line in lines:
            line_clean = line.strip()  
            if line_clean.upper().startswith("AYLAR"):  
                year = line_clean.split()[-3]  # Divide to words.
                #print(year)
                return year  
    return None

def read_pdf_from_url(href, base_url, latest_month):
    full_url = urljoin(base_url, href)
    response = requests.get(full_url, verify=False)

    if response.status_code == 200:
        pdf_content = BytesIO(response.content)
        
        with pdfplumber.open(pdf_content) as pdf:
            year = get_year_from_page(pdf, page_number=3)
            if not year:
                print("Year not found on the specified page.")
                return
            
            for month_num in range(latest_month, 0, -1):  # Start from latest month and go back to January
                month_name = months_mapping[month_num].upper()
                month_found = False

                for page in pdf.pages:
                    
                    page_number = 3
                    table_one_page = pdf.pages[page_number]
                    table_one_txt = table_one_page.extract_text_simple()

                    if table_one_txt:
                        for line in table_one_txt.split('\n'):
                            if month_name in line.upper():
                                month_found = True
                                value = line.split()
                                try:
                                    turkiye_value = value[3]
                                    istanbul_value = value[7]
                                    date_prefix = f"{year}-{month_num:02d}-01"
                                    print(f"{date_prefix} Türkiye {turkiye_value}")
                                    print(f"{date_prefix} İstanbul {istanbul_value}")
                                except IndexError:
                                    print(f"Data not found in expected position for {month_name}. Line: {line}")
                                break
                    if month_found:
                        break
                if not month_found:
                    print(f"{month_name} not found in PDF.")
    else:
        print(f"PDF alınamadı {full_url}, durum kodu: {response.status_code}")

# Main script execution
url = "https://istanbul.ktb.gov.tr/TR-368430/istanbul-turizm-istatistikleri---2024.html"
base_url = "https://istanbul.ktb.gov.tr"
disable_ssl_warnings()

html_content = fetch_page_content(url)
if html_content:
    href = parse_pdf_links(html_content)
    newest_month = find_newest_month_html(html_content)
    
    if href and newest_month:
        read_pdf_from_url(href, base_url, newest_month)
    else:
        print("No PDF link found or no valid month found.")
else:
    print("Failed to fetch HTML content.")
