import tldextract
from pathlib import Path
from spidy import crawler

"""
    Crawl URLs in index page of popular domains
    INPUT: list of popular domains
    RETURN: list of urls crawled for each domain
"""


def crawl_page(page_url):
    page_domain = tldextract.extract(page_url).registered_domain
    try:
        crawled_urls = crawler.crawl(page_url)
    except Exception as e:
        print(f"Failed to crawl {page_url} with exception {e}")
        return []
    urls = [
        url for url in crawled_urls
        if not crawler.check_link(url) and
        tldextract.extract(url).registered_domain == page_domain
    ]

    return urls


def crawl_domains(domain_list, save_dir):
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    for domain_name in domain_list:
        url_list = crawl_page(domain_name)
        file_name = domain_name.split('//')[-1].replace('.', '_') + "_url.list"
        with open(save_path / file_name, 'w') as fp:
            fp.write('\n'.join(url_list))


if __name__ == "__main__":
    import csv
    with open('top500Domains.csv') as fp:
        reader = csv.reader(fp)

        # Skip header
        _ = next(reader)
        domain_urls = [f"http://{line[1]}" for line in reader]

    crawl_domains(domain_urls, "crawled_urls")
