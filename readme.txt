# Web Scraper to CSV

This script scrapes data from a specified web page, extracts relevant information, and saves it into a CSV file. 
The script handles multiple tables on the page, processes data from linked pages, 
and consolidates everything into a single CSV file.

## Description

The script performs the following tasks:
1. **Fetches** the main page and extracts links from it.
2. **Scrapes** specific data from the main page and linked pages.
3. **Combines** the data from the main page and the linked pages.
4. **Writes** the combined data into a CSV file with headers.

## Installation

Before running the script, ensure you have the following Python libraries installed:

- `requests`
- `beautifulsoup4`

You can install these libraries using pip:

```bash
pip install requests beautifulsoup4

Usage
To run the script, use the command line with the following arguments:
python script.py <main_page_url> <output_csv_file>
<main_page_url>: The URL of the page to scrape.
<output_csv_file>: The name of the CSV file where the data will be saved.

Example
python script.py "https://example.com/main-page" "output.csv"
This command will scrape data from the given URL and save the results in output.csv.

Notes
Ensure the URLs and the structure of the page you are scraping match the expectations of the script.
The script assumes the presence of specific HTML structure and class names, which may vary depending on the actual web page.
