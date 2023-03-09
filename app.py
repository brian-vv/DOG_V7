from treatments import *
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objs as go

#-----------------------------------------------------------------#


#####---Nom de la page---#####

st.set_page_config(page_title="Dashboard Dog", layout='wide')
st.title("Dashboard - Etude sur les chiens à NY en 2017")


#-----------------------------------------------------------------#


#####---[Unique] - Total des races enregistrées---#####

# Affichage sur Streamlit
st.write("[Unique] - " + str(total_breed) + " de races de chiens enregistrées")


#-----------------------------------------------------------------#

    
left_column, right_column = st.columns(2)

with left_column: 
    
#####---[Quanti/Quanti] - Nombre de licences délivrées par trimestres---#####

    # Initialisation des données à mettre de le graph
    data = [go.Scatter(x=count_licenses['Quarter'], y=count_licenses['Cumulative_Count'])]

    # Ajout du titre + nom des axes 
    layout = go.Layout(title={"text": "[Quanti/Quanti] - Nombre de licences délivrées par trimestres"}, xaxis_title='Quarter', yaxis_title='Nbr de licences')
    
    # Création du graph
    fig = go.Figure(data=data, layout=layout)
  
    # Mettre à jour l'axe des abscisses (x) pour afficher uniquement les années où se trouvent les valeurs
    fig.update_layout(xaxis=dict(ticktext=count_licenses.Quarter, tickvals=count_licenses.Quarter))

    # Afficher sur Streamlit
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False})

with right_column: 

#####---Top 10 des races de chiens enregistrées---#####

    # Créer un pie chart 
    fig = go.Figure(data=[go.Pie(labels=count_breed['BreedName'], values=count_breed['count'], hole=.7)])

    # Affichage du titre
    fig.update_layout(title={"text": "Top 10 des races de chiens enregistrées"})

    # Afficher sur Streamlit
    st.plotly_chart(fig, use_container_width=True)


#-----------------------------------------------------------------#


#####---[Unique] - Total morsure---#####

# Affichage du nombre de mosure 
st.write("[Unique] - " + str(TotalBite) + " morsures enregistrées")


#-----------------------------------------------------------------#


left_column, right_column = st.columns(2)

with left_column: 

#####---[Quanti/Quanli] - Total des morsures par mois---#####

    # Initialisation des données à mettre dans le graph
    data = [go.Scatter(x=bite_per_month['MonthsOfBite'], y=bite_per_month['count'],mode = 'lines+markers')]

    # Ajout des titres des axes
    layout = go.Layout(title=f'[Quanti/Quanli] - Total des morsures par mois', xaxis=dict(title='Mois'), yaxis=dict(title='Nombre de morsures'))

    # Créer le graphique en utilisant les data et le layout
    fig = go.Figure(data=data, layout=layout)

    # Mettre à jour l'axe des abscisses (x) pour afficher uniquement les mois où se trouvent les valeurs
    fig.update_layout(xaxis=dict(ticktext=bite_per_month.MonthsOfBite, tickvals=bite_per_month.MonthsOfBite))

    # Configuation pour retirer les actions liées au graphiques
    st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False, 'scrollZoom': False})


with right_column:
    
#####---[Quanti/Quanti] - Répartition des morsures par âge---#####

    # Initialisation des données à mettre dans le graph
    data = go.Scatter(
        x=bite_per_age['Age'],  
        y=bite_per_age['count'], 
        mode='markers',  
        marker=dict(
            # Taille des bulles, définie en fonction du nombre de morsures par âge /8 pour afficher en plus petit 
            size=bite_per_age['count']/8,  
            # Couleur des bulles, définie en fonction de l'âge
            color=bite_per_age['Age'],  
            colorscale='Turbo',  
            reversescale=True,
             # Afficher la légende de l'échelle de couleurs
            showscale=True 
        ),
        # Étiquettes pour chaque point (dans notre cas, le nombre de morsures par âge)
        text=bite_per_age['count']  
    )

    # Ajout des titres des axes
    layout = go.Layout(
        title='[Quanti/Quanti] - Répartition des morsures par âge',
        xaxis=dict(title='Âge'),
        yaxis=dict(title='Nombre de morsures')
    )

    # Créer la figure 
    fig = go.Figure(data=data, layout=layout)

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False, 'scrollZoom': False})



#-----------------------------------------------------------------#


left_column, middle_column, right_column = st.columns(3)

with left_column: 

#####---[Quali/Quali] - Répartition Male/Femelle selon la race---#####

    # Filtrer les données en fonction du sexe et ajout de la variable pour l'année dans la sidebar 
    selected_breedname = st.sidebar.selectbox("[Quali/Quali] - Répartition Male/Femelle selon la race. Choisissez une race de chien", dict_breedname)

    # Chercher le sexe sélectionné dans le fichier mergé
    sexe_repartition_by_breedname = sexe_repartition_by_breedname[sexe_repartition_by_breedname['BreedName'] == selected_breedname]

    # Créer un pie chart 
    fig = go.Figure(data=[go.Pie(labels=sexe_repartition_by_breedname['AnimalGender'], values=sexe_repartition_by_breedname['count'], hole=.7)])

    # Affichage du titre
    fig.update_layout(title={"text": "[Quali/Quali] - Répartition Male/Femelle selon la race"})

    # Afficher sur Streamlit
    st.plotly_chart(fig, use_container_width=True)
 
#-----------------------------------------------------------------#

with middle_column:    
    
#####---top 10 des races de chien qui mordent le plus selon leur sexe---#####

    # Créer le graphique
    fig = go.Figure(data=[go.Bar(x=joined_data_breed['BreedName'], y=joined_data_breed['count'], textposition='auto')])

    # Ajout d'un titre
    fig.update_layout(title={'text': "Top 10 des races de chiens qui mordent le plus"})

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False, 'scrollZoom': False})
    
#-----------------------------------------------------------------#

with right_column: 

#####---[Quali/Quali] - Top 10 des races de chiens les plus castré--#####

    # Créer le graphique
    fig = go.Figure(data=[go.Bar(x=spray_neuter_per_breed['BreedName'], y=spray_neuter_per_breed['count'], textposition='auto')])

    # Ajout d'un titre
    fig.update_layout(title={'text': "[Quali/Quali] - Top 10 des races de chiens les plus castré"})

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False, 'scrollZoom': False})


#-----------------------------------------------------------------#

left_column, right_column = st.columns((7,3))

with left_column: 
    
#####---[Quanti/Quanli][Unique] - Morsures qui ont eu lieu dans des parc à chien---#####

    # Initialisation de la map folium 
    map = folium.Map(location=[40.762057, -73.917611], zoom_start=12)

    # Boucle for qui vient mettre chaque valeurs des colonnes dans des variables 
    for index, row in zipcode_merged.iterrows():
        lon = row['Longitude']
        lat = row['Latitude']
        count = row['count']
        
    # Couleurs en fonction de la valeur dans la variable count   
        if count >= 25 and count <= 50:
            color = '#DE00FF'
            fill_color = '#DE00FF'
        elif count > 50:
            color = 'red'
            fill_color = 'red'
        else:
            color = '#3186cc'
            fill_color = '#3186cc'
            
    # Mise en place de marker en forme de cercle 
        folium.CircleMarker(
            location=[lat, lon],
            radius=count/3,
            popup=f'Park: {feature["properties"]["name"]}<br><br>Nb Morsures: {count}',
            color=color,
            fill=True,
            fill_color=fill_color
        ).add_to(map)


    st.write("[Quanti/Quanli][Unique] - " + str(zipcode_merged_sum_bite) + " morsures enregistrées dans des parc à chien")

    # Affichage de la map sur Streamlit [Quanti/Quanli]
    st_folium(map, width=700, height=450)

    st.write("Bleu : < 25 morsures | Violet : 25 < < 50 morsures | Rouge : > 50 morsures")

with right_column: 
    
    st.write(" ")
    
    
    
    
    

    
