import requests
import re
from bs4 import BeautifulSoup
import sqlite3

page = None
url = f'https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/{page}'


def get_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")

    elements = soup.find_all('div', class_='linked-film-poster')

    links = []

    for element in elements:
        href = f"https://letterboxd.com{element['data-target-link']}"

        if not href:
            continue

        links.append(href)

    return links


def get_films(urls):
    if urls is None:
        return

    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features="html.parser")

        content = soup.find('div', id="content")

        main_content = content.find('div', {'class': 'col-17'})

        # TITLES
        en_title = main_content.find('h1', {'class': 'headline-1'}).text
        print(en_title)

        try:
            title = main_content.find('em').text
            print(title)
        except AttributeError:
            print('Title Originally in English')
            continue

        # RELEASE YEAR
        year = main_content.find('small', {'class': 'number'}).find('a').text
        print(year)

        # DIRECTOR
        director = main_content.find('span', {'class': 'prettify'}).text
        print(director)

        # CAST
        cast_details = main_content.find('div', id='tab-cast')
        cast = cast_details.find('div', {'class': 'cast-list'}).find_all('a', {'class': 'text-slug'})
        for member in cast[:5]:
            try:
                actor = member.text
                character = member['title']
            except KeyError:
                print('Missing character name')
            print(actor, character)

        # POPULAR REVIEWS
        popular_reviews = main_content.find('section', class_='film-recent-reviews')
        if len(popular_reviews) > 0:
            print(popular_reviews)


# Define the range of pages to scrape
for page in range(1, 3):
    url = f'https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/page/{page}/'
    links = get_links(url)
    get_films(links)
