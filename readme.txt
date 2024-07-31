# Election Data Scraper

This script is designed to scrape election data from a specified webpage related to a particular "okres" (district) 
and gather detailed results from linked "obec" (municipality) pages. 
It compiles the data into a CSV file with relevant election information.

## Description

The script performs the following tasks:
1. **Fetches** the main election results page for a specific "okres" and extracts links to detailed results pages for each "obec".
2. **Scrapes** specific election data, such as codes and locations, from the "okres" page and detailed statistics from each linked "obec" page.
3. **Combines** the data into a structured format.
4. **Exports** the consolidated data into a CSV file with appropriate headers.

### Context

The script allows you to select any territorial unit from the main page of election results (https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). 
Selecting a district ("X" in column "Výběr obce") directs you to a page with detailed results. From this page, the script scrapes the voting results for all 
municipalities using links found in the selection column. Each "X" in the "Výběr okrsku" column links to detailed results for a particular "obec".

## Installation

Before running the script, ensure you have the following Python libraries installed:

- requests
- beautifulsoup4

### Usage
To run the script, use the command line with two arguments:

python script.py "<okres_page_url>" "<output_csv_file>"

<okres_page_url>: The URL of the main election results page for a specific "okres" (district).
<output_csv_file>: The name of the CSV file where the election data will be saved.
The script uses sys.argv to accept these two arguments, ensuring that the URL of the "okres" page and the output CSV file name are provided.

#### Example

python script.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "election_results.csv"

This command will scrape election data from the given "okres" URL and save the results in election_results.csv.

##### Notes

The script assumes the webpage has a specific HTML structure that includes class names and table headers matching the Czech election website. 
Adjustments may be necessary if the page structure changes.
Ensure the URLs are correctly formatted and accessible.
