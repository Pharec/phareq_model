import os
from splinter import Browser
from tqdm import tqdm
from pathlib import Path


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


def collect_images(urls, save_dir):
    dir_path = Path(f"collected_images/{save_dir}")
    dir_path.mkdir(parents=True, exist_ok=True)

    browser = Browser(headless=True)

    width = 1024
    height = 3 * width // 4

    browser.driver.set_window_size(width, height)
    print("Browser size", browser.driver.get_window_size())
    for url in tqdm(urls):
        try:
            browser.visit(url)
        except Exception as e:
            print(f"Failed to visit {url} with exception {e}")
            continue

        image_path = (
            dir_path / f"img_{url_path(url)}"
        ).absolute()

        browser.screenshot(
            str(image_path),
            unique_file=False
        )
    browser.quit()


def read_crawled_urls(urls_dir='crawled_urls'):
    urls_dict = dict()

    filenames = os.listdir(urls_dir)
    for fn in filenames:
        with open(Path(urls_dir) / fn, 'r') as fp:
            dir_name = fn.split('.')[0].replace('url', 'images')
            urls_dict[dir_name] = [url.strip() for url in fp]

    return urls_dict


if __name__ == "__main__":
    import csv
    with open('top500Domains.csv') as fp:
        reader = csv.reader(fp)

        # Skip header
        _ = next(reader)
        urls = [f"http://{line[1]}" for line in reader]

    # urls = ['http://google.com', 'http://pharec-dl.tech']
    # collect_images(urls[:10])
    urls_dict = read_crawled_urls()

    for dir_name, urls in urls_dict.items():
        print(f"==== Collecting images for {dir_name} ...")
        collect_images(urls, dir_name)
