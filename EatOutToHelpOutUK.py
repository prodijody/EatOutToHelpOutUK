import requests
import html
import csv
import re
from bs4 import BeautifulSoup

regex_postcode = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})"

def correct_postcode(postcode):
    # returns a cleaned valid postcode if matches regex otherwise returns invalid
    postcode = postcode.replace(" ", "")
    if re.match(regex_postcode, postcode):
        postcode = f"{postcode[:-3]} {postcode[-3:]}".upper()
        return postcode
    else:
        return "Invalid"


def find_a_restaurant(postcode):
    # The list of registered restaurants within 5 miles of the specified postcode will be obtained from the government website.
    url = f"https://www.tax.service.gov.uk/eat-out-to-help-out/find-a-restaurant/results?postcode={postcode}"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.findAll("li", {"class": "govuk-results-list-item"})
    for result in results:
        name = result.findAll("h3", {"class": "govuk-heading-m"})[0].contents[0]
        address = result.findAll("p", {"class": "govuk-results-address govuk-body"})[0].contents[0]
        print(f"{name}: {address}")
        

if __name__ == "__main__":
    postcode = str(input())
    postcode = correct_postcode(postcode)
    find_a_restaurant(postcode)