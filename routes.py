from flask import Flask, render_template,request
import pandas as pd
import pickle
import numpy as np
app = Flask(__name__)
#Pour prendre en compte les variables de configuration
app.config.from_object('config')
#decorateur route() pour definir une ensemble de route
#Pour prendre en compte les variables de configuration
model = pickle.load(open('modelcreditanalysis.pkl', 'rb'))
app.config.from_object('config')
df = pd.read_csv('static/germandatabase.csv')
Col = df.columns
def pos(df,po):
    return df.iloc[:po]



@app.route("/")
def index():
   
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    float_features = [float(x) for x in request.form.values()]
    final_features = [np.array(float_features)]
    prediction = model.predict(final_features)

    
    if prediction == 1:
        answer = "UN BON CLIENT (SUSCEPTIBLE A REMBOURSER LA DETTE EMPRUNTER)"
    else:
        answer = "UN MAUVAIS CLIENT (SUSCEPTIBLE A REMBOURSER LA DETTE EMPRUNTER)"
   
    return render_template('index.html', prediction_text='LE CLIENT EST {}'.format(answer))

@app.route("/table")
def tables():  
    g = df
    c = pos(g,10)
    df2 =df.T
    return render_template("tables.html", lignes = [c.to_html(classes="data", header = True)],ligness = [df2.to_html(classes="data", header = True)])



if __name__ == "__main__":
    app.run()