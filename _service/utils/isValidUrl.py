from urllib.parse import urlparse

def is_valid(url):  # Function to check the provided link whether it works
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)