from flask import Flask, render_template, url_for, request
import requests
import pandas as pd

app = Flask(__name__)






@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data/",methods = ['POST','GET'])
def data():
    if request.method == "POST":
        key = ""

        url = "https://www.googleapis.com/civicinfo/v2/representatives"

        address = request.form['street_address']

        legislative = "country"

        congress = "legislatorLowerBody"
        senate = "legislatorUpperBody"

        payload = {'address': address, "levels": legislative, "roles": congress, "key": key}

        r = requests.get(url, params=payload)

        json = r.json()

        officials = json['officials']

        address = [elem['address'] for elem in officials]
        name = [elm['name'] for elm in officials]
        phone = [elm['phones'] for elm in officials]
        lookup = list(zip(name,phone))

        senator_table = pd.read_excel("senators.xls")
        congress_table = pd.read_excel('senators.xls',sheetname=1)
        congress_table = congress_table.set_index("District")


        return render_template("data.html", senate_table = senator_table.to_html(classes='Senator',bold_rows=True),
                               congress_table = congress_table.to_html(classes="Congress",bold_rows=True))




if __name__ == '__main__':
    app.run(debug=True)

