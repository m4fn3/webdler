import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# create a global session
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
session = requests.Session()
session.headers["User-Agent"] = user_agent


def handle_resource(resource_url: str, folder_name: str) -> str:
    # generate an asset url to be used in html
    asset_url = f"{resource_url.lstrip('/')}".replace("http://", "").replace("https://", "").replace(":/", "").split("?")[0]
    # convert url into the file path
    storage_url = f"./{folder_name}/{asset_url}"
    try:
        # create necessary folders
        os.makedirs("/".join(storage_url.split("/")[:-1]), exist_ok=True)
        # download the resource
        raw = session.get(resource_url).content
        with open(storage_url, 'wb') as file:
            file.write(raw)
    except:
        pass
    return asset_url


def download_page(url: str) -> str:
    folder_name = str(time.time())

    # download the page
    resp = session.get(url)
    html = resp.content
    soup = BeautifulSoup(html, "html.parser")

    # SAVE javascript
    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            # convert a relative path to an absolute url
            resource_url = urljoin(url, script.attrs.get("src"))
            # save resource to a local file
            asset_url = handle_resource(resource_url, folder_name)
            # change the resource url to a saved local file url
            script["src"] = asset_url

    # save css
    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            resource_url = urljoin(url, css.attrs.get("href"))
            asset_url = handle_resource(resource_url, folder_name)
            css["href"] = asset_url

    # save image
    for img in soup.find_all("img"):
        if img.attrs.get("src"):
            resource_url = urljoin(url, img.attrs.get("src"))
            asset_url = handle_resource(resource_url, folder_name)
            img["src"] = asset_url

    # save the modified html
    with open(f'./{folder_name}/index.html', 'w', encoding="utf-8") as file:
        file.write(str(soup))

    return f"./{folder_name}/index.html"


if __name__ == "__main__":
    target_url = input("enter the webpage url >")
    download_page(target_url)
