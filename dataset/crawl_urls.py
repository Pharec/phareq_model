"""
    Crawl URLs in index page of popular domains
    INPUT: list of popular domains
    RETURN: list of urls crawled for each domain
"""

import tldextract
from pathlib import Path
from urllib.parse import urljoin, urlparse
from spidy import crawler

from urllib.request import urlopen
import mimetypes


def guess_type_of(link, strict=True):
    """
        From Stackoverflow (Modified)
    """
    link_type, _ = mimetypes.guess_type(link)
    if link_type is None and strict:
        try:
            u = urlopen(link, timeout=10)
            link_type = u.headers.get_content_type()
        except Exception as e:
            print(f"Failed to urlopen {link} to check page type with: {e}")
    return link_type


def crawl_page(page_url, depth=2, limit=None):
    """
        Crawl iteratively for a certain depth
    """
    seen_urls = set([page_url])
    url_depth = list()

    url_depth.append(set(crawl_once(page_url, limit=limit)))
    seen_urls.update(url_depth[0])

    for i in range(depth):
        url_depth.append(set())
        for url in list(url_depth[i]):
            if limit and len(seen_urls) >= limit:
                return list(seen_urls)[:limit]

            crawled_urls = set(crawl_once(url, limit=limit))
            d_urls = crawled_urls - seen_urls
            url_depth[i+1].update(d_urls)
            seen_urls.update(d_urls)

    return list(seen_urls)


def crawl_once(page_url, limit=None):
    scheme = urlparse(page_url).scheme
    page_domain = tldextract.extract(page_url).registered_domain

    def preprocess_url(crawled_url):
        if crawled_url[:4] != 'http':
            if page_url[-1] != '/' and crawled_url[0] != '/':
                crawled_url = "/" + crawled_url
            res_url = urljoin(page_url, crawled_url)
        else:
            if scheme != crawled_url[:len(scheme)]:
                res_url = scheme + "://" + crawled_url.split("://")[-1]
            else:
                res_url = crawled_url

        parsed_url = urlparse(res_url)
        # return f"{parsed_url.scheme}/{parsed_url.netloc}/{parsed_url.path}"
        return parsed_url.geturl().split("#")[0]

    try:
        crawled_urls = crawler.crawl(page_url)
    except Exception as e:
        print(f"Failed to crawl {page_url} with exception {e}")
        return list()

    pre_urls = [
        preprocess_url(url) for url in crawled_urls
        if url and url.strip()]
    urls = [
        url for url in pre_urls
        if check_link(url, page_domain)
    ]

    if limit:
        urls = urls[:limit]

    return urls


def check_link(url, page_domain):
    if len(url) < 10 or len(url) > 255:
        return False

    # Must be an http(s) link
    if url[0:4] != 'http':
        return False

    link_domain = tldextract.extract(url).registered_domain
    if link_domain != page_domain:
        return False

    other_protocols = [
        "tel:",
        "callto:",
        "mailto:",
        "sms:",
        "data:",
        "android-app:",
        "ios-app:",
        "telprompt",
        "javascript"
    ]
    other_protocols += [p.upper() for p in other_protocols]

    path = urlparse(url).path.strip('/')
    for p in other_protocols:
        if path.startswith(p):
            return False

    if guess_type_of(url) != 'text/html':
        return False

    return True


def crawl_domains(domain_list,
                  save_dir="crawled_urls",
                  save=True, depth=0, limit=None):

    url_dict = dict()
    for domain_name in domain_list:
        urls = crawl_page(domain_name, depth=depth, limit=limit)

        if save:
            save_domain_urls(domain_name, urls, save_dir)

        url_dict[domain_name] = urls

    return url_dict


def save_domain_urls(domain_url, url_list, save_dir="crawled_urls"):
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    file_name = urlparse(domain_url).netloc.replace('.', '_') + "_url.list"
    with open(save_path / file_name, 'w') as fp:
        fp.write('\n'.join(url_list))


def read_domains(domains_list_filename='domain_refs/draft1_domains.list'):
    with open(domains_list_filename, 'r') as fp:
        return [domain.strip() for domain in fp]


if __name__ == "__main__":
    import csv
    with open('top500Domains.csv') as fp:
        reader = csv.reader(fp)

        # Skip header
        _ = next(reader)
        domain_urls = [f"http://{line[1]}" for line in reader]

    # domain_url = 'https://splonline.com.sa'
    # domain_url = 'https://mcit.gov.sa'
    # domain_url = 'https://apple.com'
    # domain_url = 'https://dropbox.com'
    # domain_url = 'https://amazon.com'
    # domain_url = 'https://amazon.sa'
    # domain_url = 'https://noon.com'
    # domain_url = 'https://xcite.com'
    # domain_url = 'https://google.com'
    # domain_url = 'https://aramex.com'
    # domain_url = 'https://airbnb.com'
    # domain_url = 'https://paypal.com'
    # domain_url = 'https://dhl.com'
    # domain_url = 'https://whatsapp.com'
    # domain_url = 'https://youtube.com'
    # domain_url = 'https://tiktok.com'
    # domain_url = 'https://facebook.com'
    # domain_url = 'https://twitter.com'
    # domain_url = 'https://coinbase.com'
    # domain_url = 'https://rain.com'
    # domain_url = 'https://binance.com'
    # domain_url = 'https://bitoasis.net'
    # domain_url = 'https://coursera.com'
    # domain_url = 'https://edx.com'
    # domain_url = 'https://udemy.com'
    # domain_url = 'https://alahli.com'
    # domain_url = 'https://alrajhibank.com'
    # domain_url = 'https://bankaljazira.com'
    # domain_url = 'https://anb.com.sa'
    # domain_url = 'https://alinma.com'

    # urls = crawl_page(domain_url, depth=0)
    # url_dict = crawl_domains(domain_urls, "crawled_urls")
    domains = read_domains()
    url_dict = crawl_domains(domains, save=True)
