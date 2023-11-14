import requests
from tqdm import tqdm
from bs4 import BeautifulSoup, Comment
import re
import csv
from urljoin import url_path_join


def crawl_and_scrape_python_org():
    # Start with the homepage
    url = "http://localhost:8000"
    visited_urls = set()  # Keep track of visited URLs to avoid duplicates
    to_visit = [url]  # Queue of URLs to crawl

    # Crawl the website and collect text data
    with tqdm(total=len(to_visit)) as pbar:
        text_data = []
        while to_visit:
            current_url = to_visit.pop(0)
            visited_urls.add(current_url)

            # Fetch the page content from the web
            try:
                response = requests.get(current_url, allow_redirects=True)
                if response.status_code != 200:
                    raise Exception(f"Error: Unexpected status code {response.status_code}")

                soup = BeautifulSoup(response.content, features="lxml")

                # Extract text from the page
                text = extract_text(soup)
                text_data.append((current_url, text))

                # Find all anchors
                find_all = soup.find_all("a")

                # Find all links on the page and add them to the queue
                for link in find_all:
                    href = link.get("href").split("#")[0]

                    to_visit_url = url_path_join(url, href)

                    if href and to_visit_url not in visited_urls and to_visit_url not in to_visit:
                        if "#" not in href and "mailto" not in href and "http" not in href and ".." not in href:
                            if "zip" not in href and "bz2" not in href and "epub" not in href:
                                if "3." not in href and "2." not in href and "changelog.html" not in href:
                                    print(f"to_visit_url: {to_visit_url}")
                                    to_visit.append(to_visit_url)

            except Exception as e:
                if response.status_code != 404:
                    print(f"Error crawling URL: {current_url}")
                    print(e)
                continue
                # Skip to the next URL in case of an error

            pbar.update()  # Update the progress bar

    # Save the collected text data to a CSV file
    with open("python_org_data.csv", "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Text"])
        for row in text_data:
            writer.writerow(row)


def extract_text(soup):
    # Remove unnecessary elements like scripts, styles, and comments
    for script in soup.find_all("script"):
        script.decompose()
    for style in soup.find_all("style"):
        style.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Extract text from the remaining elements
    text = soup.get_text(separator="\n")
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = text.strip()  # Remove leading and trailing whitespace

    return text


if __name__ == "__main__":
    crawl_and_scrape_python_org()
