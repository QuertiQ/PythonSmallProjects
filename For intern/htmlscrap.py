# Import necessary libraries
from bs4 import BeautifulSoup
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from babel.dates import format_date
import re
import textwrap
import time

# Function to extract content from a webpage using Selenium
def extract_content_with_selenium(url):
    print("Launching Chrome browser...")

    # Path to the Chrome driver (make sure to update it for your environment)
    chrome_driver_path = "./chromedriver.exe"

    # Set Chrome options for Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    options.add_argument('--disable-software-rasterizer')  # Disable software-based rendering
    options.add_argument('--disable-webusb')  # Disable WebUSB support

    # Launch the Chrome browser
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        # Open the specified URL
        driver.get(url)
        print('Page loaded')
        # Extract the HTML content of the page
        html = driver.page_source
        time.sleep(2)  # Wait for 2 seconds to ensure the page is fully loaded
        return html
    finally:
        # Close the browser once done
        driver.quit()

# Function to scrape the body content using Selenium and BeautifulSoup
def content_scrap_selenium(url):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(extract_content_with_selenium(url), 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)  # Return the HTML of the body
    return ""

# Function to clean and structure the article's body content
def clean_body_content(url):
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(content_scrap_selenium(url), "html.parser")
    # Extract the first 15 elements of specific tags (h2, h3, p, strong)
    elements = soup.find_all(['h2', 'h3', 'p', 'strong'])[:15]

    # Initialize the content with a header
    content = "Zawartość artykułu\n"

    # Loop through the elements and format them
    for elem in elements:
        # Extract the text content of each element and wrap it to 100 characters
        text_content = elem.get_text(separator=' ', strip=True)
        wrapped_text = textwrap.fill(text_content, width=100)

        # Add tags based on the element type
        if elem.name in ['h2', 'h3']:
            content += f"  <{elem.name}>\n    {wrapped_text}\n  </{elem.name}>\n"
        elif elem.name == 'p':
            content += f"    <{elem.name}>\n        {wrapped_text}\n    </{elem.name}>\n"
        elif elem.name == 'strong':
            content += f"<{elem.name}>{wrapped_text}</{elem.name}>"

    return content  # Return the formatted content

# Function to scrape metadata and content of an article
def scrapingdata(url):
    # Use newspaper3k to download and parse the article
    my_article = Article(url, language='pl')
    my_article.download()
    my_article.parse()

    soup = BeautifulSoup(my_article.html, 'html.parser')

    # Extract the title of the article
    title = my_article.title

    # Initialize variables for date and category
    date = 'none'
    category = 'none'

    # Extract the publication date (if available)
    if my_article.publish_date:
        date = format_date(my_article.publish_date, format='long', locale='pl_PL')
    else:
        # Finding it other way
        date_element = soup.find('time')
        date_pattern = re.compile(r'\d{1,2}\s\w+\s\d{4}')
        possible_dates = soup.find_all(text=date_pattern)

        if date_element:
            publish_date = date_element.get('datetime') or date_element.text
            publish_date = datetime.strptime(publish_date, "%d.%m.%Y").strftime("%Y.%m.%d")
            publish_date = datetime.strptime(publish_date, "%Y.%m.%d")
            date = format_date(publish_date, format='long', locale="pl_PL")
        elif possible_dates:
            date = possible_dates[0]
        else:
            date = "Not Found"

    # Extract the article's category based on specific URL patterns
    link = soup.find('a', href=lambda href: href and 'kategorie' in href)
    link2 = soup.find('a', href=lambda href: href and 'kategoria' in href)

    if link:
        category = link.text
    elif link2:
        category = link2.text
    else:
        category = "Nie znaleziono"

    # Return the articles metadata as a formatted string
    return f'Tytuł: {title}\nKategoria: {category}\nData wydania: {str(date)}\n'

# Main function to scrape and save multiple articles
def main(urls):
    articles_data = ''  # Initialize a string to store all articles data

    for url in urls:
        # Scrape metadata and content for each URL
        article_data = scrapingdata(url)
        content_data = clean_body_content(url)
        articles_data += article_data
        articles_data += content_data

    # Save the articles data to a JSON file
    with open("response.json", "w", encoding='utf-8') as json_file:
        json_file.write(articles_data)
        json_file.write("\n\n\n")

# List of URLs to scrape
urls = [
    "https://bistrolubie.pl/pierniki-z-miodem-tradycyjny-przepis-na-swiateczne-ciasteczka-pelne-aromatu",
    "https://bistrolubie.pl/piernik-z-mascarpone-kremowy-i-pyszny-przepis-na-deser-idealny-na-swieta",
    "https://spidersweb.pl/2024/07/metamorfoza-w-centrum-warszawy.html",
    "https://spidersweb.pl/2024/07/kontrolery-na-steam-rosnie-popularnosc.html",
    "https://www.chip.pl/2024/06/wtf-obalamy-mity-poprawnej-pozycji-przy-biurku",
    "https://www.chip.pl/2024/07/sony-xperia-1-vi-test-recenzja-opinia",
    "https://newonce.net/artykul/chief-keef-a-sprawa-polska-opowiadaja-benito-gicik-crank-all",
    "https://newonce.net/artykul/glosna-gra-ktorej-akcja-toczy-sie-w-warszawie-1905-roku-gralismy-w-the-thaumaturge"
]

# Run the main function
main(urls)
