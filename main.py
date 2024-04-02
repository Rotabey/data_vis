import streamlit as st
from utils import scatter_plot_for_year, plot_top_10_ranks_evolution, plot_map, plot_top_countries_map, \
    plot_percentage_ring
import pandas as pd
import geopandas as gpd

data = pd.read_csv('data/publications_scientifiques_par_pays.csv')

country_name_mapping = {
    "United States": "United States of America",
    "Russian Federation": "Russia",
    "Hong Kong": "Hong Kong S.A.R.",
    "Czech Republic": "Czechia",
    "South Korea": "Korea, South",
    "Taiwan": "Taiwan*",
    "Egypt": "Egypt, Arab Rep.",
    "Iran": "Iran, Islamic Rep.",
    "Netherlands Antilles": "Netherlands",
    "Palestine ": "West Bank and Gaza",
    "Syrian Arab Republic": "Syria",
    "Côte d'Ivoire": "Cote d'Ivoire",
    "Congo": "Congo, Dem. Rep.",
    "Democratic Republic Congo": "Congo, Rep.",
    "Viet Nam": "Vietnam",
    "Moldova": "Moldova, Rep.",
    "North Korea": "Korea, North",
    "Falkland Islands (Malvinas)": "Falkland Islands",
    "French Southern Territories": "French Southern and Antarctic Lands",
    "Saint Helena": "Saint Helena, Ascension and Tristan da Cunha"
}

data['Country'] = data['Country'].map(country_name_mapping).fillna(data['Country'])
world = gpd.read_file('data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

st.set_page_config(layout="wide")
st.title('Publications scientifiques par pays')
st.write('')
tabs = st.tabs(["Tableau de données", "Nuage de Points", "Évolution des Rangs", "Carte Top 10", "Carte H-index"])

with tabs[0]:
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Trie des données</h2>",
        unsafe_allow_html=True)
    st.write(data)
# Afficher le nuage de points avec les filtres appliqués
with tabs[1]:
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Nuage de Points: Documents vs Citations</h2>",
        unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3], gap="large")
    with col1:
        st.subheader('Filtres')
        selected_year_slider_key = "selected_year_slider"
        selected_year = st.slider('Sélectionner une année', min_value=data['Year'].min(), max_value=data['Year'].max(),
                                  value=data['Year'].min(), key=selected_year_slider_key)
        min_docs_filter, max_docs_filter = st.slider("Nombre de documents (fourchette)",
                                                     min_value=0,
                                                     max_value=400000,
                                                     step=1000,
                                                     value=(0, 400000))
        min_citations_filter, max_citations_filter = st.slider("Nombre de citations (fourchette)",
                                                               min_value=0,
                                                               max_value=11000000,
                                                               step=1000,
                                                               value=(0, 11000000))
    with col2:
        scatter_plot_for_year(data, selected_year, min_docs_filter, max_docs_filter, min_citations_filter,
                              max_citations_filter)

with tabs[2]:
    st.markdown("<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Évolution des Rangs des Pays</h2>",
                unsafe_allow_html=True)
    top_10_ranks = data[data['Rank'] <= 10]
    plot_top_10_ranks_evolution(top_10_ranks)


with tabs[3]:
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Carte des pays du top 10 selon le nombre de documents produits</h2>",
        unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1], gap="large")
    with col1:
        st.subheader('Filtres')
        selected_year_slider_key_2 = "selected_year_slider_2"  # Utilisez une clé distincte
        selected_year_2 = st.slider('Sélectionner une année', min_value=data['Year'].min(),
                                    max_value=data['Year'].max(), value=data['Year'].min(),
                                    key=selected_year_slider_key_2)
    with col2:
        plot_top_countries_map(data, world, 10, selected_year_2)
    with col3:
        st.subheader('Classement des 10 premiers pays par rang ')

        # Filtrer les données pour l'année sélectionnée et sélectionner les 10 premiers pays par rang
        filtered_data = data[data['Year'] == selected_year_2][['Country', 'Rank', 'Documents']].sort_values(
            by='Rank').head(
            10).reset_index(drop=True)

        # Convertir le DataFrame en HTML en masquant les index
        html_table = filtered_data.to_html(index=False)

        # Afficher le tableau HTML dans Streamlit
        st.markdown(html_table, unsafe_allow_html=True)

with tabs[4]:
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Carte des pays selon le H-index</h2>",
        unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1], gap="large")
    with col1:
        st.subheader('Filtres')
        selected_year_slider_key_3 = "selected_year_slider_3"
        selected_year_3 = st.slider('Sélectionner une année', min_value=data['Year'].min(),
                                    max_value=data['Year'].max(), value=data['Year'].min(),
                                    key=selected_year_slider_key_3)

        # Ajout du filtre pour l'indice H
        h_index_slider_key = "h_index_slider"
        h_index_range = st.slider('Sélectionner une fourchette pour l\'indice H',
                                  min_value=data['H.index'].min(),
                                  max_value=data['H.index'].max(),
                                  value=(data['H.index'].min(), data['H.index'].max()),
                                  key=h_index_slider_key)

    with col2:
        plot_map(selected_year_3, h_index_range[0], h_index_range[1], data,
                 world)  # Passer les valeurs des filtres à la fonction plot_map
    with col3:
        st.subheader(
            f'Le pourcentage de pays qui ont un H-index entre  {h_index_range[0]} et {h_index_range[1]} pour l\'année {selected_year_3}')
        fig = plot_percentage_ring(selected_year_3, h_index_range[0], h_index_range[1],
                                   data)  # Appeler la fonction avec les bons paramètres
        st.pyplot(fig)  # Afficher la figure à l'aide de st.pyplot
