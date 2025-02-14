# for basic operations
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import io
#import matplotlib as plt

# for providing path
import os

# Enable logging for gensim - optional
import logging
import warnings

# Load dataset
#@st.cache_data


def main():
    # Main Page Design
    st.title(':mailbox_with_mail: :blue[TESIS]')
    st.header('_:blue[Text Classification Model]_')
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Exploratory Data Analysis :", ["*****-----*****-----*****-----*****", 
                                                          "Statistic Descriptive", 
                                                          "Check Data Distributions",
                                                          "Data Prepocessing"])
    
    # Menu Functions
    st.set_option('deprecation.showPyplotGlobalUse', False)
    if menu == "*****-----*****-----*****-----*****":
       st.write('''TESIS is a data science project ...''')
    if menu == "Statistic Descriptive":
       st.write('''menu00 ...''')   
    if menu == "Check Data Distributions":
       st.write('''menu01 ...''')
if __name__=="__main__":
    main()
