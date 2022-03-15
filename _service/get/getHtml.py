from bs4 import BeautifulSoup as bs
import requests

# Get HTML from a given URL
def getHtmlFromWebpage(url):
    return bs(requests.get(url).content, "html.parser")