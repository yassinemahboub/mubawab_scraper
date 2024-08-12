import requests
from bs4 import BeautifulSoup

def get_listing_details(detail_url):
    try:
        response = requests.get(detail_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract Type of property
        property_type = None
        size = None
        rooms = None
        
        try:
            property_type = soup.find('p', class_='adMainFeatureContentValue').text.strip()
        except AttributeError:
            print(f"Property type not found for {detail_url}")
        
        try:
            size_feature = soup.find('div', class_='disFlex adDetails')
            if size_feature:
                size = size_feature.find_all('span')[0].text.strip()
                rooms = size_feature.find_all('span')[1].text.strip()
        except AttributeError:
            print(f"Size or rooms not found for {detail_url}")
        
        return property_type, size, rooms
    except Exception as e:
        print(f"Error getting details from {detail_url}: {e}")
        return None, None, None

def get_property_type_and_size(detail_url):
    property_type = None
    size = None
    rooms = None
    try:
        property_type, size, rooms = get_listing_details(detail_url)
    except Exception as e:
        print(f"Error getting property type and size for {detail_url}: {e}")
    return property_type, size, rooms
