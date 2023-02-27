import json
import requests
import pprint
import smtplib
import re
from time import sleep
from email.message import EmailMessage
from string import Template
from datetime import datetime


# Url and key
api = "0195e7cdbe9b41248a3f6749e731ea59"
url = 'https://newsapi.org'
endpoint = '/v2/everything'

countries_dict = ["ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz", "de", "eg", "fr", "gb",
                  "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma", "mx", "my", "ng",
                  "nl", "no", "nz", "ph", "pl", "pt", "ro", "rs", "ru",
                  "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us", "ve", "za"]

languages_dict = ["ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"]

# User meniu
user_choices = """1 - search news with keyword, 2 - search news with keyword in title, 3 - searh by category and language
               4 - search by country news, 5 - show news by sort, 6 - send email with newest news\n"""


def search_key(key):
    payload = {'apiKey': '0195e7cdbe9b41248a3f6749e731ea59',
               'q': key}
    response = requests.get(url + endpoint, params=payload)
    res = json.loads(response.text)
    pprint.pprint(res)


def search_title(tit):
    payload = {'apiKey': '0195e7cdbe9b41248a3f6749e731ea59',
               'qInTitle': tit}
    response = requests.get(url + endpoint, params=payload)
    res = json.loads(response.text)
    pprint.pprint(res)


def search_by_cat_lang(cat, lan):
    endpoint1 = "/v2/top-headlines/sources"
    pay = {'apiKey': '0195e7cdbe9b41248a3f6749e731ea59',
           "category": cat,
           "language": lan}
    r = requests.get(url + endpoint1, params=pay)
    res = json.loads(r.text)  # pakeisti json į žodyno formatą
    pprint.pprint(res)


def search_country_news(country):
    endpoint1 = "/v2/top-headlines/sources"
    payload = {'apiKey': '0195e7cdbe9b41248a3f6749e731ea59',
               "country": country}
    response = requests.get(url + endpoint1, params=payload)
    res = json.loads(response.text)
    pprint.pprint(res)


def sort_news(new):
    endpoint1 = "/v2/top-headlines/sources"
    payload = {'apiKey': '0195e7cdbe9b41248a3f6749e731ea59',
               "sortBy": new}
    response = requests.get(url + endpoint1, params=payload)
    res = json.loads(response.text)
    pprint.pprint(res)


SMTP_SERVER = "karatyse23.smshostingas.lt"
USERNAME = "katyse@karatyse23.smshostingas.lt"
PASSWORD = "3ArrZevPP"


def send_emails(subject, to, name, naujienos):
    sleep(0.2)
    with open("newsselter.html", "r", encoding="UTF-8") as f:
        html = f.read()

    email = EmailMessage()
    email["from"] = f"NEWS <{USERNAME}>"
    email["to"] = to
    email["cc"] = "klubas@karatyse23.smshostingas.lt"
    email["subject"] = subject

    template = Template(html)
    personalize_content = template.substitute({"name": name,
                                               "naujienos": naujienos,
                                               "time": datetime.now()})
    email.set_content(personalize_content, "html")

    with smtplib.SMTP(host=SMTP_SERVER, port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(USERNAME, PASSWORD)
        smtp.send_message(email)


def naujienos(key, pg, nm, ma):
    payload = {'apiKey': '0195e7cdbe9b41248a3f6749e731ea59',
               "q": key,
               "pageSize": pg}
    response = requests.get(url + endpoint, params=payload)
    res = json.loads(response.text)
    pprint.pprint(res)
    return send_emails(f"Hello {nm} Latest news from {key}", to=ma, name=nm, naujienos=res['articles'])


def validate_email(email_adres):
    pattern = r"^[0-9a-z._-]+@[0-9a-z._-]+\.[a-z]{2,6}$"
    result = re.search(pattern, email_adres.lower())
    if result:
        return True
    else:
        return False


while True:
    choices = input(user_choices)
    if choices == "":
        break

    elif choices == "1":
        search = input("Enter a keyword with you want to search: ")
        search_key(search)

    elif choices == "2":
        title = input("Enter a title keywords: ")
        search_key(title)

    elif choices == "3":
        print(f"Enter lang from this list: {languages_dict}")
        categor_s = input(
            "Enter a category wich you want to search, business, entertainment, general, health, science, sports, or technology: ")
        lang = input("Enter a language wich you want to search eg, en: ")
        search_by_cat_lang(categor_s, lang)

    elif choices == "4":
        print(f"Countries codes: {countries_dict}")
        country_search = input("Enter a country ISO code, eg, en: ")
        search_country_news(country_search)

    elif choices == "5":
        sort = input("Enter a keyword what do you want to sort popularity, publishedAt or relevancy: ")
        sort_news(sort)
    elif choices == "6":
        search_by = input("Enter a  keyword wich you want to get email: ")
        pages = input("Enter a page size, how much pages do you want to see from 1 to 100: ")

        #  email siuntimas su naujienlaiskiu
        name = input("Enter a name: ")
        while True:
            mail = input("Enter a email eg., example@example.com: ")
            validate_email(mail)
            email_check = validate_email(mail)

            if not email_check:
                print("Email address format not valid, enter valid email!!!")
                continue
            break
        naujienos(search_by, pages, name, mail)

    else:
        print("This choice not found!!")
        break