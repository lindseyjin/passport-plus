from bs4 import BeautifulSoup
import requests
from config import *


def scrape_exchange_data():
    exchange_data = [
    ]

    with requests.Session() as session:
        # header variable
        session.headers = {'User-Agent': USER_AGENT}

        # initial get request
        session.get(BASE_URL + "?s=programs")

        # get all items
        req = session.get(BASE_URL + "?_so_list_aat5ad5a89179cb63f89c2de5a1bb7ce758=250")
        soup = BeautifulSoup(req.text, "html.parser")

        # get relevant containers
        program_info = soup.find_all('td', class_=PROGRAM_INFO)
        host_info = soup.find_all('td', class_=HOST_INST)
        languages = soup.find_all('td', class_=LANGUAGE)
        terms = soup.find_all('td', class_=TERMS)

        # # add last element, which has different tags
        # TODO: CHECK IF TAG EXISTS
        program_info.append(soup.find('td', class_=PROGRAM_INFO_LAST))
        host_info.append(soup.find('td', class_=HOST_INST_LAST))
        languages.append(soup.find('td', class_=LANGUAGE_LAST))
        terms.append(soup.find('td', class_=TERMS_LAST))

        for x in range(0, len(program_info)):
            exchange_data.append({'program': '', 'link': '', 'host': '', 'location': '', 'languages': '', 'terms': []})
            if program_info[x].div.a:
                exchange_data[x]['program'] = program_info[x].div.a.text
                exchange_data[x]['link'] = BASE_URL + program_info[x].div.a['href']
            if program_info[x].div.i:
                exchange_data[x]['location'] = program_info[x].div.i.text
            if host_info[x].div:
                exchange_data[x]['host'] = host_info[x].div.text
            if languages[x].div:
                exchange_data[x]['languages'] = languages[x].div.text
            for term in terms[x].div:
                exchange_data[x]['terms'].append(term.text)

        return exchange_data


if __name__ == "__main__":
    print(scrape())
