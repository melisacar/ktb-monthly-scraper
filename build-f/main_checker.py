# Reads PDFs.
import requests
import ssl
import urllib3
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
import urllib.parse
from urllib.parse import urljoin
from tabulate import tabulate
import pdfplumber
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import extract
from models import gelen_yabanci_ziyaretci, engine
from datetime import datetime
from sqlalchemy.exc import IntegrityError

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
    #print(pdf_links)
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
    print(month_numbers)
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

def check_month_and_year_exists(session, month, year):
    exists = (
        session.query(gelen_yabanci_ziyaretci)
        .filter(
            extract('month', gelen_yabanci_ziyaretci.tarih) == month,
            extract('year', gelen_yabanci_ziyaretci.tarih == year)
        )
        .first()
    )
    return exists is not None

def read_pdf_from_url(href, base_url):
    """
    Reads the PDF content from the given href and extracts the first row containing the target month.
    """
    full_url = urljoin(base_url, href)
    response = requests.get(full_url, verify=False)

    if response.status_code == 200:
        pdf_content = BytesIO(response.content)
        output = []
        
        with pdfplumber.open(pdf_content) as pdf:
            # Extract year from the 3rd page
            year = get_year_from_page(pdf, page_number=3)
            #print(year)
            if not year:
                print("Year not found on the specified page.")
                return
            
            latest_month = find_newest_month_html(pdf)
            if not latest_month:
                print("Could not find the latest month in the PDF.")
                return
            
            for month_num in range(latest_month, 0, -1):  # Start from the latest month
                month_name = months_mapping[month_num].upper()
                month_found = False

                for page in pdf.pages:
                    table_one_txt = page.extract_text_simple()
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
    df = pd.DataFrame(output,  columns=["tarih", "ist_tr", "ziyaretci_sayisi"])
    return df

def save_to_database(df, session):
    for _, row in df.iterrows():
        new_record = gelen_yabanci_ziyaretci(
            tarih = row["tarih"],
            ist_tr = str(row["ist_tr"]),
            ziyaretci_sayisi = float(row["ziyaretci_sayisi"]),
            erisim_tarihi = datetime.today().strftime("%Y-%m-%d")
        )
        try:
            session.add(new_record)
            session.commit()
        except IntegrityError:
            session.rollback()
    print("Data added to the database.")

def generate_date_prefix(year, month):
    """
    Creates a date prefix in the format YYYY-MM-01.
    """
    return f"{year}-{month:02d}-01"

def extract_year_month(date_info):
    months_mapping = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran", 
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
    }
    parts = date_info.split()
    year = parts[0]
    month_text = parts[1]
    month = months_mapping.get(month_text, "00")

    return f"{year}-{month}-01"


def main_02_01():
    # Main script execution
    
    Session = sessionmaker(bind=engine)
    session = Session

    disable_ssl_warnings()

    url = "https://istanbul.ktb.gov.tr/TR-368430/istanbul-turizm-istatistikleri---2024.html"
    base_url = "https://istanbul.ktb.gov.tr"

    html_content = fetch_page_content(url)
    if not html_content:
        print(f"PDF file could not be downloaded: {url}")
        return
    href = parse_pdf_links(html_content)
    newest_month = find_newest_month_html(html_content)

    # Read the PDF and extract year and month
    df = read_pdf_from_url(href, base_url)
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            parsed_date = datetime.strptime(row["tarih"], "%Y-%m-%d")
            year = parsed_date.year
            month = parsed_date.month

            # Generate date_prefix
            date_prefix = generate_date_prefix(year, month)

            # Check if data for this date_prefix exists in the database
            if check_month_and_year_exists(session, month, year):
                print(f"Record already exists for {date_prefix}. Skipping...")
            else:
                # Save the data to the database
                print(f"New data found for {date_prefix}, adding to database...")
                save_to_database(df, session)
    else:
        print("No data extracted from the PDF.")
    session.close()

main_02_01()