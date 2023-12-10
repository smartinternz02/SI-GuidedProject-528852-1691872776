import numpy as np
import pickle
import joblib
import matplotlib
import matplotlib.pyplot as plt
import time
import pandas
import os
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "WSUwzDwBwUJSv5sUOaQ9Hg8foR8dIPLvfidK0k_4ylxE"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
import pickle
with open(r'C:\Users\ARE VINAY KUMAR\OneDrive\Documents\Traffic_volume_estimation-main\Flask\model.pkl','rb') as file:
    
 file.seek(0)
model = pickle.load(open(r"C:\Users\ARE VINAY KUMAR\OneDrive\Documents\Traffic_volume_estimation-main\Flask\model.pkl","rb"))
scale = pickle.load(open(r"C:\Users\ARE VINAY KUMAR\OneDrive\Documents\Traffic_volume_estimation-main\Flask\encoder.pkl","rb"))

@app.route('/')# route to display the home page
def home():
    return render_template('index.html') #rendering the home page

@app.route('/predict',methods=["POST","GET"])# route to show the predictions in a web UI
def predict():
    #  reading the inputs given by the user
    input_feature=[float(x) for x in request.form.values() ]  
    features_values=[np.array(input_feature)]
    names = [['holiday', 'temp', 'rain', 'snow', 'weather', 'year', 'month', 'day',
       'hours', 'minutes', 'seconds']]
    data = pandas.DataFrame(features_values,columns=names)
    #data = scale.transform(data)
     # predictions using the loaded model file
    prediction=model.predict(data)
    print(prediction)
    payload_scoring = {"input_data": [{"field": ['holiday', 'temp', 'rain', 'snow', 'weather', 'year', 'month', 'day',
       'hours', 'minutes', 'seconds'], "values": [input_feature]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/fe2afe09-3462-4c60-982f-408f1a00f9aa/predictions?version=2022-09-11', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    text = "Estimated Traffic Volume is :"
    return render_template("index.html",prediction_text = text + str(prediction))
     # showing the prediction results in a UI
if __name__=="__main__":
    
    # app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)