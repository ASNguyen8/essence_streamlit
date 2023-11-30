import pandas as pd
import streamlit as st
import datetime as dt

path = "https://raw.githubusercontent.com/ASNguyen8/ASNguyen8.github.io/master/docs/essence.csv"

fr_months = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]


def load_csv():
    data = pd.read_csv(path, sep=";")
    data = data[data['Pays'] == 'France']
    data['Date'] = data['Date'].apply(lambda x: dt.datetime.strptime(x, "%d/%m/%y"))
    return data


def beggining(data):
    date = data['Date'].iloc[0]
    return f"{date.day} {fr_months[date.month - 1]} {date.year}"


def sum_per_month(data, col: str):
    
    years = list(set([row.year for row in data['Date']]))
    date = {}
    for year in years:
        for m in range(1, 13):
            k = f"{year}-{'0'*(m<10)}{m}"
            date[k] = data[col][(data['Date'].dt.year == year) & (data['Date'].dt.month == m)].sum()
    new_df = pd.DataFrame(zip(date.keys(), date.values()), columns=['Mois', col])
    return new_df
    

def mean_per_station(data, col: str):
    
    years = list(set([row.year for row in data['Date']]))
    date = {}
    for year in years:
        for m in range(1, 13):
            k = f"{year}-{'0'*(m<10)}{m}"
            tmp = data[col][(data['Date'].dt.year == year) & (data['Date'].dt.month == m)]
            date[k] = tmp.sum() / tmp.shape[0]
    new_df = pd.DataFrame(zip(date.keys(), date.values()), columns=['Mois', f"{col}_per_station"])
    return new_df


if __name__ == "__main__":

    df = load_csv()
    
    # Charts
    st.write(f"""
    # Voici un récapitulatif de mes dépenses en carburant depuis le {beggining(df)}
    """)
    
    st.write("""
    ## Prix du litre d'essence
    """)
    st.scatter_chart(
        df,
        x='Date',
        y='Prix_litre',
        color='Carburant'
    )

    st.write("""
    ## Prix de l'essence à la station
    """)
    st.scatter_chart(
        df,
        x='Date',
        y='Prix',
        color='Carburant'
    )

    st.write("""
    ## Volume d'essence pris
    """)
    st.bar_chart(
        df,
        x='Date',
        y='Volume',
        color='Carburant'
    )

    st.write("""
    ## Volume d'essence par mois
    """)
    st.bar_chart(
        sum_per_month(df, 'Volume'),
        x='Mois',
        y='Volume'
    )

    st.write("""
    ## Prix de l'essence achetée par mois
    """)
    st.bar_chart(
        sum_per_month(df, 'Prix'),
        x='Mois',
        y='Prix'
    )

    st.write("""
    ## Volume moyen d'essence par station par mois
    """)
    st.bar_chart(
        mean_per_station(df, 'Volume'),
        x='Mois',
        y='Volume_per_station'
    )

    # Sidebar
    with st.sidebar.header("Sommaire"):
        st.sidebar.markdown("""
        [Prix du litre d'essence](#prix-du-litre-d-essence)
        """)
        st.sidebar.markdown("""
        [Prix de l'essence à la station](#2aa0251c)
        """)
        st.sidebar.markdown("""
        [Volume d'essence pris](#volume-d-essence-pris)
        """)
        st.sidebar.markdown("""
        [Volume d'essence par mois](#volume-d-essence-par-mois)
        """)
        st.sidebar.markdown("""
        [Prix de l'essence achetée par mois](#87e6d834)
        """)
        st.sidebar.markdown("""
        [Volume moyen d'essence par station par mois](#volume-moyen-d-essence-par-station-par-mois)
        """)
        