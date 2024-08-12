import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from utilities import get_listing_details, get_property_type_and_size

def scrape_page(page_number):
    base_url = f'https://www.mubawab.ma/fr/ct/casablanca/immobilier-a-vendre:p:{page_number}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    listings = soup.find_all('li', class_='listingBox w100')
    print(f"Found {len(listings)} listings on page {page_number}")
    
    data = []
    
    for listing in listings:
        try:
            # Extract Posting URL
            posting_url = listing.get('linkref')
            
            # Extract Price
            try:
                price = listing.find('span', class_='priceTag').text.strip()
            except AttributeError:
                price = None
            
            # Extract Neighbourhood
            try:
                neighbourhood = listing.find('h3', class_='listingH3').text.strip()
            except AttributeError:
                neighbourhood = None
            
            # Extract Image Preview URL
            try:
                image_url = listing.find('div', class_='photoBox').get('data-url')
            except AttributeError:
                image_url = None
            
            # Extract Listing Title
            try:
                title = listing.find('h2', class_='listingTit').text.strip()
            except AttributeError:
                title = None
            
            # Get additional details from the posting URL
            if posting_url:
                property_type, size, rooms = get_listing_details(posting_url)
                if not property_type or not size or not rooms:
                    print(f"Property type, size, or rooms not found for listing with URL {posting_url}, retrying...")
                    time.sleep(random.uniform(1, 2))
                    property_type, size, rooms = get_property_type_and_size(posting_url)
                # Adding a delay to avoid getting blocked by the server
                time.sleep(random.uniform(1, 2))
            else:
                property_type, size, rooms = None, None, None
            
            data.append({
                'Title': title,
                'Price': price,
                'Neighbourhood': neighbourhood,
                'Image URL': image_url,
                'Posting URL': posting_url,
                'Property Type': property_type,
                'Size': size,
                'Rooms': rooms
            })
            print(f"Scraped listing: {title}")
        except Exception as e:
            print(f"Error processing listing: {e}")
            # Adding a delay before trying the next listing to handle potential blocking
            time.sleep(random.uniform(1, 2))
    
    return data

def scrape_all_pages(total_pages=200):
    all_data = []
    for page_number in range(1, total_pages + 1):
        page_data = scrape_page(page_number)
        all_data.extend(page_data)
        print(f"Finished scraping page {page_number}")
        time.sleep(random.uniform(1, 2))  # Adding a delay between page requests
    
    # Convert the list to a DataFrame
    df = pd.DataFrame(all_data)
    
    # Save the DataFrame to a CSV file
    df.to_csv('real_estate_listings.csv', index=False)
    
    print('Data scraped and saved to real_estate_listings.csv')
