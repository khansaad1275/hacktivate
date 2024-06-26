import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Function to extract emails from a given URL
def extract_emails_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = set()

    for string in soup.stripped_strings:
        matches = re.findall(email_pattern, string)
        if matches:
            emails.update(matches)

    return emails

# Replace
base_url = 'https://canalblog.com/'
visited_urls = set()
emails_found = set()

# Function to recursively crawl pages and find emails
def crawl_and_find_emails(url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    print(f"Visiting: {url}")

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract emails from the current page
        emails = extract_emails_from_url(url)
        if emails:
            print(f"Found {len(emails)} email(s) on {url}:")
            for email in emails:
                print(email)
            emails_found.update(emails)

        # Find links to other pages within the same domain
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(url, link['href'])
            if base_url in absolute_url and absolute_url not in visited_urls:
                crawl_and_find_emails(absolute_url)

    except Exception as e:
        print(f"Error crawling {url}: {str(e)}")

# Start crawling from the base URL
crawl_and_find_emails(base_url)

# Print the collected emails from the entire website
print("\nCollected emails from the entire website:")
for email in emails_found:
    print(email)