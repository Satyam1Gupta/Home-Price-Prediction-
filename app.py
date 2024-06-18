import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app=Flask(__name__)
# Load the model
reg_model=pickle.load(open('regression_model.pkl','rb'))
scaler=pickle.load(open('scaling.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1)) 
    new_data=scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output=reg_model.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict', methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    print(np.array(data).reshape(1,-1)) 
    final_input=scaler.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output=reg_model.predict(final_input)
    print(output)
    return render_template("home.html", prediction_text="The House Price Prediction is {}".format(output))

# # this is for development environment
# if __name__=="__main__":
#     app.run(debug=True)
    
# this is for production environment
if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False)