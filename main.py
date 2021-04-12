import csv

import requests
from bs4 import BeautifulSoup

CSV = "companies_mail.csv"
HOST = "https://www.b2b.by/"
URL = "https://www.b2b.by/mezhdunarodnye-avtomobilnye-gruzoperevozki-TL401/companies/"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}


def get_html(url, params=""):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="for-show-all-goods-main-page")
    companies = []

    for item in items:
        try:
            companies.append(
                {
                    "company": item.find("span",
                                         class_="company-center").find("a").get_text(strip=True),

                    "email": item.find("div",
                                       class_="company-center-email").find("a").get_text(strip=True)
                }
            )
        except AttributeError:
            continue

    return companies


def save_doc(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Company", "Email"])
        for item in items:
            writer.writerow([item["company"], item["email"]])


def parser():
    PAGENATION = input("how much pages: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        companies = []
        for page in range(1, PAGENATION + 1):
            print(f"process: {page}")
            html = get_html(URL, params={"page": page})
            companies.extend(get_content(html.text))
        save_doc(companies, CSV)
    else:
        print("Error")


if __name__ == "__main__":
    parser()
