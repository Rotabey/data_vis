import altair as alt
import matplotlib.pyplot as plt
import streamlit as st


def scatter_plot_for_year(data, year, min_documents, max_documents, min_citations, max_citations):
    # Filtrer les données pour l'année sélectionnée
    data_year_filtered = data[data['Year'] == year]

    # Calculer les moyennes pour l'année sélectionnée
    grouped_data_for_year = data_year_filtered.groupby('Country').agg(
        avg_documents=('Documents', 'mean'),
        avg_citations=('Citations', 'mean'),
        median_rank=('Rank', 'median'),
        avg_h_index=('H.index', 'mean')
    ).reset_index()

    # Filtrer les pays selon la fourchette de nombre de documents et de citations
    grouped_data_for_year_filtered = grouped_data_for_year[
        (grouped_data_for_year['avg_documents'] >= min_documents) &
        (grouped_data_for_year['avg_documents'] <= max_documents) &
        (grouped_data_for_year['avg_citations'] >= min_citations) &
        (grouped_data_for_year['avg_citations'] <= max_citations)
        ]

    # Nuage de points pour l'année sélectionnée
    scatter_plot = alt.Chart(grouped_data_for_year_filtered).mark_circle().encode(
        x=alt.X('avg_documents', title='Moyenne des documents'),
        y=alt.Y('avg_citations', title='Moyenne des citations'),
        color=alt.Color('median_rank', scale=alt.Scale(scheme='category20b'), title='Rang'),
        size=alt.Size('avg_h_index', title='H-index moyen'),
        tooltip=['Country', 'avg_documents', 'avg_citations', 'median_rank', 'avg_h_index']
    ).properties(
        width=700,
        height=400
    )

    return st.altair_chart(scatter_plot, use_container_width=True)


def plot_top_10_ranks_evolution(top_10_ranks):
    # Filtrer les données pour ne prendre en compte que les 10 premiers rangs
    top_10_ranks = top_10_ranks[top_10_ranks['Rank'] <= 10]

    # Créer un graphique avec Altair
    chart = alt.Chart(top_10_ranks).mark_line().encode(
        x='Year:O',
        y=alt.Y('Rank:O', sort='ascending'),  # Ajouter un pas de 1 à l'axe y
        color='Country:N',
        tooltip=['Country', 'Year', 'Rank']
    ).properties(
        width=600,
        height=400
    ).interactive()

    # Afficher le graphique dans Streamlit
    st.write(chart)


def plot_map(selected_year, min_h_index, max_h_index, data, world):
    # Filtrer les données en fonction de l'année et de la plage d'indices H
    data_filtered = data[
        (data['Year'] == selected_year) & (data['H.index'] >= min_h_index) & (data['H.index'] <= max_h_index)]
    world_filtered = world.merge(data_filtered, how='left', left_on='SOVEREIGNT', right_on='Country')

    # Créer la carte
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    world.plot(ax=ax, color='black', edgecolor='black')
    world_filtered.plot(ax=ax, column='H.index', cmap='viridis', edgecolor='black', legend=True)

    # Ajouter une légende à la carte
    if not ax.collections:
        vmin = min_h_index
        vmax = max_h_index
        norm = plt.Normalize(vmin=vmin, vmax=vmax)
        cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='viridis'), ax=ax)
        cbar.set_label('Indice H')

    # Afficher la carte dans Streamlit
    st.pyplot(fig)


def plot_percentage_ring(selected_year, min_h_index, max_h_index, data):
    # Filtrer les données en fonction de l'année et de la fourchette d'indices H
    data_filtered = data[
        (data['Year'] == selected_year) & (data['H.index'] >= min_h_index) & (data['H.index'] <= max_h_index)
        ]

    # Calculer le nombre de pays dans la fourchette
    num_countries_in_range = len(data_filtered)

    # Calculer le nombre total de pays
    total_countries = len(data[data['Year'] == selected_year]['Country'].unique())

    # Calculer le pourcentage de pays dans la fourchette par rapport au nombre total de pays
    percentage_in_range = (num_countries_in_range / total_countries) * 100

    # Couleurs plus foncées pour les deux sections de l'anneau
    colors = ['#2ca02c', '#d62728']

    # Tailles des sections de l'anneau
    sizes = [percentage_in_range, 100 - percentage_in_range]

    fig, ax = plt.subplots(facecolor='#0E1117')  # Couleur de fond personnalisée
    wedges, texts, autotexts = ax.pie(sizes, colors=colors, startangle=90, wedgeprops=dict(width=0.3),
                                      autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Modifier la taille et la couleur du texte pour les pourcentages
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_color('white')
        # Supprimer les étiquettes 0% et 100%
        if autotext.get_text() in ['0.0%', '100.0%']:
            autotext.set_text('')

    # Ajouter un texte au centre de l'anneau
    centre_text = ax.text(0, 0, f"{percentage_in_range:.1f}%", ha='center', va='center', fontsize=40, color='white')

    return fig


def plot_top_countries_map(data, world, top_n, selected_year):
    # Sélectionner uniquement les pays présents dans le top N pour l'année sélectionnée
    top_countries = data[(data['Rank'] <= top_n) & (data['Year'] == selected_year)]

    # Fusionner les données avec les frontières des pays
    merged_data = world.merge(top_countries, how='inner', left_on='ADMIN', right_on='Country')

    # Créer la carte
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plotter les frontières des pays
    world.plot(ax=ax, color='lightgrey')

    # Colorer les pays en fonction du nombre de documents produits
    merged_data.plot(ax=ax, column='Documents', cmap='viridis', legend=True)
    plt.axis('off')

    # Récupérer la légende de la carte
    cbar = ax.get_figure().get_axes()[1]
    cbar.set_ylabel('Nombre de documents produits', fontsize=12)

    # Afficher la carte dans Streamlit
    st.pyplot(fig)
