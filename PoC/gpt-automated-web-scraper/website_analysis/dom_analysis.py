"""dom_analysis.py: A module for analyzing the Document Object Model (DOM) of a website.

This module is a part of the Website Structure Analysis component.
It is responsible for handling DOM parsing, element identification, and content extraction.
As the module evolves, it may include additional functionality related to DOM analysis.
"""

from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
import time

class HtmlLoader:
    def __init__(self, html_location):
        self.html_location = html_location

    def get_html(self):
        with open(self.html_location, 'r') as file:
            html_code = file.read()
        return html_code
    
class UrlHtmlLoader:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        response = requests.get(self.url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.text
    
class SeleniumScraperLoader:
    def __init__(self, url, headless=False):
        self.url = url
        self.headless = headless
        self.driver = self._get_driver()

    def _recommended_driver_option_bypass_captcha(self, options):
        # windows size dont be default
        options.add_argument('window-size=157x600')
        
        # randomized uzer agent
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)
        options.add_argument(f'--user-agent={user_agent}')


        return options
    def _get_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options = self._recommended_driver_option_bypass_captcha(options)

        driver = webdriver.Chrome(options=options)
        # Set implicit wait immediately after initializing the driver
        print("Waiting for driver start.")
        driver.implicitly_wait(10)  # wait up to 10 seconds
        print("Waiting for driver finish.")
        return driver

    def get_html(self):
        print("To input get.")
        self.driver.get(self.url)
        print("Finish input get.")
        self.driver.implicitly_wait(10)
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        print("Finish waiting ready state.")
        scraped_data = self.driver.page_source
        self.close()
        print("Close.")
        return scraped_data

    def close(self):
        self.driver.quit()
    
    

class HTMLParser:
    def __init__(self, parser_type='html.parser'):
        self.parser_type = parser_type

    def parse(self, html):
        return BeautifulSoup(html, self.parser_type)


class HTMLSearcher:
    def search(self, parsed_html, target_string):
        # Case Insensitive Search
        elements_containing_string = parsed_html(text=re.compile(target_string, re.I))

        # If not found in text nodes, search within tags
        if not elements_containing_string:
            elements_containing_string = parsed_html(string=lambda text: target_string in text)

            # If still not found, search within tag attributes
            if not elements_containing_string:
                elements_containing_string = parsed_html(lambda tag: target_string in str(tag.attrs))

        if elements_containing_string:
            # Just take the first occurrence for this example
            return elements_containing_string[0]
        else:
            return None


class ParentExtractor:
    def extract(self, element, generations):
        parent = element
        for _ in range(generations):
            parent = parent.parent if parent.parent is not None else parent
        return parent

class HTMLPreparer:
    def prepare(self, element):
        # Convert the element back into a string of HTML
        element_html = str(element)

        # Strip out any leading/trailing white space
        prepared_html = element_html.strip()

        return prepared_html


class HTMLProcessingPipeline:
    def __init__(self, parser, searcher, extractor, preparer):
        self.parser = parser
        self.searcher = searcher
        self.extractor = extractor
        self.preparer = preparer

    def process(self, html, target_string, generations):
        parsed_html = self.parser.parse(html)
        target_element = self.searcher.search(parsed_html, target_string)
        parent_element = self.extractor.extract(target_element, generations)
        prepared_html = self.preparer.prepare(parent_element)
        return prepared_html
    

class HtmlManager:
    _SOURCE_TYPE = ['url', 'url_selenium', 'file']
    @classmethod
    def get_source_type(cls):
        return cls._SOURCE_TYPE

    def __init__(self, source, source_type, target_string, max_length=4000, ):
        self.max_length = max_length
        self.target_string = target_string
        if source_type not in self._SOURCE_TYPE:
            raise ValueError(f"Invalid source type: {source_type}, should be one of {self._SOURCE_TYPE}")
        
        if source_type == 'url':
            self.loader = UrlHtmlLoader(source)
        elif source_type == 'url_selenium':
            self.loader = SeleniumScraperLoader(source)
        else:  # source_type == 'file'
            self.loader = HtmlLoader(source)

    
        
    def process_html(self):
        html = self.loader.get_html()
        print(html)
        raise ValueError("Test")

        if len(html) >= self.max_length:
            # Create instances of each class
            parser = HTMLParser()
            searcher = HTMLSearcher()
            extractor = ParentExtractor()
            preparer = HTMLPreparer()

            # Create an instance of the pipeline using the instances of the classes
            pipeline = HTMLProcessingPipeline(parser, searcher, extractor, preparer)

            # Call the `process` method of the pipeline with the necessary parameters
            target_string = self.target_string
            generations = 3
            processed_html = pipeline.process(html, target_string, generations)
        else:
            processed_html = html
            

        return processed_html 


def main():
    # Choose a loader
    manager = HtmlManager('https://www.scrapethissite.com/pages/simple/', source_type='url')

    # Create instances of each class
    parser = HTMLParser()
    searcher = HTMLSearcher()
    extractor = ParentExtractor()
    preparer = HTMLPreparer()

    # Create an instance of the pipeline using the instances of the classes
    pipeline = HTMLProcessingPipeline(parser, searcher, extractor, preparer)

    # Call the `process` method of the pipeline with the necessary parameters
    html = manager.process_html() # the HTML you want to process
    target_string = "Andorra"
    generations = 2
    prepared_html = pipeline.process(html, target_string, generations)

    # Now you can use `prepared_html` as you see fit
    print(prepared_html)

if __name__ == "__main__":
    main()
