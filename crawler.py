import json
import requests
from bs4 import BeautifulSoup
from parser import AdvertisementsParser
from utils import adv_count_selector, base_url, request_header
import queue
import convert_numbers

class CrawlerBase:
    @staticmethod
    def archive(data, file_name):
        with open(f'store/{file_name}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def read_file(file_name):
        with open(f'store/{file_name}.json', 'r') as f:
            return json.load(f)

class GetUserData:
    @staticmethod
    def get_user_data():
        keyword = input('Please Enter Your Keyword: ')
        city = input('Please Enter Your City (FARSI): ')
        return {'keyword': keyword, 'city': city}

class GetAdvLinks(CrawlerBase):
    def __init__(self):
        self.user_data = GetUserData.get_user_data()
        self.page_count = self.pages_count()
        self.data_queue = queue.Queue()

    def pages_count(self):
        url = base_url.format(self.user_data['keyword'], self.user_data['city'], 1)
        response = requests.get(url, headers=request_header)
        soup = BeautifulSoup(response.text, 'html.parser')
        num = soup.select_one(adv_count_selector).text.split()[0]
        english_number = int(convert_numbers.persian_to_english(num))
        return (english_number // 20) + 1

    def crawl_page(self, page_number):
        url = base_url.format(self.user_data['keyword'], self.user_data['city'], page_number)
        return requests.get(url, headers=request_header)

    def advertisements_links(self, page_number):
        response = self.crawl_page(page_number)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [li.get('href') for li in soup.find_all('a', attrs={'class': 'c-jobListView__titleLink'})]
        for link in links:
            print(link)
            self.data_queue.put(link)

    def save_links(self):
        links = []
        while not self.data_queue.empty():
            links.append(self.data_queue.get())
        self.archive(data=links, file_name='adv_links')

class DataCrawler(CrawlerBase):
    def __init__(self):
        self.adv_links = self.read_file('adv_links')
        self.parser = AdvertisementsParser()
        self.parsed_data = queue.Queue()

    def start(self, links_subset):
        for link in links_subset:
            response = requests.get(link, headers=request_header)
            data = self.parser.parse(response)
            self.parsed_data.put(data)
            print(data)

    def save_data(self):
        data_list = []
        while not self.parsed_data.empty():
            data_list.append(self.parsed_data.get())
        self.archive(data=data_list, file_name='parsed_data')
