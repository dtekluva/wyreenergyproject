import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime


# # SAMPLE KWATT DATA CLEANING
def predict_usage(values, cdd, test_cdd, num_of_required_months = 6, reproccess = True):# Reprocess True if the monthly kwatt-hour value is not yet determined
    print(values, cdd)
    #DATA ARRANGEMENT

    x = np.array(cdd).reshape((-1, 1))
    y = np.array(values)

    # if len(x) < num_of_required_months: return 0

    # try:
    model = LinearRegression()
    model = LinearRegression().fit(x, y)

    r_sq = model.score(x, y)

    predictions = model.predict(x)

    intercept = model.intercept_
    slope = model.coef_

    def get_lower_points(slope, intercept, x, y): #GET ALL POINTS BENEATH THE REGRESSION LINE
        
        lower_points = []
        
        for value, actual_y in zip(x,y):
            
            predicted_y = slope[0] * value + intercept
            if predicted_y >= actual_y:
                lower_points.append((value,actual_y))
        
        return lower_points



    lower_points = get_lower_points(intercept=intercept, slope=slope, x=cdd, y = values)

    adjusted_baseline = pd.DataFrame(lower_points, columns=["cdd", "kwatts"])

    a = np.array(adjusted_baseline["cdd"]).reshape((-1, 1))
    b = np.array(adjusted_baseline["kwatts"])

    adjusted_model = LinearRegression()
    adjusted_model = LinearRegression().fit(a, b)

    r_sq = model.score(a, b)

    current_month_prediction = model.predict([[test_cdd]])[0]

    return current_month_prediction

    # except ValueError:

    #     return 0



# # # SAMPLE KWATT DATA CLEANING
# def predict_usage(values, cdd, reproccess = True):# Reprocess True if the monthly kwatt-hour value is not yet determined

#     #DATA ARRANGEMENT

#     kwatts = pd.DataFrame(values, columns = ["date", "raw_kw_hrs"])
    

#     kwatts.date = pd.to_datetime(kwatts.date, format="%m/%d/%Y")

#     max_monthly_kwatt_hrs = kwatts.resample(rule="m", on= "date").max()
#     min_monthly_kwatt_hrs = kwatts.resample(rule="m", on= "date").min()
#     monthly_kwatts        = kwatts.resample(rule="m", on= "date").sum()

#     monthly_kwatts["kwatts"] = (max_monthly_kwatt_hrs.raw_kw_hrs - min_monthly_kwatt_hrs.raw_kw_hrs)

#     monthly_kwatts = monthly_kwatts.reset_index()
#     monthly_kwatts["week"] = monthly_kwatts.date.dt.month


#     # # ANALYSIS SECTION

#     data = pd.DataFrame(cdd, columns=['Date', 'CDD'])
#     new_data = data.copy()
#     new_data["Date"] = pd.to_datetime(new_data.Date, dayfirst=True)
#     new_data = new_data.resample(rule = "m", on = "Date").sum().reset_index()
#     new_data["month"] = new_data.Date.dt.month

#     this_month = datetime.datetime.now().month #GET CURRENT MONTH 
#     current_month_cdd = float(new_data.loc[new_data['month'] == this_month].CDD) #GET CORRESPONDING CDD FOR CURRENT MONTH

#     new_data = new_data[(len(new_data) - len(monthly_kwatts)):] ##MATCH NUMBER OF CDD TO NUMBER OF KWATTS READINGS


#     def create_name(row):
#         return f"{row.month}, {row.year}"

#     new_dates = new_data.Date.apply(create_name)
#     new_data["new_dates"] = new_dates

#     grouped_data = new_data.reset_index(inplace=False)

#     monthly_kwatts["cdd"] =  grouped_data["CDD"]
#     monthly_kwatts =  monthly_kwatts.tail(6)

#     x = np.array(monthly_kwatts.cdd).reshape((-1, 1))
#     y = np.array(monthly_kwatts['kwatts'])

#     try:
#         model = LinearRegression()
#         model = LinearRegression().fit(x, y)

#         r_sq = model.score(x, y)

#         predictions = model.predict(x)

#         intercept = model.intercept_
#         slope = model.coef_

#         def get_lower_points(slope, intercept, x, y): #GET ALL POINTS BENEATH THE REGRESSION LINE
            
#             lower_points = []
            
#             for value, actual_y in zip(x,y):
                
#                 predicted_y = slope[0] * value + intercept
#                 if predicted_y >= actual_y:
#                     lower_points.append((value,actual_y))
            
#             return lower_points



#         lower_points = get_lower_points(intercept=intercept, slope=slope, x=monthly_kwatts['cdd'], y = monthly_kwatts['kwatts'])

#         adjusted_baseline = pd.DataFrame(lower_points, columns=["cdd", "kwatts"])

#         a = np.array(adjusted_baseline["cdd"]).reshape((-1, 1))
#         b = np.array(adjusted_baseline["kwatts"])

#         adjusted_model = LinearRegression()
#         adjusted_model = LinearRegression().fit(a, b)

#         r_sq = model.score(a, b)

#         current_month_prediction = model.predict([[current_month_cdd]])[0]

#         return current_month_prediction

#     except ValueError:

#         return 0



