# Import main functions from respective modules
from scrapper import scrape_yogonet             # Web scraping function
from processor import data_processing           # Data cleaning/transformation
from big_quer_client import upload_to_bigquery  # BigQuery upload function

if __name__ == "__main__":
    # Scrape news data from Yogonet's international section
    data = scrape_yogonet(url="https://www.yogonet.com/international/")
    
    # Print raw scraped data for debugging
    print(data)
    
    # Process and structure the data into a DataFrame
    df = data_processing(data)
    
    # Upload the processed data to Google BigQuery
    upload_to_bigquery(df)
