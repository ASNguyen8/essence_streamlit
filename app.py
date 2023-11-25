import streamlit as st
import pandas as pd

if __name__ == "__main__":

    path = "https://github.com/ASNguyen8/ASNguyen8.github.io/blob/ddd074b228ed447560a290ae76e75ff053be78ca/docs/essence.csv"

    df = pd.read_csv(path, delimiter=";")
    date = df["Date"]
    prix_litre = df["Prix_litre"]
    st.write("Prix du litre d'essence (€)", prix_litre.sort_index)
    
    
    print("Hello world")