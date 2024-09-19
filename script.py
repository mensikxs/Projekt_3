"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Simona Menšíková
email: mensikxs@gmail.com
discord: mensikxs@gmail.com
"""

import sys
import csv
from requests import get
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs


def parse_html(url: str) -> bs:
    """Fetch and pars HTML content from a given URL."""
    soup = bs(get(url).text, "html.parser")
    return soup


def get_links(soup: bs) -> list[str]:
    """Get list of links from 'td' elements with class 'cislo'."""
    base_url = "https://volby.cz/pls/ps2017nss/"
    links = []
    for item in soup.find_all("td", {"class": "cislo"}):
        for tag in item:
            links.append(urljoin(base_url, tag["href"]))
    return links


def get_data(soup: bs, header_list: list[str]) -> list[str]:
    """Extract data from 'td' elements by headers."""
    data = []
    for header in header_list:
        for item in soup.find_all("td", {"headers": header}):
            value = item.get_text().strip()
            if value != "-":
                data.append(value)
    return data


def get_headers() -> dict:
    """Return headers for scraping."""
    return {
        "codes": ["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"],
        "locations": ["t1sa1 t1sb2", "t2sa1 t2sb2", "t3sa1 t3sb2"],
        "counts": ["sa2", "sa5", "sa6", "t1sa2 t1sb3", "t2sa2 t2sb3"],
        "titles": ["t1sa1 t1sb2", "t2sa1 t2sb2"]
    }


def scrape_main_data(soup: bs, headers: dict) -> dict:
    """Scrape main data: links, codes, locations, and counts."""
    links = get_links(soup)
    codes = get_data(soup, headers["codes"])
    locations = get_data(soup, headers["locations"])
    data = [get_data(parse_html(url), headers["counts"]) for url in links]
    return {
        "links": links,
        "codes": codes,
        "locations": locations,
        "rows": data
    }


def prepare_titles(links: list[str], headers: dict) -> list[str]:
    """Prepare titles (headers) for the CSV file."""
    base_titles = ["codes", "locations", "registered", "envelopes", "valid"]
    additional_titles = get_data(parse_html(links[0]), headers["titles"])
    return base_titles + additional_titles


def combine_data(
        codes: list[str],
        locations: list[str],
        data: list[list[str]]
 ) -> list[list[str]]:
    """Combine codes, locations, and data into a single list."""
    combined_data = []
    for code, location, row in zip(codes, locations, data):
        combined_data.append([code, location] + row)
    return combined_data


def save_to_csv(
        file_name: str,
        titles: list[str],
        combined_data: list[list[str]]
) -> None:
    """Save data to a CSV file."""
    print("creating csv file")
    with open(file_name, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(titles)
        writer.writerows(combined_data)
    print("CSV file created successfully.")


def validate_input_args():
    """Validate script arguments."""
    if len(sys.argv) != 3:
        print("Enter: python script.py 'http link' 'file_name.csv'")
        sys.exit(1)
    elif not sys.argv[1].startswith("https"):
        print("First argument must be a valid HTTP link.")
        sys.exit(1)
    elif "https://volby.cz/pls/ps2017nss/" not in sys.argv[1]:
        print("Invalid URL.")
        sys.exit(1)
    elif not sys.argv[2].endswith(".csv"):
        print("Second argument must be a CSV file name with '.csv' extension.")
        sys.exit(1)
    else:
        print("Opening Election scraper...")


def main_function():
    """Main function to run the scraping and CSV file generation."""
    validate_input_args()
    print("Scraping data...")
    headers = get_headers()
    first_page_soup = parse_html(sys.argv[1])
    data = scrape_main_data(first_page_soup, headers)
    titles = prepare_titles(data["links"], headers)
    combined_data = combine_data(data["codes"], data["locations"], data["rows"])
    save_to_csv(sys.argv[2], titles, combined_data)


if __name__ == "__main__":
    main_function()
