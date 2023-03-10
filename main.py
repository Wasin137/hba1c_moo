import streamlit as st
import pandas as pd
import xgboost as xgb
import numpy as np

st.header('Predict HbA1c Level by your Blood Group and Birthday (Just for FUN!)')
inp_name = st.text_input('Enter you Name:', key="name")

#Load model
model = xgb.XGBRegressor(objective='reg:squarederror', learning_rate=0.1, max_depth=3, n_estimators=100)
model.load_model('hba1c_model.json')


st.subheader('Select your blood group')
left_column, right_column = st.columns(2)
with left_column:
    inp_abo = st.radio('Blood group:', ['A', 'B', 'AB', 'O'])

st.subheader('Select your birthday')
left_column, right_column = st.columns(2)
with left_column:
    inp_day = st.radio('Day:', ['monday', 'tuesday', 'wednesday','thursday', 'friday','saturday', 'sunday'])

st.subheader('Select your birth month')
left_column, right_column = st.columns(2)
with left_column:
    inp_month = st.radio('Month:', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

def make_inp(inp_abo, inp_day, inp_month):
    keys = ['ABOGROUP_A', 'ABOGROUP_AB', 'ABOGROUP_B', 'ABOGROUP_O', 'weekday_friday', 'weekday_monday', 'weekday_saturday', 'weekday_sunday', 'weekday_thursday', 'weekday_tuesday', 'weekday_wednesday', 'month_April', 'month_August', 'month_December', 'month_February', 'month_January', 'month_July', 'month_June', 'month_March' ,'month_May', 'month_November', 'month_October', 'month_September']
    feature_dict = dict.fromkeys(keys, 0)
    for k in feature_dict.keys():
        if k == f"ABOGROUP_{inp_abo}":
            feature_dict[k] = 1
        elif k == f"weekday_{inp_day}":
            feature_dict[k] = 1
        elif k == f"month_{inp_month}":
            feature_dict[k] = 1
        else:
            feature_dict[k] = 0
    cols_order = ['ABOGROUP_A', 'ABOGROUP_B', 'ABOGROUP_AB', 'ABOGROUP_O', 'weekday_friday', 'weekday_monday', 'weekday_saturday', 'weekday_sunday', 'weekday_thursday', 'weekday_tuesday', 'weekday_wednesday', 'month_January', 'month_February', 'month_March', 'month_April', 'month_May', 'month_June', 'month_July', 'month_August', 'month_September', 'month_October', 'month_November', 'month_December']
    feature_df = pd.DataFrame.from_dict(feature_dict, orient='index', columns=['value'])
    feature_df = feature_df.transpose().reset_index(drop=True)
    feature_df = feature_df[cols_order]
    return feature_df

if st.button('Make Prediction'):
    feature_to_predict = make_inp(inp_abo, inp_day, inp_month)
    prediction = model.predict(feature_to_predict)
    print('Your predicted HbA1c', prediction)
    st.write(f'{inp_name} predicted Hba1c is: {prediction} mg/dl')

