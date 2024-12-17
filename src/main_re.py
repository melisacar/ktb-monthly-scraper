import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.parse import urljoin
import pdfplumber
import pandas as pd
import re
import locale

locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

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

def extract_month_number(month_string):
    """ Extracts the month number from the month string. """
    normalized = tr_upper_char(month_string)
    for month, name in months_mapping.items():
        if name in normalized:
            return month
    return None

def tr_upper_char(text):
    char_map = {
        "ç":"Ç", "ğ":"Ğ", "ı":"I", "i":"İ", "ö":"Ö", "ş":"Ş", "ü":"Ü" 
    }

    return ''.join(char_map.get(m, m.upper()) for m in text)

def normalize_date_info(date_info):
    """
    Strips unnecessary spaces and converts the string to uppercase with Turkish character support.
    """
    return tr_upper_char(date_info.strip()) 

def extract_year_month(date_info):
    month_mapping = {
        "OCAK": "01", "ŞUBAT": "02", "MART": "03", "NİSAN": "04",
        "MAYIS": "05", "HAZİRAN": "06", "TEMMUZ": "07", "AĞUSTOS": "08",
        "EYLÜL": "09", "EKİM": "10", "KASIM": "11", "ARALIK": "12"
    }

    normalized_info = normalize_date_info(date_info)

    # Regex
    match = re.search(r"([A-ZÇŞİĞÜ]+)\s?(\d{4})", normalized_info)
    #[A-ZÇŞİĞÜ]+ Matches one or more uppercase letters
    #\s? Matches zero or one whitespace character.
    # \d{4} Matches exactly four digits (a year).
    if match:
        month_text = match.group(1)  # Month name
        print(f"Extracted month text: {month_text}")
        year = match.group(2)        # Year
        month = month_mapping.get(month_text.upper(), "00")
        return f"{year}-{month}-01"
    
    print(f"Invalid date_info format: {date_info}")
    return None

def extract_all_dates_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    date_links = []

    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        text = a_tag.get_text(strip=True)

        if href and '.pdf' in href.lower():
            date = extract_year_month(text)
            if date:
                date_links.append((href, date))
    return date_links

def find_latest_pdf(dates_with_links):
    if not dates_with_links:
        print("No dates with links found")
        return None, None
    latest_link, latest_date = max(dates_with_links, key=lambda x: x[1])
    return latest_link, latest_date

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
    output = []

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
                                    output.append([date_prefix, "Türkiye", turkiye_value])
                                    output.append([date_prefix, "İstanbul", istanbul_value])
                                except IndexError:
                                    print(f"Data not found in expected position for {month_name}. Line: {line}")
                                break
                    if month_found:
                        break
                if not month_found:
                    print(f"{month_name} not found in PDF.")
    else:
        print(f"PDF alınamadı {full_url}, durum kodu: {response.status_code}")
    
    df = pd.DataFrame(output, columns=["tarih","ist_tr","ziyaretci_sayisi"])
    
    return df



def main_all():
    # Main script execution

    url = "https://istanbul.ktb.gov.tr/TR-368430/istanbul-turizm-istatistikleri---2024.html"
    base_url = "https://istanbul.ktb.gov.tr"

    html_content = fetch_page_content(url)
    if html_content:
        latest_month = find_newest_month_html(html_content)
        dates_with_links = extract_all_dates_from_html(html_content)
        latest_link, latest_date = find_latest_pdf(dates_with_links) 
        if latest_link:
                print(f"En güncel PDF: {latest_link}, Tarih: {latest_date}")

                df = read_pdf_from_url(latest_link, base_url, latest_month)
                print(df)
        else:
            print("No PDF link found with valid dates.")
    else:
        print("Failed to fetch HTML content.")

main_all()