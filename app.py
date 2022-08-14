from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pyshorteners

app = Flask(__name__)



def success(name):
    data = pd.DataFrame()
    pd.set_option('display.max_columns', 5)
    # pd.set_option('display.max_colwidth', -1)

    req = requests.get(name)

    soup = BeautifulSoup(req.content, "html.parser")

    type_tiny = pyshorteners.Shortener()

    Scra_data = {"Price": [], "Location": [], "Baths": [], "Beds": [], "Area Covered": [], "Link": []}
    for i in soup.findAll('li', attrs={"aria-label": "Listing"}):

        a = i.find('span', attrs={"aria-label": "Price"})
        Scra_data["Price"].append(a.string)
        l = i.find('div', attrs={"aria-label": "Location"})
        Scra_data["Location"].append(l.string)
        li = i.find('a', href=True)
        lin = ("https://www.zameen.com" + li['href'])
        Scra_data["Link"].append(type_tiny.tinyurl.short(lin))

        try:
            baths = i.find('span', attrs={"aria-label": "Baths"})
            Scra_data["Baths"].append(baths.string)
        except:
            Scra_data["Baths"].append("None")
        ar = i.find('span', attrs={"aria-label": "Area"})
        Scra_data["Area Covered"].append(ar.string)
        try:
            beds = i.find('span', attrs={"aria-label": "Beds"})
            Scra_data["Beds"].append(beds.string)
        except:
            Scra_data["Beds"].append("None")

    data = pd.DataFrame(Scra_data)

    def make_clickable(val):
        # target _blank to open new window
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)

    data.style.format({'Link': make_clickable})
    # return (data)
    # data.to_csv("output.csv")
    # return render_template('simple.html',  tables=[data.to_html(classes='data', header="true")])
    print(Scra_data)
    return render_template('simple.html', value=Scra_data, tl=len(Scra_data['Price']))


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=["POST", "GET"])
def my_form_post():
    text = request.form['text']
    print(text)
    return success(text)


if __name__ == "__main__":
    app.run(debug=True)
