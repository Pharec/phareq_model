from splinter import Browser
from tqdm import tqdm
from pathlib import Path

"""
    How to collect screenshot and crawl using selenium:
        1. Visit page
        2. Take screenshot
        3. Find all a tags:
            a_tags = browser.find_by_tag('a')
        4. Get href of a_tags:
            hrefs = [ elem._element.get_attribute('href') for elem in a_tags ]
        5. Filter found urls
        6. Add filtered urls to queue
        7. Iterate or use multi-threading (back to 1)

"""

def process_one(element):
    raise("Not implemented")

    # browser = Browser(headless=True)

    # width = 1024
    # height = 3 * width // 4

    # browser.driver.set_window_size(width, height)
    # print("Browser size", browser.driver.get_window_size())
    # browser.visit(url)
    # image_path = (Path("./") / f"collected_images/img_{url_path(url)}").absolute()
    # browser.screenshot(
        # str(image_path),
        # unique_file=False
    # )
    # browser.quit()

def url_path(url):
    if url[:7] == "http://":
        lim = 7
    else:
        lim = 8

    return (
        url[lim:].strip('/')
        .strip()
        .replace('/', '__')
    )


if __name__ == "__main__":
    import csv
    with open('top500Domains.csv') as fp:
        reader = csv.reader(fp)

        # Skip header
        _ = next(reader)
        urls = [f"http://{line[1]}" for line in reader]

    # urls = ['http://google.com', 'http://pharec-dl.tech']
    # collect_images(urls[:10])
