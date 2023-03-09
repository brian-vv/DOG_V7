import pandas as pd 
from calendar import month_name
from datetime import datetime
import json

#-----------------------------------------------------------------#


#####---Lecture des fichiers---#####

data_morsures = pd.read_csv('datas/DOHMH_Dog_Bite_Data.csv', sep=";")
data_licenses = pd.read_csv('datas/NYC_Dog_Licensing_Dataset.csv', sep=";")
data_park = open("datas/NYC Parks Dog Runs.geojson")


#-----------------------------------------------------------------#


#####---Cleaning du fichier data_morsures---#####

# Renommer la colonne "AnimalBirthMonth" en "AnimalBirthYear" avec la méthode "rename"
data_morsures = data_morsures.rename(columns={'AnimalBirthMonth': 'AnimalBirthYear'})

# Supprimer les lignes qui ne respectent pas deux conditions : La colonne "AnimalBirthYear" doit contenir une valeur composée de 4 chiffres OU la valeur de "AnimalBirthYear" doit être supérieure ou égale à 1994 (âge max d'un chien 29 ans)
data_morsures.drop(data_morsures[~data_morsures['AnimalBirthYear'].astype(str).str.match('\d{4}$') | (data_morsures['AnimalBirthYear'].astype(int) < 1994)].index, inplace=True)

# Supprimer les lignes qui contiennent des valeurs nulles avec la méthode "dropna"
data_morsures = data_morsures.dropna()

# Diviser la colonne "DateOfBite" en trois nouvelles colonnes ("MonthsOfBite", "DaysOfBite" et "YearsOfBite") en utilisant la méthode "split" 
data_morsures[['MonthsOfBite', 'DaysOfBite', 'YearsOfBite']] = data_morsures.DateOfBite.str.split(" ", expand = True)


#####---Cleaning du fichier data_licenses---#####

# Même chose pour les commentaires
data_licenses = data_licenses.rename(columns={'AnimalBirthMonth': 'AnimalBirthYear'})

data_licenses.drop(data_licenses[~data_licenses['AnimalBirthYear'].astype(str).str.match('\d{4}$') | (data_licenses['AnimalBirthYear'].astype(int) < 1994)].index, inplace=True)

data_licenses = data_licenses.dropna()

data_licenses[['DaysLicenseIssue', 'MonthsLicenseIssue', 'YearsLicenseIssue']] = data_licenses.LicenseIssuedDate.str.split("/", expand = True)


#####---Merge des 2 fichiers---#####

# Jointure des 2 fichiers 
join_data = pd.merge(data_morsures, data_licenses, on='Unique Dog ID')

# Division de la colonne "DateOfBite" en trois nouvelles colonnes ("MonthsOfBite", "DaysOfBite" et "YearsOfBite") du nouveau fichier mergé
join_data[['MonthsOfBite', 'DaysOfBite', 'YearsOfBite']] = join_data.DateOfBite.str.split(" ", expand = True)


#-----------------------------------------------------------------#


#####---[Unique] - Total des races enregistrées---#####

# Compter le nombre de licence unique 2017 
total_breed = data_licenses[data_licenses['YearsLicenseIssue'].isin(['2017'])]["BreedName"].nunique()


#-----------------------------------------------------------------#


#####---[Quanti/Quanti] - Nombre de licences délivrées par trimestres---#####

# Définition des intervalles de temps (bins) et des étiquettes correspondantes (labels)
bins = [0, 3, 6, 9, 12]
labels = ['3 mois', '6 mois', '9 mois', '12 mois']

# Sélection des données pour l'année 2017 et regroupement par mois avec calcul du nombre de licences
count_licenses = data_licenses[data_licenses['YearsLicenseIssue'].isin(['2017'])].groupby('MonthsLicenseIssue').size().reset_index(name='counts')

# Conversion de la colonne "MonthsLicenseIssue" en entiers et ajustement des valeurs pour qu'elles soient sur une échelle de 0 à 11 (12 valeurs en tout) 
count_licenses['MonthsLicenseIssue'] = count_licenses['MonthsLicenseIssue'].astype(int) - 1

# Regroupement des données par trimestre en utilisant la méthode "cut" pour découper les mois selon les intervalles de temps définis précédemment
count_licenses['Quarter'] = pd.cut(count_licenses['MonthsLicenseIssue'], bins=bins, right=False)

# Regroupement des données par trimestre et calcul de la somme du nombre de licences pour chaque trimestre
count_licenses = count_licenses.groupby('Quarter').sum()

# Association des étiquettes correspondantes à la colonne Quarter
count_licenses['Quarter'] = labels

# Ajout de la colonne "Cumulative_Count" avec le cumul du nombre de licences
count_licenses['Cumulative_Count'] = count_licenses['counts'].cumsum()


#-----------------------------------------------------------------#


#####---Top 10 des races de chiens enregistrées---#####

# Compter les breedname en 2017 dans une colonne count, puis le grouper par breedname
count_breed = data_licenses[data_licenses['YearsLicenseIssue'].isin(['2017'])].groupby(['BreedName']).size().reset_index(name='count')

# Afficher les 10 plus grandes valeurs de la colonne count
count_breed = count_breed.nlargest(10, 'count')



#-----------------------------------------------------------------#


#####---[Unique] - Total morsure---#####

# Compter les morsures en 2017 et les mettres dans une colonne count
TotalBite = data_morsures[data_morsures['YearsOfBite'].isin(['2017'])].groupby('YearsOfBite').size().reset_index(name='count')

# Sommmer la colonne count
TotalBite = TotalBite['count'].sum()


#-----------------------------------------------------------------#


#####---[Quanti/Quanli] - Total des morsures par mois---#####

# Regrouper les morsures par mois et par années 
bite_per_month = data_morsures[data_morsures['YearsOfBite'].isin(['2017'])].groupby(['YearsOfBite','MonthsOfBite']).size().reset_index(name='count')

# Convertir les mois en type "datetime" en utilisant le format "MM" pour les mois
bite_per_month['MonthsOfBite']= pd.to_datetime(bite_per_month['MonthsOfBite'],format='%B')

# Ajouter une colonne pour les mois sous forme de nombre
bite_per_month["month_num"] = bite_per_month["MonthsOfBite"].dt.month

# Création d'une bibliothèque des mois 
month_name = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

# Transformer les numéros de mois en lettres, et ajustement des valeures uniquement si elles osnt comprise dans l'intervalle 0-12 correspondant aux mois
bite_per_month['MonthsOfBite']= bite_per_month['month_num'].apply(lambda x: month_name[x-1] if x>0 and x<=12 else "NA")

# Trier les données en utilisant la colonne 'month_num' pour les trier dans l'ordre d'un calendrier
bite_per_month = bite_per_month.sort_values(by=['YearsOfBite','month_num'],ascending=[True,True])


#-----------------------------------------------------------------#


#####---[Quanti/Quanti] - Répartition des morsures par âge---#####

# Création d'une colonne avec l'année actuelle 
data_morsures['Current_Year'] = datetime.now().year

# Création d'une colonne Age à l'aide d'une soustraction de l'année actuelle et l'année de naissance du chien
data_morsures['Age'] = data_morsures['Current_Year'] - data_morsures['AnimalBirthYear']

# Prendre les mosure de 2017 et les grouper par âge dans une colonne count 
bite_per_age = data_morsures[data_morsures['YearsOfBite'].isin(['2017'])].groupby("Age").size().reset_index(name='count')


#-----------------------------------------------------------------#


#####---[Quali/Quali] - Top 10 des races de chiens les plus castré---#####

# Prendre les valeurs de 2017 
joined_data = join_data[join_data['YearsOfBite'].isin(['2017'])]

# Grouper par breedname et compter le nombre de castré dans une colonne count et en sortir les 10 plus grandes valeurs 
spray_neuter_per_breed = joined_data.groupby('BreedName')['SpayNeuter'].sum().reset_index(name='count').nlargest(10, 'count')


#-----------------------------------------------------------------#


#####---[Quali/Quali] - Répartition Male/Femelle selon la race---#####

# Création d'une liste de toutes les races de chien 
dict_breedname = joined_data['BreedName'].unique()

# Grouper les valeurs par race et sexe et compter le nombre de chien y correspondant, dans une colonne count
sexe_repartition_by_breedname = joined_data.groupby(['BreedName', 'AnimalGender'])['Unique Dog ID'].count().reset_index(name='count')


#-----------------------------------------------------------------#


#####---[Quanti/Quanli][Unique] - Morsures qui ont eu lieu dans des parc à chien---#####

# Charger les données du fichier geojson dans une variable 
with data_park as park:
    data = json.load(park)

# Création d'un dictionnaire pour stocker les zipcode et coordonnées gps 
zipcodes = {}

# Prendre les morsure de 2017 et compter les zipcode correspondant, donc le nombre de morsures par parc
bite_per_park = data_morsures[data_morsures['YearsOfBite'].isin(['2017'])].groupby(['ZipCode']).size().reset_index(name='count')

# Boucle for qui va chercher dans les features du fichiers json les zipcode et coordonnées gps 
for feature in data['features']:
    zipcode = feature['properties']['zipcode']
    lon, lat = feature['geometry']['coordinates'][0][0][0]
    
# Association des zipcode aux coordonnées correspondantes 
    zipcodes[zipcode] = [lon, lat]
    
# Création d'un dataframe issue du dictionnaire créer plutot et création des colonnes longitude et latitudes 
zipcodes_df = pd.DataFrame.from_dict(zipcodes, orient='index', columns=['Longitude', 'Latitude'])

# Renommer la colonne index en zipcode 
zipcodes_df = zipcodes_df.reset_index().rename(columns={'index': 'ZipCode'})

# Conversion des valeurs de la variable bite_per_park en valeur numérique + si une valeur ne peut pas être convertie en nombre, elle sera remplacée par NaN
bite_per_park['ZipCode'] = pd.to_numeric(bite_per_park['ZipCode'], errors='coerce')

# Même chose 
zipcodes_df['ZipCode'] = pd.to_numeric(zipcodes_df['ZipCode'], errors='coerce')

# Enlever les valeurs vides 
bite_per_park = bite_per_park.dropna()

# Même chose 
zipcodes_df = zipcodes_df.dropna()

# Transformer ces valueurs en integer 
bite_per_park['ZipCode'] = bite_per_park['ZipCode'].astype(int)

# Même chose 
zipcodes_df['ZipCode'] = zipcodes_df['ZipCode'].astype(int)

# Merger les 2 dataframe 
zipcode_merged = pd.merge(bite_per_park, zipcodes_df, on='ZipCode')

# Trier les données en ordre croissant 
zipcode_merged = zipcode_merged.sort_values(by=['ZipCode'],ascending=[True])

# Sommer la colonne count 
zipcode_merged_sum_bite = zipcode_merged['count'].sum()



#-----------------------------------------------------------------#

# Grouper les données par race de chien et sexe
joined_data_breed = joined_data.groupby('BreedName')['Unique Dog ID'].count().reset_index(name='count').nlargest(10, 'count')

