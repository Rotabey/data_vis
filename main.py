import streamlit as st
from utils import scatter_plot_for_year, plot_top_10_ranks_evolution, plot_map, plot_top_countries_map
import pandas as pd
import geopandas as gpd

data = pd.read_csv('data/publications_scientifiques_par_pays.csv')
data.loc[data['Country'] == 'United States', 'Country'] = 'United States of America'
world = gpd.read_file('data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

st.set_page_config(layout="wide")

st.sidebar.title('Filtres')
selected_year_slider_key = "selected_year_slider"
selected_year = st.sidebar.slider('Sélectionner une année', min_value=data['Year'].min(), max_value=data['Year'].max(),
                                  value=data['Year'].min(), key=selected_year_slider_key)

tabs = st.tabs(["Nuage de Points", "Évolution des Rangs", "Carte Top 10", "Carte H-index", "Conclusion"])

with tabs[0]:
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Nuage de Points: Documents vs Citations pour " + str(
            selected_year) + "</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1], gap="large")
    with col1:
        scatter_plot_for_year(data, selected_year)
    with col2:
        st.subheader('Le leader :')
        st.write("On peut constater à travers ce graphique que les Etats Unis sont de 1996 à 2014 le pays qui arrive a produire le plus de documents qui sont par la suite utilisé pour la recheche.")
        st.write("")
        st.subheader('L\'ascension de la Chine :')
        st.write("On remarque également que la Chine, à partir de 2005 augmente considérablement sa production")

with tabs[1]:
    st.markdown("<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Évolution des Rangs des Pays</h2>",
                unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1], gap="large")
    with col1:
        top_10_ranks = data[data['Rank'] <= 10]
        plot_top_10_ranks_evolution(top_10_ranks)
    with col2:
        st.write("Ajoutez ici des commentaires sur les graphiques affichés dans la première colonne.")

with tabs[2]:
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Carte des pays du top 10 pour l\'année " + str(
            selected_year) + " selon le nombre de documents produits</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1], gap="large")
    with col1:
        plot_top_countries_map(data, world, 10, selected_year)
    with col2:
        st.write("Ajoutez ici des commentaires sur les graphiques affichés dans la première colonne.")

with tabs[3]:
    h_index_slider_key = "h_index_threshold_slider"
    h_index_threshold = st.sidebar.slider('Sélectionner un seuil pour l\'indice H', min_value=0,
                                          max_value=data['H.index'].max(), value=0, key=h_index_slider_key)
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Carte des pays avec un H-index supérieur à " + str(
            h_index_threshold) + " pour l'année " + str(selected_year) + "</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1], gap="large")
    with col1:
        plot_map(selected_year, h_index_threshold, data, world)
    with col2:
        st.write("Ajoutez ici des commentaires sur les graphiques affichés dans la première colonne.")

with tabs[4]:
    st.markdown(
        "<h2 style='font-weight:bold;margin-bottom:20px;font-size:35px'>Stratégies de Revitalisation des 5 Pires Pays</h2>",
        unsafe_allow_html=True)

    strategies = [
        "Investissement dans la recherche et développement (R&D) : Encourager les gouvernements à investir davantage dans la recherche scientifique et technologique. Cela pourrait inclure l'allocation de fonds spécifiques, la création de subventions pour les chercheurs et les institutions de recherche, et le financement de projets de recherche innovants.",
        "Amélioration de l'infrastructure de recherche : Développer et moderniser les infrastructures de recherche, telles que les laboratoires, les centres de recherche et les universités. Cela pourrait impliquer la construction de nouvelles installations de recherche, l'acquisition d'équipements de pointe et la mise en place de collaborations internationales.",
        "Éducation et formation : Renforcer les programmes d'éducation scientifique et technologique à tous les niveaux, de l'enseignement primaire à l'enseignement supérieur. Encourager la formation continue des chercheurs et des professionnels de la science pour maintenir leurs compétences à jour et favoriser l'innovation.",
        "Promotion de la collaboration internationale : Encourager la collaboration et les échanges scientifiques internationaux en facilitant les partenariats entre les chercheurs, les institutions de recherche et les organisations internationales. Cela pourrait favoriser le partage des connaissances, des ressources et des meilleures pratiques.",
        "Création d'incitations : Mettre en place des incitations pour encourager la recherche et l'innovation, telles que des prix, des subventions de recherche, des crédits d'impôt pour la recherche et le développement, et des politiques de propriété intellectuelle favorables à l'innovation.",
        "Promotion de l'entrepreneuriat scientifique : Encourager la création d'entreprises innovantes dans le domaine des sciences et de la technologie en fournissant un soutien financier, une assistance technique et des infrastructures adaptées.",
        "Transfert de technologie : Faciliter le transfert de technologie et de connaissances scientifiques des institutions de recherche vers le secteur industriel afin de stimuler l'innovation et la croissance économique."
    ]

    col1, col2 = st.columns(2)
    with col1:
        for strategy in strategies[:4]:
            strategy_title, strategy_content = strategy.split(":", 1)
            st.markdown("<p style='font-size:20px; font-weight:bold;'>" + strategy_title.strip() + "</p>",
                        unsafe_allow_html=True)
            st.write(strategy_content.strip())
    with col2:
        for strategy in strategies[4:]:
            strategy_title, strategy_content = strategy.split(":", 1)
            st.markdown("<p style='font-size:20px; font-weight:bold;'>" + strategy_title.strip() + "</p>",
                        unsafe_allow_html=True)
            st.write(strategy_content.strip())