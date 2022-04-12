import csv
from splinter import Browser
from tqdm import tqdm

def collect_images(urls):
    browser = Browser(headless=True)
    # browser = Browser()

    width = 1024
    height = width // 3

    browser.driver.set_window_size(width, height)
    print("Browser size", browser.driver.get_window_size())
    for url in tqdm(urls):
        browser.visit(url)

        browser.screenshot(f"/home/falco/phareq_model/dataset/collected_images/img-{url.split('//')[-1]}.png")
    browser.quit()

if __name__ == "__main__":
    with open('top500Domains.csv') as fp:
        reader = csv.reader(fp)

        # Skip header
        _ = next(reader)
        urls = [f"http://{line[1]}" for line in reader] 

    # urls = ['http://google.com', 'http://pharec-dl.tech']
    collect_images(urls)
