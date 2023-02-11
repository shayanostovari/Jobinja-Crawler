import json
from abc import ABC

import convert_numbers
import requests
from bs4 import BeautifulSoup

from parser import AdvertisementsParser
from utils import adv_count_selector, base_url, request_header


class CrawlerBase(ABC):
    @staticmethod
    def archive(data, file_name):
        with open(f'store/{file_name}.json', 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def read_file(file_name):
        with open(f'store/{file_name}.json', 'r') as f:
            return json.loads(f.read())


class GetUserData:
    @staticmethod
    def get_user_data():
        keyword = input('Please Enter Your Keyword: ')
        city = input('Please Enter Your City (FARSI) :  ')
        user_data = {'keyword': keyword, 'city': city}
        return user_data


class GetAdvLinks(CrawlerBase):
    def __init__(self):
        self.user_data = GetUserData.get_user_data()
        self.page_count = self.pages_count()
        self.data_list = list()

    def pages_count(self):
        url = base_url.format(self.user_data['keyword'], self.user_data['city'], 1)
        response = requests.get(url, headers=request_header)
        soup = BeautifulSoup(response.text, 'html.parser')
        num = soup.select_one(adv_count_selector).text.split()
        persian_number = num[0]
        english_number = int(convert_numbers.persian_to_english(persian_number))
        pages_count = english_number // 20
        pages_count = pages_count + 1
        return pages_count

    def crawl_page(self):
        counter = 0
        while counter <= self.page_count:
            counter += 1
            url = base_url.format(self.user_data['keyword'], self.user_data['city'], counter)
            response = requests.get(url, headers=request_header)
            self.advertisements_links(response)

    def advertisements_links(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for li in soup.find_all('a', attrs={'class': 'c-jobListView__titleLink'}):
            print(li)
            self.data_list.append(li.get('href'))
        self.archive(data=self.data_list, file_name='adv_links')


class DataCrawler(CrawlerBase):
    def __init__(self):
        self.adv_links = self.__load_links()
        self.parser = AdvertisementsParser()
        self.parsed_data = list()

    def __load_links(self):
        links = self.read_file(file_name='adv_links')
        return links

    def start(self):
        for link in self.adv_links:
            response = requests.get(link, headers=request_header)
            data = self.parser.parse(response)
            self.parsed_data.append(data)
            self.archive(data=self.parsed_data, file_name='parsed_data')
            print(data)
