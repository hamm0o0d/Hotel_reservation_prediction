import pandas as pd 
import numpy as np
from flask import Flask, request, jsonify,render_template
from sklearn.preprocessing import StandardScaler
import pickle

app = Flask(__name__)

# load the pickle model
model = pickle.load(open("KNN.pkl","rb"))

@app.route("/")

def Home():
    return render_template("index.html")


@app.route("/predict", methods = ["POST"])
def predict ():
   
    features = [ ]
    i = 1
    for x in request.form.values():
        
        if i < 5:
         features.append(float(x)) 
        
        elif i == 5 :
            x = pd.Timestamp(x) 
            x = x.year         
            features.append(x)    
        elif i == 6 :
            if x == 'Corporate':
                features.append(1)
                features.append(0)

            elif x == 'Online':
                features.append(0)
                features.append(1)
            else:
                features.append(0)
                features.append(0)
        i+=1
    features = [np.array(features)]
    scaler =  pickle.load(open("scaler.pkl","rb"))
    features = scaler.transform(features)
    prediction = model.predict(features)
    if prediction ==1:
        prediction = 'not canceled'
    else:
        prediction = '  canceled'
    return render_template("index.html", prediction_text = "the reservation is {}".format(prediction)) 


if __name__ == "__main__":
   app.run(debug = True)

#  year(date) ... market segement (5 different values)

