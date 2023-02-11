from crawler import GetAdvLinks, DataCrawler

if __name__ == "__main__":

    find_link = GetAdvLinks()
    find_link.crawl_page()

    parse_data = DataCrawler()
    parse_data.start()
