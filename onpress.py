# for basic operations
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import io
import matplotlib as plt

# for providing path
import os

# Enable logging for gensim - optional
import logging
import warnings

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("rawJan25.xlsx")
    df = df.drop('No', axis=1)
    return df
df = load_data()

def main(df):
    # Main Page Design
    st.title(':mailbox_with_mail: :blue[TESIS]')
    st.header('_:blue[Text Classification Model]_')
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Exploratory Data Analysis :", ["*****-----*****-----*****-----*****", 
                                                          "Statistic Descriptive", 
                                                          "Check Data Distributions",
                                                          "Data Prepocessing"])
    
    menu2 = st.sidebar.selectbox("Modeling:", ["*****-----*****-----*****-----*****", 
                                                     "LED K-Means", 
                                                     "LDA Model",
                                                     "Model Evaluation"])
    # Menu Functions
    st.set_option('deprecation.showPyplotGlobalUse', False)
    if menu == "*****-----*****-----*****-----*****" and menu2 == "*****-----*****-----*****-----*****" :
       st.write('''TESIS is a data science project ...''')
    if menu == "Statistic Descriptive" and menu2 == "*****-----*****-----*****-----*****" :
       st.write('''menu00 ...''')   
    if menu == "Check Data Distributions" :
       st.write('''menu01 ...''')
