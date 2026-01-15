import streamlit as st
import pandas as pd
import joblib
import time

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

st.title('Diabetes Prediction')
with st.form("diabetes_form"):
    with st.expander("Enter your basic details"):
        col1,col2 = st.columns(2)
        with col1:
            gender = st.selectbox('Gender',['Female','Male','Other'])
            ethnicity = st.selectbox('Ethinicity',['White','Hispanic','Black','Asian','Other'])
            education_level = st.selectbox('Education Level',['Highschool','Graduate','Postgraduuate','No formal'])
        with col2:
            income_level = st.selectbox('Income Level',['Low','Lower-Middle','Middle','Upper-Middle','High'])
            smoking_status = st.selectbox('Smoking Status',['Never','Current','Former'])
            employment_status = st.selectbox('Employment Status',['Student','Unemployed','Employed','Retired'])

    with st.expander("Basic Health Information"):
        col1,col2 = st.columns(2)
        with col1:
            age = st.number_input('enter your age',min_value=19,max_value=90,step=1)
            diet_score = st.number_input('Enter your diet score',min_value=1,max_value=10,step=1)
        with col2:
            bmi = st.number_input('Enter your bmi',min_value=10,max_value=40,step=1,help="Body Mass Index = weight(kg) / height(m)^2")
            heart_rate = st.number_input('Enter your heart rate',min_value=30,max_value=110)

    with st.expander("Medical history"):
        family_history_diabetes = st.selectbox('Family Diabetes History',['Yes','No'])
        hypertension_history = st.selectbox('hypertension history',['Yes','No'])
        cardiovascular_history = st.selectbox('cardiovascular history',['Yes','No'])

    with st.expander("Enter some extra details"):
        col1,col2 = st.columns(2)
        with col1:
            physical_activity = st.number_input('enter your physical activity minutes per week',min_value=0,max_value=1200,step=1)
            waist_to_hip_ratio = st.number_input('Enter your waist to hip ratio')
            systolic_bp = st.number_input('Enter your systolic bp',min_value=80,max_value=170,step=1)
            diastolic_bp = st.number_input('Enter your diastolic bp',min_value=40,max_value=120,step=1)
        with col2:
            cholesterol_total = st.number_input("Enter your total cholesterol",min_value=100,max_value=300,step=1)
            hdl_cholesterol = st.number_input('Enter your hdl cholesterol',min_value=10,max_value=100,step=1)
            ldl_cholesterol = st.number_input('Enter your ldl cholesterol',min_value=40,max_value=220,step=1)
            triglycerides = st.number_input('Enter your triglycerides',min_value=20,max_value=300,step=1)
    submitted = st.form_submit_button("Check Diabetes Risk")



if submitted:
    mapping = {'Yes':1,'No':0}
    family_history_diabetes = mapping[family_history_diabetes]
    hypertension_history = mapping[hypertension_history]
    cardiovascular_history = mapping[cardiovascular_history]

    metabolic_risk = bmi*cholesterol_total
    bad_diet_bmi = bmi*(10-diet_score)
    lifestyle_risk = (bmi*cholesterol_total*(10-diet_score)) - physical_activity
    non_genetic_risk = lifestyle_risk*((1-family_history_diabetes)+(1-hypertension_history)+(1-cardiovascular_history))


    df = pd.DataFrame({
        'age':[age],
        'physical_activity_minutes_per_week':[physical_activity],
        'diet_score':[diet_score],
        'bmi':[bmi],
        'waist_to_hip_ratio':[waist_to_hip_ratio],
        'systolic_bp':[systolic_bp],
        'diastolic_bp':[diastolic_bp],
        'heart_rate':[heart_rate],
        'cholesterol_total':[cholesterol_total],
        'hdl_cholesterol':[hdl_cholesterol],
        'ldl_cholesterol':[ldl_cholesterol],
        'triglycerides':[triglycerides],
        'family_history_diabetes':[family_history_diabetes],
        'hypertension_history':[hypertension_history],
        'cardiovascular_history':[cardiovascular_history],
        'gender':[gender],
        'ethnicity':[ethnicity],
        'education_level':[education_level],
        'income_level':[income_level],
        'smoking_status':[smoking_status],
        'employment_status':[employment_status],
        'metabolic_risk':[metabolic_risk],
        'bad_diet_bmi':[bad_diet_bmi],
        'non_genetic_risk':[non_genetic_risk]
    })

    try:
        with st.spinner("Analyzing......"):
            prob = model.predict_proba(df)[0][1]
            time.sleep(1)
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)
        st.metric("Diabetes Risk Probability",f"{prob:.2%}")
        if(prob<0.25):
            st.success("You are safe")
        elif(prob>0.75):
            st.error("You have High Risk of diabetes")
        else:
            st.warning("You have Medium Risk")
        st.caption("Probability represents the model's confidence based on your inputs.")
    except Exception as e:
        st.error(f"Error:{e}")


