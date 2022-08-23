import requests
from bs4 import BeautifulSoup
import pandas
r=requests.get("https://www.mimovrste.com/slusalke?s=slusalke")
c =r.content

soup = BeautifulSoup(c,"html.parser")

all =soup.find_all("div",{"class":"product-box-category__body"})

page_nr = soup.find_all("a",{"class":"pagination__item"})[-2].text.replace("\n","").replace(" ","")
l = []


base_url = "https://www.mimovrste.com/slusalke?pagination="
for page in range(1,int(page_nr)):
    r=requests.get(base_url+str(page))
    c=r.content
    soup = BeautifulSoup(c,"html.parser")
    all =soup.find_all("div",{"class":"product-box-category__body"})
    for item in all:
        d = {}
        d["Ime"]=item.find_all("h3")[0].text.replace("\n","")
        try:
            d["Nova cena"]=item.find_all("span",{"class":"product-price__price"})[0].text.replace("\n","")
            d["Stara cena"]= item.find_all("del",{"class":"product-price__price-old"})[0].textreplace("\n","")
        except:
            d["Trenutna cena"]=item.find_all("span",{"class":"product-price__price"})[0].text.replace("\n","")
        l.append(d)

df =pandas.DataFrame(l)

df.to_csv("Output.csv")

