import requests
from Proxies import Proxies as proxies
from bs4 import BeautifulSoup
import pandas
# Set the URL to scrape
searchterm = 'slusalke'
url = f"https://www.mimovrste.com/{searchterm}"

# Set the user agent to avoid being blocked
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Set the list of proxy servers to use
proxies_list = [
    "http://34.89.200.178:3128",
    "http://34.89.200.178:3128",
    "http://34.89.200.178:3128",
    "http://34.89.200.178:3128",
]

# Create a RotatingProxy object using the list of proxy servers
rotating_proxy = proxies.RotatingProxy(proxies=proxies_list)

l = []

# Send a GET request to the URL using the RotatingProxy object
response = requests.get(url, headers=headers, proxies=rotating_proxy)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the number of pages of results
    page_nr = int(soup.find_all("a", {"class":"pagination__item"})[-2].text)
    # Loop through each page
    for page in range(1, page_nr+1):
        # Set the URL for the current page
        page_url = f"{url}&pagination={page}"
        # Send a GET request to the URL using the RotatingProxy object
        response = requests.get(page_url, headers=headers, proxies=rotating_proxy)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all the elements containing information about the headphones
            all = soup.find_all("div", {"class":"product-box-category__body"})
            # Loop through each element
            for item in all:
                d = {}
                # Extract the name of the headphones
                d["Ime"] = item.find_all("h3")[0].text.replace("\n","")
                try:
                    # Extract the current and old price of the headphones
                    current_price = float(item.find_all("span", {"class":"product-price__price"})[0].text.replace("\n","").replace(",","."))
                    old_price = float(item.find_all("del", {"class":"product-price__price-old"})[0].textreplace("\n","").replace(",","."))
                    # Calculate the discount
                    discount = (old_price - current_price) / old_price
                    # Check if the discount is greater than 80%
                    if discount > 0.8:
                        # Extract the current and old price of the headphones
                        d["Nova cena"] = current_price
                        d["Stara cena"] = old_price
                        # Append the dictionary to the list
                        l.append(d)
                except:
                    pass

# Convert the list to a Pandas dataframe
df = pandas.DataFrame(l)

# Save the dataframe to a CSV file
df.to_csv("Output.csv")
