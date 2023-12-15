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
            date[k] = tmp.sum() / tmp.shape[0] if tmp.shape[0] else 0
    new_df = pd.DataFrame(zip(date.keys(), date.values()), columns=['Mois', f"{col}_per_station"])
    return new_df


def time_gap(data):
    dates = df.sort_values(by="Date", ascending=True)["Date"].tolist()
    gaps = [(dates[i]-dates[i-1]).days for i in range(1, len(dates))]
    x = list(range(1, len(dates)))
    new_data = pd.DataFrame(zip(x, gaps), columns=["Station", "Jours"])
    return new_data


if __name__ == "__main__":

    df = load_csv()
    
    # Charts
    st.write(f"Voici un récapitulatif de mes dépenses en carburant depuis le {beggining(df)}")

    st.title("Suivi des dépenses dans le temps")

    st.write("Nombre de jours entre deux achats en station")
    st.line_chart(time_gap(df), x='Station', y='Jours')
    
    st.write("### Prix du litre d'essence")
    st.scatter_chart(
        df,
        x='Date',
        y='Prix_litre',
        color='Carburant'
    )

    st.write("### Prix de l'essence à la station")
    st.scatter_chart(
        df,
        x='Date',
        y='Prix',
        color='Carburant'
    )

    st.write("### Volume d'essence pris")
    st.bar_chart(
        df,
        x='Date',
        y='Volume',
        color='Carburant'
    )

    st.title("Consommation totale par mois")
    st.write("### Volume d'essence par mois")
    st.bar_chart(
        sum_per_month(df, 'Volume'),
        x='Mois',
        y='Volume'
    )

    st.write("### Prix total de l'essence achetée par mois")
    st.bar_chart(
        sum_per_month(df, 'Prix'),
        x='Mois',
        y='Prix'
    )

    st.title("Consommation moyenne par mois")
    st.write("### Coût moyen de l'essence par mois")
    st.bar_chart(
        mean_per_station(df, "Prix"),
        x="Mois",
        y="Prix_per_station"
    )

    st.write("### Volume moyen d'essence par station par mois")
    st.bar_chart(
        mean_per_station(df, 'Volume'),
        x='Mois',
        y='Volume_per_station'
    )

    # Sidebar
    with st.sidebar.header("Sommaire"):
        st.sidebar.markdown("[Suivi des dépenses dans le temps](#2e66de86)")
        st.sidebar.markdown("[Consommation totale par mois](#consommation-totale-par-mois)")
        st.sidebar.markdown("[Consommation moyenne par mois](#consommation-moyenne-par-mois)")
        