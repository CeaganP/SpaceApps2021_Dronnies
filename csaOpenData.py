# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
import numpy as np
import time
'''
Tips/Astuces
In CKAN terminology, a package/dataset is a listing like this: https://donnees-data.asc-csa.gc.ca/dataset/02969436-8c0b-4e6e-ad40-781cdb43cf24. Every item that you can download or access on a dataset page is a resource.
Get JSON-formatted lists of all datasets
https://donnees-data.asc-csa.gc.ca/api/3/action/package_list
Get a full JSON representation of a dataset or resource.
https://donnees-data.asc-csa.gc.ca/api/3/action/package_show?id=02969436-8c0b-4e6e-ad40-781cdb43cf24
Search for dataset or resources matching a query.
https://donnees-data.asc-csa.gc.ca/api/3/action/package_search?q=astronomy
Get an activity stream of recently changed datasets on the site.
https://donnees-data.asc-csa.gc.ca/api/3/action/recently_changed_packages_activity_list
'''
'''
Exemple/Example: get_data
Get all metadata for datasets where project = project_cat. Options include:
Value
'atmospheric_sci' : Science atmosphérique/Atmospheric science
'earth_observation' : Observation terrestre/Earth observation
'life_sciences' : Science de la vie/Life sciences
'space_astronomy' : Astronomie spatiale/Space astronomy
'space_environment' : Environnement spatiale/météo spatiale/ Space environment/Space weather
'space_exploration' : Exploration spatiale/Space exploration
'telemetry' : Télémétrie/Telemetry
For more information about the metadata used in this portal, see:
https://github.com/asc-csa/ckanext-asc-csa-scheming/blob/master/ckanext/scheming/ckan_dataset.json
https://github.com/asc-csa/ckanext-asc-csa-scheming/blob/python3/ckanext/scheming/presets.json.
'''
def get_data(project_cat):
    # Demander une liste des ensembles de données dans la catégorie de votre choix.
    # Request a list of datasets in the category of your choice.
    response = requests.get('https://donnees-data.asc-csa.gc.ca/api/action/package_search?fq=project:'+ project_cat)
    response.encoding = "utf-8"
    datasets= json.loads(response.text)
    # Créez un objet dataframe de pandas pour faciliter l'analyse.
    # Create a pandas dataframe object for easy analysis.
    df = pd.DataFrame(datasets['result']['results'])
    # Sauvegarder les données demandées dans un fichier .json
    # Save the data that was requested into a .json file
    with open('%s_datasets_raw.json'%project_cat, 'w') as f:
        json.dump(datasets, f)
        print("Succès ! | Success!")
        #return df
        # Appliquer la fonction/Apply the function
        #space_df = get_data('space_astronomy')
        print(df)
        # Obtenir tous les noms de colonnes/Get all of the column names
        for row in range(0, len(df)):
            print("Title: " + df.at[row, "title"])

            if df.at[row, "title"].find("CloudSat"):
                #for resource in range(0, len(df.at[row, "resources"]):
                print(df.at[row, "resources"][1]["resource_type"])
                print('https://donnees-data.asc-csa.gc.ca/dataset/' + df.at[row, "resources"][1]["id"])
                return
                response = requests.get('https://donnees-data.asc-csa.gc.ca/dataset/' + df.at[row, "resources"][0]["package_id"])
                response.encoding = "utf-8"

                return response.content

