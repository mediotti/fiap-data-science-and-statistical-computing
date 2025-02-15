import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('Social Media Performance')
st.text('This dashboard displays social media performance metrics')

file = st.file_uploader('Submit the file (.csv)')

if file:
    df = pd.read_csv(file)
    fig, ax = plt.subplots(1,1)
    ax.scatter(x=df['Reach'], y=df['Likes'])
    ax.set_xlabel("Reach")
    ax.set_ylabel("Likes")
    
    st.write(df)

    st.pyplot(fig)