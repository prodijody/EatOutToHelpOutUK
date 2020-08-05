import requests
import html
import csv
import re
import os
import pandas as pd 
from bs4 import BeautifulSoup

regex_postcode = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})"
path = os.getcwd()
postcode_path = os.path.join(path, "postcodes")
new_postcode_path = os.path.join(path, "new_postcodes")

def correct_postcode(postcode):
    # returns a cleaned valid postcode if matches regex otherwise returns invalid
    postcode = postcode.replace(" ", "")
    if re.match(regex_postcode, postcode):
        postcode = f"{postcode[:-3]} {postcode[-3:]}".upper()
        return postcode
    else:
        return "Invalid"
#df = pd.DataFrame(columns=['Name','Address'])

def find_a_restaurant(postcode):
    restaurant_list = []
    restaurant_dict = {}
    # The list of registered restaurants within 5 miles of the specified postcode will be obtained from the government website.
    url = f"https://www.tax.service.gov.uk/eat-out-to-help-out/find-a-restaurant/results?postcode={postcode}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.findAll("li", {"class": "govuk-results-list-item"})
    for result in results:
        name = result.findAll("h3", {"class": "govuk-heading-m"})[0].contents[0]
        address = result.findAll("p", {"class": "govuk-results-address govuk-body"})[
            0
        ].contents[0]
        restaurant_dict[address] = name
    return restaurant_dict


def load_and_sort_postcodes(postcode_file):
    filename = os.path.join(postcode_path, postcode_file)
    postcode_dict = {}
    postcode_list = []
    file = open(filename, "r")
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        postcode = correct_postcode(row[0])
        split = postcode.split()
        if split[0] not in postcode_dict:
            postcode_dict[split[0]] = split[1]
    for key, item in postcode_dict.items():
        postcode_list.append(f"{key} {item}")
    output_filename = os.path.join(new_postcode_path, postcode_file)
    with open(output_filename, 'w') as f:
        for item in postcode_list:
            f.write("%s\n" % item)      


def load_and_get_restaurants(postcode_file):
    rest_dict = {}
    with open(postcode_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            postcode = row[0]
            for x,y in find_a_restaurant(postcode).items():
                rest_dict[x] = y
    rest_dict_inv = {v: k for k, v in rest_dict.items()}
    df = pd.Series(rest_dict_inv, name='Address')
    df.index.name = 'Name'
    df.reset_index()
    df.to_csv("aberdeen.csv", sep=',', encoding='utf-8')

if __name__ == "__main__":
    """
    postcode_files = os.listdir(postcode_path)
    for postcode_file in postcode_files:
        load_and_sort_postcodes(postcode_file)
    """

    postcode_files = os.listdir(new_postcode_path)
    for postcode_file in postcode_files:
        load_and_get_restaurants(os.path.join(new_postcode_path, postcode_file))
        break

    #find_a_restaurant("ky1 1jn")