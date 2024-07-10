from flask import Flask, render_template, request, after_this_request
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from io import BytesIO

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import StackingClassifier


app = Flask(__name__)

# tkinter_result = None


df_a = pd.read_csv("D:\CBIT-Projects\sih23_final_fr\sih23\gujarat_db.csv")
df_p = pd.read_csv("D:\CBIT-Projects\sih23_final_fr\sih23\dataset.csv", sep=';')

CATEGORIES = ["CLASS/STANDARD", "GENDER", "CASTE", "REASON"]

Y = df_p.iloc[:, 34:35]
X = df_p.iloc[:, 0:34]
X_train, X_test,Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state=0)
sm = SMOTE(random_state=42, k_neighbors=3)
X_smote, y_smote = sm.fit_resample(X_train, Y_train)

def meta_classifier(single_row, X_smote, y_smote):
    estimator_list = [
            ('logmodel',LogisticRegression(max_iter=10000)),
            ('rfc',RandomForestClassifier()),
            ('xgbpreds',xgb.XGBClassifier()),
            ('AdaBoost', AdaBoostClassifier()) ]

    # # Define the stacking classifier with Logistic Regression as the final estimator
    # stack_classifier = StackingClassifier(estimators=estimator_list, final_estimator=LogisticRegression(max_iter=10000), cv=10)

    # # Fit the stacking classifier on the SMOTE data
    # stack_classifier.fit(X_smote, y_smote)

    # Define the stacking classifier with Logistic Regression as the final estimator
    stack_classifier = StackingClassifier(estimators=estimator_list, final_estimator=LogisticRegression(max_iter=10000), cv=10)

    # Fit the stacking classifier on the SMOTE data
    stack_classifier.fit(X_smote, y_smote)
    
    # Ensure that single_row is a 2D array with one row
    single_row = single_row.reshape(1, -1)

    # Predict the class label for the single input row
    prediction = stack_classifier.predict(single_row)

    return prediction



@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html", categories=CATEGORIES)


@app.route("/analyse", methods=["POST"])
def analysis_res():
    key = request.form.get("key")
    on = request.form.get("on") if key != "AREA" else int(request.form.get("on"))
    category = request.form.get("category")
    criteria, data = analyse(df_a, key=key, on=on, cat=category)

    image_paths = []

    if category == "all":
        image_paths = display_all(criteria, on, data)
        return render_template("plot_all.html", image_paths=image_paths)
    else:
        image_paths = display_single_plot(category, on, data[criteria.index(category)])
        return render_template("Blank_Graph.html", image_paths=image_paths)
    

@app.route("/predict", methods=["POST"])
def predict():
    return render_template("predict.html")


@app.route('/prediction', methods=["POST"])
def predict_res():
    marital_status = int(request.form.get("marital_status"))
    application_mode = int(request.form.get("application_mode"))
    application_order = 0
    course = int(request.form.get("course"))
    attendance_regime = int(request.form.get("att_regime"))
    previous_qualification = int(request.form.get("previous_qualification"))
    nationality = int(request.form.get("nationality"))
    mothers_qual = int(request.form.get("mothers_qual"))
    fathers_qual = int(request.form.get("fathers_qual"))
    mothers_occ = int(request.form.get("mothers_occ"))
    fathers_occ = int(request.form.get("fathers_occ"))
    displaced = int(request.form.get("displaced"))
    ed_sp_needs = int(request.form.get("educational_special_needs"))
    debtor = int(request.form.get("debtor"))
    tuition_fee = int(request.form.get("tuition_fee_upto_date"))
    gender = int(request.form.get("gender"))
    scholarship = int(request.form.get("scholarship_holder"))
    age_at_enrollment = int(request.form.get("age_at_enrollment"))
    international = int(request.form.get("international"))
    cu_1sem_cred = int(request.form.get("cu_1sem_cred"))
    cu_1sem_enrolld = int(request.form.get("cu_1sem_enrolld"))
    cu_1sem_eval = int(request.form.get("cu_1sem_eval"))
    cu_1sem_approved = int(request.form.get("cu_1sem_approved"))
    cu_1sem_grade = int(request.form.get("cu_1sem_grade"))
    cu_1sem_without_eval = int(request.form.get("cu_1sem_without_eval"))
    cu_2sem_cred = int(request.form.get("cu_2sem_cred"))
    cu_2sem_enrolld = int(request.form.get("cu_2sem_enrolld"))
    cu_2sem_eval = int(request.form.get("cu_2sem_eval"))
    cu_2sem_approved = int(request.form.get("cu_2sem_approved"))
    cu_2sem_grade = int(request.form.get("cu_2sem_grade"))
    cu_2sem_without_eval = int(request.form.get("cu_2sem_without_eval"))
    unemployment_rate = int(request.form.get("unemployment_rate"))
    inflation_rate = int(request.form.get("inflation_rate"))
    gdp = int(request.form.get("gdp"))
    single_row = []
    
    single_row.extend([marital_status, application_mode, application_order,course,attendance_regime,
                  previous_qualification,nationality,mothers_qual,fathers_qual, mothers_occ,fathers_occ,
                  displaced,ed_sp_needs,debtor,tuition_fee,gender,scholarship,age_at_enrollment,international,
                  cu_1sem_cred,cu_1sem_enrolld,cu_1sem_eval,cu_1sem_approved,cu_1sem_grade,
                  cu_1sem_without_eval,cu_2sem_cred,cu_2sem_enrolld,cu_2sem_eval,cu_2sem_approved,cu_2sem_grade,cu_2sem_without_eval,unemployment_rate,inflation_rate,
                  gdp])
    single_row = np.array(single_row)
    prediction = meta_classifier(single_row, X_smote, y_smote)
    return render_template("prediction1.html", single_row=single_row, prediction=prediction[0])



def analyse(DF: pd.DataFrame, key: str = "STATE", on="GUJARAT", cat="all"):
    if key != "AREA":
        key = key.upper()
        on = on.upper()
    Dict = {"ACADEMIC": 0, "MOVED": 0, "POVERTY": 0, "OTHERS": 0}
    Dict_percentages = {}
    Gender = {"MALE": 0, "FEMALE": 0}
    Gender_Percent = {}
    Standard_Dict = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
    }
    Standard_Dictper = {}
    Caste = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    Casteper = {}
    for i in range(len(DF)):
        if (DF.loc[i, key] == on) and ((DF.loc[i, "GRADE"]) < 4):
            class_drops = DF.loc[i, "CLASS/STANDARD"]
            Standard_Dict[class_drops] += 1
            caste_drops = DF.loc[i, "CASTE"]
            Caste[str(caste_drops)] += 1
            if DF.loc[i, "GRADE"] != 0:
                Dict["ACADEMIC"] += 1
            if (DF.loc[i, "GENDER"]) == "M":
                Gender["MALE"] += 1
            if (DF.loc[i, "GENDER"]) == "F":
                Gender["FEMALE"] += 1
            if DF.loc[i, "GRADE"] == 0:
                if DF.loc[i, "MOVED"] == "YES":
                    Dict["MOVED"] += 1
                elif DF.loc[i, "OTHERS"] == "YES":
                    Dict["OTHERS"] += 1
                elif DF.loc[i, "POVERTY"] == "YES":
                    Dict["POVERTY"] += 1

    q, r, s, t = (
        sum(Dict.values()),
        sum(Standard_Dict.values()),
        sum(Caste.values()),
        sum(Gender.values()),
    )

    if sum(Dict.values()) == 0:
        q = 1

    for i in Dict.keys():
        percentage = (Dict[i] / q) * 100
        Dict_percentages[i] = percentage

    if sum(Standard_Dict.values()) == 0:
        r = 1

    for i in Standard_Dict.keys():
        percentage = (Standard_Dict[i] / r) * 100
        Standard_Dictper[i] = percentage

    if sum(Caste.values()) == 0:
        s = 1

    for i in Caste.keys():
        percentage = (Caste[i] / s) * 100
        Casteper[i] = percentage

    if sum(Gender.values()) == 0:
        t = 1

    for i in Gender.keys():
        percentage = (Gender[i] / t) * 100
        Gender_Percent[i] = percentage
    criteria = ["REASON", "CLASS/STANDARD", "CASTE", "GENDER"]
    data = [Dict_percentages, Standard_Dictper, Casteper, Gender_Percent]
    return criteria, data


def display_all(criteria: list[str], parameter: str, data: list[dict]):
    fig, ax = plt.subplots(2, 2, layout="constrained")
    fig = plt.gcf()
    fig.set_size_inches(10.2, 7.9)
    colors = ["#FF9933", "lightblue", "green"]

    for i in range(4):
        data_dict = data[i]
        axis = ax[i // 2, i % 2]  # Calculate subplot position
        bars = axis.bar(
            data_dict.keys(),
            data_dict.values(),
            label=data_dict.keys(),
            color=colors,
            align="center",
        )
        fig.suptitle(f"{parameter} DROPOUT ANALYSIS", c="#FF9933", fontweight="bold")
        axis.set_xticks(range(len(data_dict.keys())))
        axis.set_xlabel(f"{criteria[i]} CRITERION", c="green", fontweight="bold")
        axis.set_ylabel("PERCENTAGE", c="green", fontweight="bold")
        axis.bar_label(bars, padding=0, fmt="%.1f")
    # Clear the entire figure to release memory
    # plt.clf()
    image_paths = []
    for i, axs in enumerate(ax.flat):
        buffer = BytesIO()
        axs.get_figure().savefig(buffer, format="png")
        buffer.seek(0)
        image_path = f"D:\CBIT-Projects\sih23_final_fr\sih23\static/plot_{i + 1}.png"
        image_paths.append(image_path)
        with open(image_path, "wb") as img_file:
            img_file.write(buffer.read())

        plt.clf()
        plt.close()
        # Return a list of image paths
    return image_paths


def display_single_plot(criteria: str, parameter: str, drop_percent: dict):
    # global tkinter_result

    fig, ax = plt.subplots()
    colors = ["#FF9933", "lightblue", "green"]
    ans = ax.bar(
        drop_percent.keys(),
        drop_percent.values(),
        label=drop_percent.keys(),
        color=colors,
        align="center",
    )
    fig.suptitle(f"{parameter} DROPOUT ANALYSIS", c="#FF9933", fontweight="bold")
    ax.set_xticks(range(len(drop_percent.keys())))
    ax.set_xlabel(f"{criteria} CRITERION", c="green", fontweight="bold")
    ax.set_ylabel("PERCENTAGE", c="green", fontweight="bold")
    ax.bar_label(ans, padding=0, fmt="%.2f")

    buffer = BytesIO()
    ax.get_figure().savefig(buffer, format="png")
    buffer.seek(0)
    image_path = "D:\CBIT-Projects\sih23_final_fr\sih23\static/plot_single.png"

    with open(image_path, "wb") as img_file:
        img_file.write(buffer.read())

    ax.get_figure().clf()
    plt.close(ax.get_figure())

    # tkinter_result = image_path
    return image_path


if __name__ == "__main__":
    app.run(debug=True)
