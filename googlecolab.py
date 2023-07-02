from webdler.webdler import download_page
from IPython.core.display import HTML

url = ""  # @param {type:"string"}
html_path = download_page(url)
HTML(filename=html_path)
