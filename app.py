
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pickle  # for loading machine learning models
import pandas as pd

app = Flask(__name__)

# Load machine learning models
models = {
    ('CSE', 'GM'): pickle.load(open('models\model_cs_gm.pkl', 'rb')),
    ('CSE', 'OBC'): pickle.load(open('models\model_cs_obc.pkl', 'rb')),
    ('CSE', 'SC'): pickle.load(open('models\model_cs_sc.pkl', 'rb')),
    ('ISE', 'GM'): pickle.load(open('models\model_ise_gm.pkl', 'rb')),
    ('ISE', 'OBC'): pickle.load(open('models\model_ise_obc.pkl', 'rb')),
    ('ISE', 'SC'): pickle.load(open('models\model_ise_sc.pkl', 'rb'))
}
colg_cs_gm=['BMSIT', 'MSRIT', 'BMSCE', 'RVCE', 'PES RING ROAD', 'DSCE', 'BIT',
       'JSSCE', 'PES ELECTRONIC CITY', 'NIE', 'MSRUAS', 'DSAT KANAKAPURA',
       'RVIT', 'AIT', 'RNSIT', 'REVA', 'OXFORD', 'DSU HOSUR', 'MCE',
       'NMIT', 'SMVIT', 'CMRIT', 'PRESIDENCY', 'HKBK', 'CAMBRIDGE',
       'GLOBAL', 'MVJ', 'AMC', 'KSIT', 'DONBOSCO']
# colg_cs_gm.to_numpy()
colg_cs_sc=['BMSIT', 'MSRIT', 'BMSCE', 'RVCE', 'PES RING ROAD', 'DSCE', 'BIT',
       'JSSCE', 'PES ELECTRONIC CITY', 'NIE', 'MSRUAS', 'DSAT KANAKAPUR',
       'RVIT', 'AIT', 'RNSIT', 'REVA', 'OXFORD', 'DSU HOSUR', 'MCE',
       'NMIT', 'SMVIT', 'CMRIT', 'PRESIDENCY', 'HKBK', 'CAMBRIDGE',
       'GLOBAL', 'MVJ', 'AMC', 'KSIT', 'DONBOSCO']
# colg_cs_sc.to_numpy()
colg_cs_obc=['BMSIT', 'MSRIT', 'BMSCE', 'RVCE', 'PES RING ROAD', 'DSCE', 'BIT',
       'JSSCE', 'PES ELECTRONIC CITY', 'NIE', 'MSRUAS', 'DSAT KANAKAPUR',
       'RVIT', 'AIT', 'RNSIT', 'REVA', 'OXFORD', 'DSU HOSUR', 'MCE',
       'NMIT', 'SMVIT', 'CMRIT', 'PRESIDENCY', 'HKBK', 'CAMBRIDGE',
       'GLOBAL', 'MVJ', 'AMC', 'KSIT', 'DONBOSCO']
colg_ise_gm=['BMSIT', 'MSRIT', 'BMSCE', 'RVCE', 'DSCE', 'BIT', 'JSSCE', 'NIE',
       'MSRUAS', 'DSAT KANAKAPURA', 'RVIT', 'AIT', 'RNSIT', 'REVA',
       'OXFORD', 'MCE', 'NMIT', 'SMVIT', 'CMRIT', 'PRESIDENCY', 'HKBK',
       'CAMBRIDGE', 'GLOBAL', 'MVJ', 'AMC', 'DONBOSCO']
colg_ise_obc=['BMSIT', 'MSRIT', 'BMSCE', 'RVCE', 'DSCE', 'BIT', 'JSSCE', 'NIE',
       'MSRUAS', 'DSAT KANAKAPURA', 'RVIT', 'AIT', 'RNSIT', 'REVA',
       'OXFORD', 'MCE', 'NMIT', 'SMVIT', 'CMRIT', 'PRESIDENCY', 'HKBK',
       'CAMBRIDGE', 'GLOBAL', 'MVJ', 'AMC', 'DONBOSCO']
colg_ise_sc=['BMSIT', 'MSRIT', 'BMSCE', 'RVCE', 'DSCE', 'BIT', 'JSSCE', 'NIE',
       'MSRUAS', 'DSAT KANAKAPURA', 'RVIT', 'AIT', 'RNSIT', 'REVA',
       'OXFORD', 'MCE', 'NMIT', 'SMVIT', 'CMRIT', 'PRESIDENCY', 'HKBK',
       'CAMBRIDGE', 'GLOBAL', 'MVJ', 'AMC', 'DONBOSCO']


# Predict function takes user input and returns the predicted college
def predict_college(rank, branch, category):
    model = models.get((branch, category), None)
    if model:
        # Perform prediction here using the selected model
        rank=pd.DataFrame([rank])
        predicted_college_array_number = model.predict(rank)
        predicted_college_array_number


        # predicted_college_array_number = list(predicted_college_array_number)

        
        if category=='GM' and branch=='CSE':
            colg=colg_cs_gm
        if category=='OBC'and branch=='CSE':
            colg=colg_cs_obc
        if category=='SC' and branch=='CSE':
            colg=colg_cs_sc
        if category=='GM' and branch=='ISE':
            colg=colg_ise_gm
        if category=='OBC' and branch=='ISE':
            colg=colg_ise_obc
        if category=='SC' and branch=='ISE':
            colg=colg_ise_obc

        
        predicted_clg=colg[int(predicted_college_array_number[0]-1)]

        return predicted_clg
    else:
        return "Invalid input"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        rank = int(request.form["rank"])
        branch = request.form["branch"]
        category = request.form["category"]

        predicted_college = predict_college(rank, branch, category)

        # Redirect to the result page with the predicted college as a query parameter
        return redirect(url_for("result", college=predicted_college))

    return render_template("index.html")

@app.route("/result")
def result():
    # Get the predicted college from the query parameter
    predicted_college = request.args.get("college")
    return render_template("result.html", college=predicted_college)

if __name__ == "__main__":
    app.run(debug=True)