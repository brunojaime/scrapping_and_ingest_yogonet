from scrapper import scrape_yogonet
from processor import data_processing
from big_quer_client import upload_to_bigquery


if __name__== "__main__":
    data = scrape_yogonet(url="https://www.yogonet.com/latinoamerica/")
    df =  data_processing(data)
    upload_to_bigquery(df)
    

    