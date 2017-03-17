from flask import Flask, render_template, request, url_for, jsonify
import requests
import pandas as pd
import re
import os



app = Flask(__name__)

 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/legal")
def legal():
    return render_template("legal.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/what-to-say")
def what_to_say():
    return render_template("what-to-say.html")


@app.route("/data", methods = ['GET','POST'])
def data():
    if request.method == "POST":

            #Look for secret key before deployment
        key = "AIzaSyADr0eoKKdN-s2jjUXwHTpAOthlOs7JfQw"
        url = "https://www.googleapis.com/civicinfo/v2/representatives"

        street = request.form['street']
        city = request.form['city']
        state = request.form['state']

        legislative = "country"

        house = "legislatorLowerBody"

        house_payload = {'address': street + " " + city, "levels": legislative, "roles": house,
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
        senator_table = pd.read_excel("data.xlsx")
        house_table = pd.read_excel("data.xlsx", sheetname=1)



        house_column = house_table.columns
        senate_column = senator_table.columns

        house_df = pd.DataFrame(data=house_table,columns= house_column)
        senator_df = pd.DataFrame(data=senator_table,columns=senate_column)
        



            #Create a sub dataframe to itterate through based on state
            #Helps deal with different column numbers for different amount
            #of phone numbers

        senate_by_state_df = senator_df[senator_df["STATE"] == state]
        house_df_by_state = house_df[(house_df["STATE"] == state) & (house_df["DISTRICT NUMBER"] == district_int)]

        house_clean = house_df_by_state.dropna(1)

        dic = house_clean.to_dict(orient= "split")
        liz = dic['data'][0]
        numbers = liz[4:]
        district_number = liz[1]
        rep = liz[2]
        url = liz[3]
        senate_clean = senate_by_state_df.dropna(1)
        senate_dic = senate_clean.to_dict(orient="split")
        senate_list = senate_dic['data']
        senator_1 = senate_list[0]
        senator_2 = senate_list[1]
        senator_1_url = senator_1[1]
        senator_1_name = senator_1[2]
        sen_1_offices = senator_1[3:]
        senator_2_url = senator_2[1]
        senator_2_name = senator_2[2]
        senator_2_offices = senator_2[3:]


    return render_template("data.html", numbers = numbers, district = district_number, rep = rep,
                               url = url, senator_1_url = senator_1_url, senator_1_name = senator_1_name,sen_1_offices = sen_1_offices,
                               senator_2_url = senator_2_url, senator_2_name = senator_2_name,
                               senator_2_offices = senator_2_offices)   
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = int(os.environ.get("DEBUG", False))
    app.run(host='0.0.0.0', port=port, debug=True)

