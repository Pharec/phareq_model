from splinter import Browser
from tqdm import tqdm
from pathlib import Path


def collect_images(urls):
    browser = Browser(headless=True)
    # browser = Browser()

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
            Path("./") / f"collected_images/img_{url.split('//')[-1]}_"
        ).absolute()
        browser.screenshot(
            str(image_path)
        )
    browser.quit()

if __name__ == "__main__":
    import csv
    with open('top500Domains.csv') as fp:
        reader = csv.reader(fp)

        # Skip header
        _ = next(reader)
        urls = [f"http://{line[1]}" for line in reader]

    # urls = ['http://google.com', 'http://pharec-dl.tech']
    collect_images(urls[:10])
