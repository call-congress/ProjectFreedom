from flask import Flask, render_template, request
import requests
import pandas as pd
import re

app = Flask(__name__)






@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data/",methods = ['POST','GET'])
def data():
    if request.method == "POST":
        key = "AIzaSyADr0eoKKdN-s2jjUXwHTpAOthlOs7JfQw"
        url = "https://www.googleapis.com/civicinfo/v2/representatives"

        address = request.form['firstname']
        state = "NJ"

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
        district_int = int(district_num[0])

        #Load data from excel sheet rubs is building
        senator_table = pd.read_excel("Congress reps doc.xlsx")
        house_table = pd.read_excel("Congress reps doc.xlsx", sheetname=1)



        house_column = house_table.columns
        senate_column = senator_table.columns

        house_df = pd.DataFrame(data=house_table,columns= house_column)
        senator_df = pd.DataFrame(data=senator_table,columns=senate_column)



        #Create a sub dataframe to itterate through based on state
        #Helps deal with different column numbers for different amount
        #of phone numbers

        senate_by_state_df = senator_df[senator_df["STATE"] == 'Alabama']
        house_df_by_state = house_df[(house_df["STATE"] == state) & (house_df["DISTRICT NUMBER"] == district_int)]


        lis = house_df_by_state.to_dict(orient="split")
        data = lis['data'][0]
        final = data[4:]

    return render_template("/scripts/index.html", house = final , senate = senate_by_state_df)



if __name__ == '__main__':
    app.run(debug=True)


