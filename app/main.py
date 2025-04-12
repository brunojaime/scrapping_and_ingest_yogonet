from scrapper import scrape_yogonet
from processor import data_processing
if __name__== "__main__":
    data = scrape_yogonet()
    data_processing(data)
    