# Analyse des Publications Scientifiques par Pays

Ce projet Streamlit est conçu pour analyser et visualiser les données sur les publications scientifiques par pays. Il fournit des graphiques interactifs et des cartes pour explorer divers aspects de la production scientifique mondiale, notamment les documents publiés, les citations, les classements des pays, les indices H et bien plus encore.

## Fichiers

- **main.py:** Contient le code principal de l'application Streamlit.
- **utils.py:** Contient les fonctions utilitaires utilisées pour créer les graphiques et les cartes.
- **publications_scientifiques_par_pays.csv:** Données sur les publications scientifiques par pays.
- **ne_110m_admin_0_countries.shp:** Frontières géographiques des pays du monde.

## Exigences

- Python 3.x
- Streamlit
- Pandas
- Geopandas
- Altair
- Matplotlib

## Installation et Exécution

1. **Installer les dépendances :**
    ```bash
    pip install streamlit pandas geopandas altair matplotlib
    ```

2. **Exécuter l'application Streamlit :**
    ```bash
    streamlit run main.py
    ```