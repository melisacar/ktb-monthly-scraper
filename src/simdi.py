import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.parse import urljoin
import pdfplumber
import pandas as pd

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

def get_all_pdf_links(html_content):
    """
    Finds all .pdf links in the HTML content.
    Returns a list of tuples (href, text).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    pdf_links = [
        (a_tag.get('href'), a_tag.get_text(strip=True)) 
        for a_tag in soup.find_all('a') 
        if a_tag.get('href') and '.pdf' in a_tag.get('href')
    ]
    return pdf_links

def extract_month_and_year(text):
    """ Extracts the month and year from the given text. """
    for month, name in months_mapping.items():
        if name.upper() in text.upper():
            # Extract year as the first 4-digit number in the text
            year = next((int(word) for word in text.split() if word.isdigit() and len(word) == 4), None)
            return year, month
    return None, None

def find_latest_pdf(pdf_links):
    """
    Finds the latest .pdf link based on the month and year in the link text.
    pdf_links: List of tuples (href, text).
    Returns the href of the latest .pdf file.
    """
    dated_pdfs = []
    
    for href, text in pdf_links:
        year, month = extract_month_and_year(text)
        if year and month:
            dated_pdfs.append((href, year, month))
    
    if dated_pdfs:
        # Find the most recent (year, month)
        latest_pdf = max(dated_pdfs, key=lambda x: (x[1], x[2]))
        return latest_pdf[0]  # Return the href of the latest PDF

    return None

def read_pdf_from_url(href, base_url, latest_month):
    """
    Reads the PDF content from the given href and extracts data for all months in the PDF.
    """
    full_url = urljoin(base_url, href)
    response = requests.get(full_url, verify=False)
    output = []

    if response.status_code == 200:
        pdf_content = BytesIO(response.content)
        
        with pdfplumber.open(pdf_content) as pdf:
            year = latest_month[0]  # Assuming year is passed from main
            if not year:
                print("Year not found on the specified page.")
                return
            
            for month_num in range(latest_month[1], 0, -1):  # Start from latest month and go back to January
                month_name = months_mapping[month_num].upper()
                month_found = False

                for page in pdf.pages:
                    table_one_txt = page.extract_text()
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
    
    df = pd.DataFrame(output, columns=["tarih", "ist_tr", "ziyaretci_sayisi"])
    
    return df

def main_all():
    """
    Main script execution.
    Fetches HTML content, identifies the latest PDF link, and processes its data.
    """
    url = "https://istanbul.ktb.gov.tr/TR-368430/istanbul-turizm-istatistikleri---2024.html"
    base_url = "https://istanbul.ktb.gov.tr"
    disable_ssl_warnings()

    # Fetch HTML content
    html_content = fetch_page_content(url)
    if html_content:
        # Get all .pdf links
        pdf_links = get_all_pdf_links(html_content)
        print(f"Found PDF links: {pdf_links}")
        
        # Find the latest .pdf link
        latest_pdf_href = find_latest_pdf(pdf_links)
        if latest_pdf_href:
            print(f"Latest PDF link: {latest_pdf_href}")
            
            # Process the latest PDF
            latest_month = extract_month_and_year(next(text for href, text in pdf_links if href == latest_pdf_href))
            if latest_month:
                df = read_pdf_from_url(latest_pdf_href, base_url, latest_month)
                print(df)
            else:
                print("Could not extract the latest month and year from the link.")
        else:
            print("No valid PDF link with a date was found.")
    else:
        print("Failed to fetch HTML content.")

main_all()
