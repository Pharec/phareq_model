"""
    Collect a dataset given a single domain (e.g. example.com)
"""

from crawl_urls import crawl_page
from collect_images_splinter import collect_images


def collect_one(domain="example.com", limit=100):
    """
        1. Crawl domain site for links
        2. Collect images
    """
    urls = crawl_page(domain, limit=limit)
    collect_images(urls)
    return urls


if __name__ == "__main__":
    domain_url = "https://splonline.com.sa"

    collect_one(domain_url, limit=None)
