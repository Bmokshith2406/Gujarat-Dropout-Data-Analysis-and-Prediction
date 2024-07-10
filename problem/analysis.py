from io import BytesIO
from PIL import Image
import pandas
from matplotlib import pyplot as plt


def analyse(DF: pandas.DataFrame, key: str = "STATE", on="GUJARAT", cat="all"):
    # if key != "AREA":
    #     key = key.upper()
    #     on = on.upper()
    # Dict = {"ACADEMIC": 0, "MOVED": 0, "POVERTY": 0, "OTHERS": 0}
    # Dict_percentages = {}
    # Gender = {"MALE": 0, "FEMALE": 0}
    # Gender_Percent = {}
    # Standard_Dict = {
    #     1: 0,
    #     2: 0,
    #     3: 0,
    #     4: 0,
    #     5: 0,
    #     6: 0,
    #     7: 0,
    #     8: 0,
    #     9: 0,
    #     10: 0,
    #     11: 0,
    #     12: 0,
    # }
    # Standard_Dictper = {}
    # Caste = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    # Casteper = {}
    # for i in range(len(DF)):
    #     if (DF.loc[i, key] == on) and ((DF.loc[i, "GRADE"]) < 4):
    #         class_drops = DF.loc[i, "CLASS/STANDARD"]
    #         Standard_Dict[class_drops] += 1
    #         caste_drops = DF.loc[i, "CASTE"]
    #         Caste[str(caste_drops)] += 1
    #         if DF.loc[i, "GRADE"] != 0:
    #             Dict["ACADEMIC"] += 1
    #         if (DF.loc[i, "GENDER"]) == "M":
    #             Gender["MALE"] += 1
    #         if (DF.loc[i, "GENDER"]) == "F":
    #             Gender["FEMALE"] += 1
    #         if DF.loc[i, "GRADE"] == 0:
    #             if DF.loc[i, "MOVED"] == "YES":
    #                 Dict["MOVED"] += 1
    #             elif DF.loc[i, "OTHERS"] == "YES":
    #                 Dict["OTHERS"] += 1
    #             elif DF.loc[i, "POVERTY"] == "YES":
    #                 Dict["POVERTY"] += 1

    # q, r, s, t = (
    #     sum(Dict.values()),
    #     sum(Standard_Dict.values()),
    #     sum(Caste.values()),
    #     sum(Gender.values()),
    # )

    # if sum(Dict.values()) == 0:
    #     q = 1

    # for i in Dict.keys():
    #     percentage = (Dict[i] / q) * 100
    #     Dict_percentages[i] = percentage

    # if sum(Standard_Dict.values()) == 0:
    #     r = 1

    # for i in Standard_Dict.keys():
    #     percentage = (Standard_Dict[i] / r) * 100
    #     Standard_Dictper[i] = percentage

    # if sum(Caste.values()) == 0:
    #     s = 1

    # for i in Caste.keys():
    #     percentage = (Caste[i] / s) * 100
    #     Casteper[i] = percentage

    # if sum(Gender.values()) == 0:
    #     t = 1

    # for i in Gender.keys():
    #     percentage = (Gender[i] / t) * 100
    #     Gender_Percent[i] = percentage
    # criteria = ["REASON", "CLASS/STANDARD", "CASTE", "GENDER"]
    # data = [Dict_percentages, Standard_Dictper, Casteper, Gender_Percent]

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

    if cat == "all":
        display_all(criteria, on, data)
    else:
        cats = zip(criteria, data)
        return display(cat, on, data[criteria.index(cat)])

def display(criteria, parameter: str, drop_percent: dict):
    fig, ax = plt.subplots(layout="tight")
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
    ax.bar_label(ans, padding=2, fmt="%.2f")
    # # Save the Matplotlib plot as an image
    # buffer = BytesIO()
    # plt.savefig(buffer, format="png")
    # buffer.seek(0)
    # # Clear the Matplotlib plot to avoid conflicts
    # plt.clf()
    # plt.close()
    # # Return a PNG image object
    # img = Image.open(buffer).convert('RGB')
    # return img
def display_all(criteria: str, parameter: str, data: list[dict]):
  fig, ax = plt.subplots(2, 2, layout='constrained')

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
      axis.bar_label(bars, padding=2, fmt="%.2f")    

if __name__ == "__main__":
    df = pandas.read_csv(
        "C:/Users/Ajay/AppData/Roaming/Python/Python312/sih23/gujarat_db.csv"
    )
    key = input("ANALYSIS BASED ON: ")
    on = input(f"{key}: ") if key != "AREA" else int(input(f"{key}: "))

    print(analyse(df, key, on))

    plt.show()
    print(type(list()))
