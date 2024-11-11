# BUILD-F README
## `main_all_months_scraper.py``

### Overview
This Python script retrieves and parses monthly tourism statistics in PDF format from a specified website. It is designed to:

- Identify the latest PDF file available on the site.
- Extract monthly data from the PDF, including values for "Türkiye" and "İstanbul" tourism statistics.
- Display the extracted data in a date-formatted output.

The script uses `requests` for web scraping, `BeautifulSoup` for parsing HTML, and `pdfplumber` for processing PDF files.

### Requirements
To run this script, you need to install the following Python libraries:

- `requests`: For making HTTP requests.
- `urllib3`: For managing SSL warnings.
- `beautifulsoup4`: For parsing HTML.
- `pdfplumber`: For extracting text from PDF files.

Install these dependencies with:

```bash
pip install requests urllib3 beautifulsoup4 pdfplumber
```

### How It Works
#### Main Functions
1. disable_ssl_warnings()
- Disables SSL warnings for smoother HTTP requests.

2. fetch_page_content(url)
- Retrieves the HTML content of a given URL. Returns None if the page request fails.

3. parse_pdf_links(html_content)
- Extracts all .pdf links from the HTML content and returns the most recent PDF link.

4. extract_month_number(month_string)
- Parses a month name from a string and returns the corresponding month number (e.g., "TEMMUZ" -> 7).

5. find_newest_month_html(html_content)
- Scans HTML content for month information in PDF links, then returns the most recent month number available.

6. get_year_from_page(pdf, page_number)

- Reads the specified page of a PDF to find the year in a line beginning with "AYLAR". Assumes that the year is found in the third-to-last word of this line.

7. read_pdf_from_url(href, base_url, latest_month)

- Processes the PDF to extract monthly statistics starting from the latest month back to January.
- For each month, it identifies the correct line and extracts Türkiye and İstanbul values from specific positions, printing them in YYYY-MM-01 format.

#### Script Execution

The script:

1. Fetches HTML from the target URL (url).
2. Parses the HTML to find the most recent PDF link and determine the latest available month.
3. Reads the PDF, extracting monthly data by parsing lines containing each month’s name.
4. Prints extracted data or logs messages if data cannot be found.

#### Usage
To run the script:
```bash
python3 main_all_months_scraper.py
```

Expected Output
For each month in the PDF, the script will output lines like:

```bash
2024-07-01 Türkiye 2,500,000
2024-07-01 İstanbul 1,200,000
```

#### Error Handling
- If a PDF or HTML page cannot be retrieved, or if data is missing from an expected position, the script will print error messages.
- If a month is not found in the PDF, the script will log a message indicating the missing data.

#### Notes
- The script is designed for a specific PDF structure. If the structure changes (e.g., different line formats), adjustments to line parsing may be required.
- For optimal results, ensure the PDF source URL is reliable and up-to-date.