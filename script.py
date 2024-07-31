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


def parse_html(url: str) -> bs4.BeautifulSoup:
    """Fetches and parses HTML content from the given URL."""
    soup = bs(get(url).text, "html.parser")
    return soup


def get_links(soup: bs4.BeautifulSoup) -> list[str]:
    """Extracts and returns links from 'td' elements with class 'cislo'."""
    base_url = "https://volby.cz/pls/ps2017nss/"
    links = []
    for item in soup.find_all("td", {"class": "cislo"}):
        for tag in item:
            links.append(urljoin(base_url, tag["href"]))
    return links


def get_data(soup: bs4.BeautifulSoup, header_list: list[str]) -> list[str]:
    """Extracts data from 'td' elements based on provided headers."""
    data = []
    for header in header_list:
        for item in soup.find_all("td", {"headers": header}):
            value = item.get_text().strip()
            if value != "-":
                data.append(value)
    return data


def main_function():
    """Main function to scrape data and save it to a CSV file."""

    print("scraping data...")

    headers = {
        "codes": ["t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1"],
        "locations": ["t1sa1 t1sb2", "t2sa1 t2sb2", "t3sa1 t3sb2"],
        "counts": ["sa2", "sa5", "sa6", "t1sa2 t1sb3", "t2sa2 t2sb3"],
        "titles": ["t1sa1 t1sb2", "t2sa1 t2sb2"]
    }
    first_page_soup = parse_html(sys.argv[1])
    links = list(get_links(first_page_soup))
    codes = list(get_data(first_page_soup, headers["codes"]))
    locations = list(get_data(first_page_soup, headers["locations"]))
    data = [get_data(parse_html(url), headers["counts"]) for url in links]

    base_titles = ["codes", "locations", "registered", "envelopes", "valid"]
    aditional_titles = get_data(parse_html(links[0]), headers["titles"])
    titles = base_titles + aditional_titles
    
    combined_data = []
    for column_1, column_2, row in zip(codes, locations, data):
        combined_data.append([column_1, column_2] + row)

    print("creating csv file")
    with open(sys.argv[2], mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(titles)
        writer.writerows(combined_data)
    print("csv file has been created successfully")


if len(sys.argv) != 3:
    print(
        "enter: python script.py 'http link' 'file_name.csv'", sep="\n"
    )
    sys.exit(1)
elif not sys.argv[1].startswith("https"):
    print(
        "first argv must be http link"
    )
    sys.exit(1)
elif "https://volby.cz/pls/ps2017nss/" not in sys.argv[1]:
    print(
        "https adress not valid.."
    )
elif ".csv" not in sys.argv[2]:
    print(
        "second argv must contain file extension '.csv'"
    )
    sys.exit(1)
else:
    print(
        "opening Election scraper.."
    )


if __name__ == "__main__":
    main_function()      
