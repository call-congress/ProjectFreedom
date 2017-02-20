from flask import Flask, render_template, url_for, request
import requests
import pandas as pd
import re

app = Flask(__name__)






@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data/",methods = ['POST','GET'])
def data():
    # I know this should probably be a get request... ill look into it.
    if request.method == "POST":
        key = ""
        url = "https://www.googleapis.com/civicinfo/v2/representatives"

        address = request.form['street_address']
        state = request.form['state']

        legislative = "country"

        house = "legislatorLowerBody"

        house_payload = {'address': address, "levels": legislative, "roles": house,
                         "key": key}

        house_request = requests.get(url, params=house_payload)


        house_json = house_request.json()

        #Parse the JSON data for district num

        house_dict = house_json['divisions']
        district = list(house_dict)
        district = str(district)
        district_num = re.findall('\d', district)
        district_num = [''.join(district_num)]

        #Load data from excel sheet rubs is building
        senator_table = pd.read_excel("Congress reps doc.xlsx")
        congress_table = pd.read_excel("Congress reps doc.xlsx", sheetname=1)



        congress_column = congress_table.columns
        senate_column = senator_table.columns

        congress_df = pd.DataFrame(data=congress_table,columns=congress_column)
        senator_df = pd.DataFrame(data=senator_table,columns=senate_column)

        congress_df.set_index("STATE",inplace=True)
        senator_df.set_index("STATE",inplace=True)

        #Create a sub dataframe to itterate through based on state
        #Helps deal with different column numbers for different amount
        #of phone numbers

        senate_by_state_df = senator_df[senator_df["STATE"] == 'Alabama']

        senate_by_state_dic = senate_by_state_df.to_dict()


        return render_template("data.html", senator_table = senate_by_state_dic,
                               congress_table = congress_df.to_dict(), state = state, sen = senate_by_state_df)




if __name__ == '__main__':
    app.run(debug=True)


