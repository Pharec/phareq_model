"""
    Collect a dataset given a single domain (e.g. example.com)
"""
from crawl_urls import crawl_page, save_domain_urls
from collect_images_splinter import collect_images


def collect_one(domain_url="example.com", depth=2, limit=200):
    """
        1. Crawl domain site for links
        2. Collect images
    """

    urls = crawl_page(domain_url, depth=depth, limit=limit)
    save_domain_urls(domain_url, urls)

    collect_images(urls)
    return urls


if __name__ == "__main__":
    domain_url = "https://splonline.com.sa"

    collect_one(domain_url, depth=0, limit=None)
