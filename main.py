from crawler import GetAdvLinks, DataCrawler
from threading import Thread

def crawl_links():
    find_link = GetAdvLinks()

    threads = [Thread(target=find_link.advertisements_links, args=(page_number,))
               for page_number in range(1, find_link.page_count+1)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    find_link.save_links()

def data_parser():
    data_crawler = DataCrawler()
    links = data_crawler.adv_links
    num_threads = 10
    links_per_thread = len(links) // num_threads

    threads = []
    for i in range(num_threads):
        start_index = i * links_per_thread
        end_index = len(links) if i == num_threads - 1 else start_index + links_per_thread
        links_subset = links[start_index:end_index]

        t = Thread(target=data_crawler.start, args=(links_subset,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    data_crawler.save_data()

if __name__ == "__main__":
    crawl_links()
    data_parser()
