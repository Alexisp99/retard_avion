import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import streamlit.components.v1 as components
import requests
import json
import pymysql

# Configurer l'application Streamlit
st.set_page_config(page_title="NB_RECO", page_icon="🧊", layout="wide")

# connection avec le ficjier css
def local_css(file_name):
    with open(file_name) as c:
        st.markdown(f'<style>{c.read()}</style>', unsafe_allow_html=True)

local_css("style.css")


# # get the data
# @st.cache_data
# def get_data():
#     url = "data/df.csv"
#     return pd.read_csv(url)

# df = get_data()


# ajouter une image
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://media.istockphoto.com/id/155439315/fr/photo/avion-de-passagers-voler-au-dessus-des-nuages-au-coucher-du-soleil.jpg?s=612x612&w=0&k=20&c=LRxXZHvGfbWnAM_ELCPbFHI9gdqJXDRqIy3xOM7m5tg=");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


with st.container():
    selected = option_menu(
        menu_title=None,
        options=["HOME", "MODEL INSIGHTS"],
        icons=['house', 'cloud-upload'],
        menu_icon="cast",
        orientation="horizontal",
        styles={
            "nav-link": {
                "text-align": "left",
                "--hover-color": "#6CDFDF",
            },

            "nav-link-selected": {"background-color": "#6CDFDF"},


        }
    )


    # container
    with st.container():


        if selected == 'HOME':

            st.write("""
            <div style="text-align:center">
                <h1>FLIGHT DELAY</h1>
            </div>
            """, unsafe_allow_html=True)

            st.write("""
            <div style="text-align:center">
                <h3>An app capable of predicting flight delays</H3>
            </div>
            """, unsafe_allow_html=True)

            # Créer un conteneur principal avec une largeur de 800 pixels et une hauteur de 600 pixel

            # Ajouter une colonne centrale à l'intérieur du conteneur principal
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Ajouter le formulaire ici
                st.write("""
                <div style="text-align:center">
                    <h3>Renseignez quelques informations sur votre vol</H3>
                </div>
                """, unsafe_allow_html=True)
                QUARTER = st.text_input("QUARTER")
                DAY_OF_MONTH = st.text_input("DAY_OF_MONTH")
                DAY_OF_WEEK = st.text_input("DAY_OF_WEEK")
                MONTH = st.text_input('MONTH')
                CRS_DEP_TIME = st.text_input('CRS_DEP_TIME')
                DEP_DELAY = st.text_input('DEP_DELAY')
                CRS_ARR_TIME = st.text_input('CRS_ARR_TIME')
                DISTANCE = st.text_input('DISTANCE')
                st.write("")
                m = st.markdown("""
                <style>
                div.stButton{
                display:block;
                margin-left: 330px;}
                </style>""", unsafe_allow_html=True)
                predict_button = st.button("PREDICT")


            if predict_button:

                ####################requests#####################
                headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                }


                data = json.dumps({
                    "QUARTER": QUARTER,
                    "DAY_OF_MONTH": DAY_OF_MONTH,
                    "DAY_OF_WEEK": DAY_OF_WEEK,
                    "MONTH": MONTH,
                    "CRS_DEP_TIME": CRS_DEP_TIME,
                    "DEP_DELAY": DEP_DELAY,
                    "CRS_ARR_TIME": CRS_ARR_TIME,
                    "DISTANCE": DISTANCE
                })


                response = requests.get('https://bloublouplane.azurewebsites.net/predict', headers=headers, data=data)


                co1, co2, co3 = st.columns([1, 2, 1])

                with co2:

                    st.write("""
                    <div style="text-align:center">
                        <h2>Predictions</h2>
                    <  </div>
                    """, unsafe_allow_html=True)

                    if response.status_code == 200:
                        result = response.json()
                        if result['prediction'] == 0:
                            st.write(f"""
                            <div style="text-align:center">
                                <h3>Votre avion arrivera à l'heure !</H3>
                            </div>
                            """, unsafe_allow_html=True)
                        else :
                            st.write(f"""
                            <div style="text-align:center">
                                <h3>Votre avion aura du retard !</H3>
                            </div>
                            """, unsafe_allow_html=True)

                        st.write(f"""
                        <div style="text-align:center">
                            <h3>The probability of a delay is {result['probability']:.2%}</h3>
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.write(f"Error: {response.status_code} - {response.text}")


                # data = '{f"QUARTER": {QUARTER},"MONTH": {MONTH},"DAY_OF_MONTH": {DAY_OF_MONTH},"DAY_OF_WEEK": {DAY_OF_WEEK}, "CRS_DEP_TIME": {CRS_DEP_TIME}, "DEP_DELAY": {DEP_DELAY}, "CRS_ARR_TIME": {CRS_ARR_TIME}, "DISTANCE":{DISTANCE}}


        if selected == 'MODEL INSIGHTS':

            st.write("""
                <div style="text-align:center">
                    <h1>MODEL INSIGHTS</h1>
                </div>
            """, unsafe_allow_html=True)

            st.write("""
                <div style="text-align:center">
                    <h3>Everything you need to know about our model</H3>
                </div>
            """, unsafe_allow_html=True)

            # with st.container():
            #     col_1, col_2 = st.columns(2, gap="large")

            #     with col_1:

            #         st.title("")
            #         st.title("")
            #         st.header("")
            #         tab1, tab2 = st.tabs(["Temps de retard du vol par rapport à la distance du vol",
            #                             "Distance moyenne d'un vol pour chaque mois"])

            #         with tab1:
            #             # tracer le scatter plot
            #             fig, ax = plt.subplots(figsize=(6, 5))
            #             sns.scatterplot(x="DISTANCE", y="DEP_DELAY", hue="ARR_DEL15", data=df, palette=[ "#7FFFD4" ,"#6CDFDF"])
            #             plt.title("Temps de retard du vol par rapport à la distance du vol")
            #             plt.ylabel("Retard ( en min )")
            #             # fig.set_size_inches(6, 3)
            #             st.pyplot(fig)

            #         with tab2:
            #         # Créer le plot avec Seaborn
            #             fig, ax = plt.subplots(figsize=(6, 5))
            #             sns.lineplot(x='MONTH', y='DISTANCE', data=df, color='#7FFFD4')

            #             # Ajouter un titre
            #             plt.title("Distance moyenne d'un vol pour chaque mois")
            #             # fig.set_size_inches(6, 3)
            #             st.pyplot(fig)

            #     with col_2:

            #         st.title("")
            #         st.header("")
            #         st.header("")
            #         st.header("")
            #         st.header("")
            #         # pie chart
            #         # calculer le nombre de vols en retard
            #         delayed = df[df["ARR_DEL15"] == 1]
            #         ontime = df[df["ARR_DEL15"] == 0]
            #         num_delayed = len(delayed)
            #         num_ontime = len(ontime)

            #         # créer le pie chart
            #         labels = ["DELAYED", "ONTIME"]
            #         sizes = [num_delayed, num_ontime]
            #         colors = [ "#7FFFD4" ,"#6CDFDF"]

            #         fig, ax = plt.subplots(figsize=(5,5))
            #         ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
            #         # Modifier la taille du titre
            #         plt.title("Total d'avion en retard en pourcentage", fontsize=12)

            #         # Modifier la taille des pourcentages
            #         ax.legend(labels, title="Legend", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10, title_fontsize=12)
            #         st.pyplot(fig)


conn = pymysql.connect(
    host="dbplaneap.mysql.database.azure.com",
    user="alexisp",
    password="roadtrip99!",
    database="plane"
)
st.write(conn)
