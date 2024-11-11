 # README for KTB Scraper Scripts (Pre-Build Scripts)

This repository contains three Python scripts designed to scrape tourism statistics data from the Istanbul Provincial Directorate of Culture and Tourism website. These scripts fetch PDF files from the website, process them, and extract specific data for further analysis.

## Overview of Scripts

### 1. `main_ktb_scraper.py`
- **Purpose**: Downloads the most recent PDF file containing tourism statistics.
- **Functionality**:
  - Connects to the target website and retrieves HTML content.
  - Parses the HTML to locate PDF links.
  - Identifies the most recent PDF file based on month information in the link.
  - Downloads the PDF file and saves it locally.
- **Differences**: Focuses solely on downloading PDF files without extracting or analyzing the contents of the PDFs.

### 2. `main_ktb_scraper_.py`
- **Purpose**: Downloads the most recent PDF file and reads its content.
- **Functionality**:
  - Performs similar steps to `main_ktb_scraper.py` for downloading the latest PDF.
  - Reads and prints the contents of the PDF directly using the `pdfplumber` library.
  - Extracts specific text from a designated page (page 3) and displays it.
- **Differences**: This script goes beyond downloading by directly reading and displaying PDF content, which is useful for quick data previews.

### 3. `new_month_scraper.py`
- **Purpose**: Extracts specific month-related data from a PDF and verifies the year.
- **Functionality**:
  - Identifies and downloads the most recent PDF.
  - Extracts the publication year from a specific page (page 3) of the PDF.
  - Searches for a particular month in the PDF content and prints the relevant row.
- **Differences**: Adds advanced functionality by verifying the year and filtering rows based on the target month. This is ideal for monthly data extraction with additional accuracy.

4. `main_all_months_scraper.py`

**Purpose**: 
Downloads the most recent PDF file containing tourism statistics from the specified URL and extracts monthly data for "Türkiye" and "İstanbul."

**Functionality**:
- Connects to the target website and retrieves HTML content.
- Parses the HTML to locate PDF links.
- Identifies the most recent PDF file based on month information within the link.
- Downloads the PDF file and analyzes it to extract monthly data.
- Reads each page in the PDF to find and display tourism statistics for "Türkiye" and "İstanbul" for each month, starting from the latest month and working backward to January.

**Differences**:
Unlike a simple PDF downloader, this script:
- Analyzes the content of the PDF to extract specific tourism data by month.
- Extracts and displays tourism data for "Türkiye" and "İstanbul" directly from the file, allowing for targeted data analysis.

## Usage Notes

- **SSL Verification**: All scripts include a function to disable SSL verification, which helps bypass security warnings for websites with unverified certificates.
- **Dependencies**: Required packages include `requests`, `beautifulsoup4`, `pandas`, `pdfplumber`, and `urllib3`. Ensure all dependencies are installed before running the scripts.
- **Customization**: Update the URL in each script to match the current structure of the Istanbul Provincial Directorate of Culture and Tourism website if it changes.

These scripts collectively offer a streamlined workflow for accessing, downloading, and processing tourism data in PDF format. Choose the appropriate script based on whether you need to download only, preview data, or conduct detailed monthly analyses.
