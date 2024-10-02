import requests
from bs4 import BeautifulSoup
import re
import argparse

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text()))
        phone_numbers = set(re.findall(r'\+?\d[\d -]{8,}\d', soup.get_text()))
        
        social_links = {}
        for a in soup.find_all('a', href=True):
            href = a['href']
            if 'facebook.com' in href:
                social_links['Facebook'] = href
            elif 'twitter.com' in href:
                social_links['Twitter'] = href
            elif 'linkedin.com' in href:
                social_links['LinkedIn'] = href
            elif 'instagram.com' in href:
                social_links['Instagram'] = href

        print("Emails Found:")
        for email in emails:
            print(email)

        print("\nPhone Numbers Found:")
        for phone in phone_numbers:
            print(phone)

        print("\nSocial Media Links Found:")
        for platform, link in social_links.items():
            print(f"{platform}: {link}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

# Argument parser setup
parser = argparse.ArgumentParser(description='Passive reconnaissance web scraping tool.')
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the website to scrape.')

args = parser.parse_args()

scrape_website(args.url)
