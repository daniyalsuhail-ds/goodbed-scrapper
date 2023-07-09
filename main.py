import requests
from bs4 import BeautifulSoup
import pandas as pd

import_file = "data.csv"
export_file = "data2.csv"

def scrape_Phone(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        phone = soup1.find("ul",{"class":"store-details"})
        phone = [i.find("span").text for i in phone if "Phone" in i.text][0]
    except:
        try:
            phone = soup1.find("div", attrs={"id":"phone-btn"})["data-phone"]
        except:
            phone = "Not Found"
    return phone

def scrape_store(instance, export_file):
    file = open(export_file, "a")
    zipcode = instance["code"]
    r = requests.get(f"https://www.goodbed.com/mattress-stores/?zip={zipcode}")
    if r.status_code == 200:
        print("\n\n200")
        soup = BeautifulSoup(r.text, 'html.parser')
        # data = soup.findAll("script")[-2]
        store_list = soup.findAll("div", attrs={"class":"store-item row no-gutters"})
        for store in store_list:
            link = "https://www.goodbed.com"+store.find("a")["href"]
            name = store.find("h3", {"class":"object-name mb-0"}).text.strip("\n ").split("\n")[0]
            add = store.find("span", {"class":"text-muted store-address"}).text
            phone = scrape_Phone(link)
            print(f"{name},{instance['state']},{instance['city']},{zipcode},{add},{phone},{link}")
            file.write(f"{name},{instance['state']},{instance['city']},{zipcode},{add},{phone},{link}")
    else:
        print("\n\n", r.status_code,zipcode)
        return
    file.close()

data = pd.read_csv(import_file, sep=",", dtype={'code': object})
del data["lat"]
del data["lon"]
del data["area_code"]

try:
    last_Record = open(export_file, "r").read().split("\n")[-2]
    last_zipcode = last_Record.split(",")[3]
    start = data[data["code"] == last_zipcode].index[0]
    stop = data.index.stop
    ranges = range(start, stop)
except:
    ranges = data.index
    
for i in ranges:
    instance = data.iloc[i]
    file = open(export_file, "a")
    # scrape_store(instance, export_file)
    zipcode = instance["code"]
    r = requests.get(f"https://www.goodbed.com/mattress-stores/?zip={zipcode}")
    if r.status_code == 200:
        print("\n\n200")
        soup = BeautifulSoup(r.text, 'html.parser')
        # data = soup.findAll("script")[-2]
        store_list = soup.findAll("div", attrs={"class":"store-item row no-gutters"})
        for store in store_list:
            link = "https://www.goodbed.com"+store.find("a")["href"]
            name = store.find("h3", {"class":"object-name mb-0"}).text.strip("\n ").split("\n")[0]
            add = store.find("span", {"class":"text-muted store-address"}).text
            
            r = requests.get(link)
            soup1 = BeautifulSoup(r.text, 'html.parser')
            try:
                phone = soup1.find("ul",{"class":"store-details"})
                phone = [i.find("span").text for i in phone if "Phone" in i.text][0]
            except:
                try:
                    phone = soup1.find("div", attrs={"id":"phone-btn"})["data-phone"]
                except:
                    phone = "Not Found"
            print(f"{name},{instance['state']},{instance['city']},{zipcode},{add},{phone},{link}")
            file.write(f"{name},{instance['state']},{instance['city']},{zipcode},{add},{phone},{link}\n")
    else:
        print("\n\n", r.status_code, zipcode)
        break
    file.close()
