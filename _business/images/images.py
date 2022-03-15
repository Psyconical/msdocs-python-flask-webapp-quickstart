
# Import External libraries
from urllib.parse import urljoin

# Importing utility functions
from _service.get.getHtml import getHtmlFromWebpage
from _service.utils.isValidUrl import is_valid
from _service.get.downloadImages import download

def get_all_images(url):  # Function to read all image's link in the provided website
    soup = getHtmlFromWebpage(url)
    # print(soup)
    urls = []
    for img in soup.findAll('img'):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url.rstrip())
    return urls

def fetch_images_from_url(url, path):# Function to operate all three above functions
    imgs = get_all_images(url)
    print(imgs)
    for x in range(3):  # download 3 images only
        impath = imgs[x]
        download(impath, path)
    return imgs
   