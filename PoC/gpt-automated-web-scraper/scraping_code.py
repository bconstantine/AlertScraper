

from bs4 import BeautifulSoup
from website_analysis.dom_analysis import HtmlLoader, UrlHtmlLoader, SeleniumScraperLoader

# Create HtmlLoader or UrlHtmlLoader based on the source type
def create_html_loader(source, source_type):
    if source_type == 'url':
        return UrlHtmlLoader(source)
    elif source_type == 'url_selenium':
        return SeleniumScraperLoader(source)
    else:  # source_type == 'file'
        return HtmlLoader(source)

html_loader = create_html_loader("https://www.thestreet.com/investing/stocks/as-nvidia-climbs-old-tech-stocks-get-ai-boost", "url_selenium")
response = html_loader.get_html()

html_soup = BeautifulSoup(response, 'html.parser')
    
# Import required libraries
import requests

# Define the URL of the website
url = 'https://www.thestreet.com/investing/stocks/as-nvidia-climbs-old-tech-stocks-get-ai-boost'

# Send HTTP request to the specified URL and save the response from server in a response object called r
r = requests.get(url)

# Create a BeautifulSoup object and specify the parser
html_soup = BeautifulSoup(r.text, 'html.parser')

# Find the news summary on the page
news_summary = html_soup.find('p').text

print(news_summary)
        