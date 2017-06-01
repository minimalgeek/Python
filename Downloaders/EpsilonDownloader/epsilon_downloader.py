"""PDF downloader for Epsilon Theory website
"""
from bs4 import BeautifulSoup
import requests

def process_page(page_tree):
    links = page_tree.select('div.post-items div h2 a')
    for link in links:
        process_link(link)

def process_link(link):
    article_url = link['href']
    article = requests.get(article_url)
    if article.status_code == 200:
        print('article opened: ' + article_url)
        article_content = BeautifulSoup(article.text, "lxml")
        try:
            pdf_url = ('http://www.salientpartners.com'
                       + article_content.find('a', 'icon-pdf')['href'])
            pdf = requests.get(pdf_url, stream=True)
            save_pdf(pdf)
        except Exception:
            print('Error happened at: ', article_url)

def save_pdf(pdf):
    with open(pdf.url.split("/")[-1], 'wb') as output:
        output.write(pdf.content)

for year in range(2012, 2018):
    for month in range(1, 13):
        html = requests.get('http://www.salientpartners.com/epsilon-theory/'
                            + str(year) + '/' + str(month))
        if html.status_code == 200:
            print('archive page opened: ' + html.url)
            soup = BeautifulSoup(html.text, "lxml")
            process_page(soup)
