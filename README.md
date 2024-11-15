# KTB Monthly Scraper

- This project extracts monthly tourism statistics for Türkiye and Istanbul from a PDF available on a specified webpage. 
- The extracted data is structured and ready for further analysis or storage in a database.

## Features

- Web scraping: Automatically fetches the latest PDF from the specified website.
- PDF processing: Extracts relevant data (date, location, and visitor count) from the PDF.
- Data structuring: Outputs the extracted information in a structured format as a `pandas.DataFrame`.

## Requirements
- Install the dependencies using:
```bash
pip install -r requirements.txt
```

## Usage
- Run the script: Execute the main_check() function to process the latest available data.
- Output: The script outputs a structured DataFrame with the following columns:
    - tarih (Date)
    - ist_tr (Location: "Türkiye" or "İstanbul")
    - ziyaretci_sayisi (Visitor Count)


## Error Handling

- If you wish to install a Python library that isn't in Homebrew,

    - Use a Virtual Environment: Using a virtual environment allows you to manage your Python packages independently of the system-wide Python installation. Here’s how to create and activate a virtual environment:
```bash
python3.13 -m venv venv 
# Here the path to venv is /Users/user_name/your_folder/ktb-monthly-scraper/venv
```
```bash
source /Users/user_name/your_folder/ktb-monthly-scraper/venv/bin/activate
```
```bash
python3 -m pip install xyz
```







