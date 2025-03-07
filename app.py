import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import keras
import joblib

# Load the trained model
scaler = joblib.load('standard_scaler.pkl')
load_diabetes = joblib.load('load_diabetes.pkl')
model = keras.models.load_model('model.h5', compile=False)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# CSS for loading the font
st.markdown(
    """
    <style>
    body {
        direction: rtl;
    }
    .high-risk {
        background-color: red;
        color: white;
        padding: 7px;
        border-radius: 8px;
        display: inline-block;
    }
    .low-risk {
        background-color: green;
        color: white;
        padding: 7px;
        border-radius: 8px;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Menu options
st.sidebar.header("انتخاب زبان :", divider='rainbow')
language = st.sidebar.radio("", ("فارسی","English"))


# Sidebar setup



if language == "فارسی":
    st.sidebar.header("منو :", divider='rainbow')
    menu = st.sidebar.radio("یک گزینه را انتخاب کنید:", ("Home", "Plots", "About Project"))
    
    st.sidebar.header("**توسعه داده شده توسط :**", divider='rainbow')
    st.sidebar.write("امید حقایق (پاییز 1403)")
else:
    st.sidebar.header("Menu :", divider='rainbow')
    menu = st.sidebar.radio("Select a section:", ("Home", "Plots", "About Project"))
    st.sidebar.header("**Developed by :**", divider='rainbow')
    st.sidebar.write("Omid Haghayegh (Fall 2024)")



if menu == "Home":
    if language == "فارسی":
        st.title("برنامه پیش‌بینی دیابت")
        st.write("""
        این برنامه خطر دیابت را بر اساس چندین ویژگی ورودی پیش‌بینی می‌کند.
        لطفاً جزئیات زیر را وارد کنید تا پیش‌بینی دریافت کنید.
        """)
        
        gender = st.selectbox("جنسیت", ("زن", "مرد"))
        gender_convert = 0 if gender == "زن" else 1
        age = st.number_input('سن',step=1,format="%d")

        hypertension = st.selectbox("فشار خون بالا", ("خیر", "بله"))
        hypertension_convert = 0 if hypertension == "خیر" else 1

        heart_disease = st.selectbox("بیماری قلبی", ("خیر", "بله"))
        heart_disease_convert = 0 if heart_disease == "خیر" else 1

        bmi = st.number_input('شاخص توده بدن (BMI)')
        HbA1c_level = st.number_input('سطح HbA1c')
        blood_glucose_level = st.number_input('سطح قند خون')

    else:
        st.title("Diabetes Prediction Application")
        st.write("""
        This application predicts the diabetes risk based on several input features.
        Please enter the details below to get a prediction.
        """)

        gender = st.selectbox("Gender", ("Female", "Male"))
        gender_convert = 0 if gender == "Female" else 1
        age = st.number_input('Age',step=1,format="%d")
        # age = st.slider("Age", 0, 100)

        hypertension = st.selectbox("Hypertension", ("No", "Yes"))
        hypertension_convert = 0 if hypertension == "No" else 1

        heart_disease = st.selectbox("Heart Disease", ("No", "Yes"))
        heart_disease_convert = 0 if heart_disease == "No" else 1

        bmi = st.number_input('BMI')
        HbA1c_level = st.number_input('HbA1c Level')
        blood_glucose_level = st.number_input('Blood Glucose Level')

    # Prepare the input for prediction
    input_data = np.array([[gender_convert, age, hypertension_convert, heart_disease_convert, bmi, HbA1c_level, blood_glucose_level]])
    
    # Standardize the input data
    standardized_input = scaler.transform(input_data)

    # دکمه پیش‌بینی با توجه به زبان
    button_label = 'پیشبینی' if language == "فارسی" else 'Predict'
    if st.button(button_label, key='predict_button'):
        prediction = model.predict(standardized_input)
        
        if language == "English":
            if prediction[0].item() > 0.5:
                st.markdown('<div class="high-risk">High Risk</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="low-risk">Low Risk</div>', unsafe_allow_html=True)

            st.write(f"The probability of having diabetes is: {prediction[0].item() * 100:.2f} Percent")
            st.write(f"The probability of not having diabetes is: {(1 - prediction[0].item()) * 100:.2f} Percent")

        else:
            if prediction[0].item() > 0.5:
                st.markdown('<div class="high-risk">پرخطر</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="low-risk">کم خطر</div>', unsafe_allow_html=True)

            st.write(f"احتمال دیابت: {prediction[0].item() * 100:.2f} %")
            st.write(f"احتمال عدم دیابت: {(1 - prediction[0].item()) * 100:.2f} %")

elif menu == "Plots":
    diabetes = load_diabetes
    plt.title('Heatmap of Diabetes Dataset Features')
    sns.heatmap(diabetes[['diabetes', 'age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'gender', 'heart_disease', 'hypertension']].corr(),
                 annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Heatmap of Diabetes Dataset Features')
    st.pyplot(plt)