#Importamos las librerías a utilizar
import pandas as pd #Ya mencionado anteriormente, permite manipular y manejar los datos de un DataFrame.
import streamlit as st
import numpy as np #ofrece herramientas que manejan datos númericos
import function as fl 

#PASO 01
#Cargamos la base de datos de películas
#Lo cargamos como un DataFrame para acceder a él, el formato CSV almacena grandes cantidades de datos y Pandas permite acceder a él.
df = pd.read_csv("Peliculas.csv")

#PASO 02 - Función para filtrar películas
#Esta función toma los aspectos como años, géneros, idioma y ubicación para filtrar las películas
#Mediante las condicionales se busca tener una filtración que nos arroje información 'separada'
def lista_películas(año_inicio, año_fin, Género, Idioma, Locación):
    # Filtrar por año para obtener las películas que solo estén dentro del rango establecido. Esto mediante las condicionales
    if año_inicio and año_fin:
        filtered_df = df[(df['Año'] >= año_inicio) & (df['Año'] <= año_fin)] #si no se especifica rango, se mantiene junto
    else:
        filtered_df = df

    # Filtrar por género para obtener solo las películas que perteneces y son escogidas
    if Género:
        filtered_df = filtered_df[filtered_df['Género'].isin(Género)]

    # Filtrar por idioma (similar a las anteriores)
    if Idioma:
        filtered_df = filtered_df[filtered_df['Idioma'].isin(Idioma)]

    # Filtrar por locaciones (similar a las anteriores)
    if Locación:
        filtered_df = filtered_df[filtered_df['Locación'].isin(Locación)]

    # Devolver la lista de títulos de películas recomendadas
    return filtered_df['Título'].tolist()

#Agregamos el título y lo centramos
st.markdown("<h1 style='text-align: center; color: #FF5733;'>Buscador de Películas</h1>", unsafe_allow_html=True)


#PASO 03 - Filtros para la selección de películas
row1 = st.columns((1, 1, 1), gap='small', vertical_alignment='top')
#Aquí usamos el st.colums para organizar los widgtes en columnas (son 3)
#with permitirá que se hagan operaciones después de que un código ha sido ejecutado :D
with row1[0]:
    Género = st.multiselect( #el multiselect permite seleccionar uno o más de dos géneros en una película
        'Género:',
        options=df['Género'].unique(),
        default=['Comedia']
    )  
with row1[1]:
    Idioma = st.multiselect(
        'Idioma:',
        options=df['Idioma'].unique(),
        default=['Español']
    )  
with row1[2]: #Aquí creamos dos columnas más pequeñas para el botón de la selección del año
    Locación = st.multiselect(
        'Locación:',
        options=df['Locación'].unique(),
        default=['Lima']
    )  

row2 = st.columns((0.3, 0.7), gap='small', vertical_alignment='top')

with row2[0]:
    on = st.toggle(" :orange[Desactivar selección de rango]") #este permitirá activar la opción del rango de años. Si está desactivado el usuario podrá elegir un solo año, sino, seguirá en rango.
with row2[1]:
    with st.container(border=True):
        Año = df['Año'].unique()
        dia = 0
        if on:
            st.write(":green[Activado]") 
            dia = st.select_slider(
                "Seleccionar un año",
                options=Año,
                value=2016
            )
        else:
            inicio_dia, fin_dia = st.select_slider(
                "Seleccionar un rango de años",
                options=Año,
                value=(2000, 2024)
            )
            
    if on:
        st.write(f"Seleccionaste: :green[{dia}]") 
    else:
        st.write(f"Seleccionaste: :green[{inicio_dia}] - :green[{fin_dia}]")  

row3 = st.columns(1)

if dia:
    resultado_peliculas = lista_películas(dia, dia, Género, Idioma, Locación)
else:
    resultado_peliculas = lista_películas(inicio_dia, fin_dia, Género, Idioma, Locación)

# PASO 04 - Resultados de los filtros
st.title(":rainbow[🎥 Películas]")

if resultado_peliculas:
    # Dividimos en 3 columnas para mostrar las películas de manera atractiva
    pelicula_columna = st.columns(3)  
    for i, pelicula in enumerate(resultado_peliculas):
        with pelicula_columna[i % 3]:
            # Buscar la información de la película
            pelicula_info = df[df['Título'] == pelicula].iloc[0]
            
            # Creamos un contenedor para cada película, esto para que sea visualmente atractivo
            with st.expander(f"{pelicula_info['Título']}"):
                # Mostrar la portada de la película
                st.image(
                    pelicula_info['Portada Imagen'], 
                    caption=pelicula_info['Título'], 
                    use_container_width=True
                )
                
                # Mostrar el enlace al tráiler con botón personalizado
                st.markdown(f"""
                    <div style="text-align: center;">
                        <a href="{pelicula_info['Trailer']}" target="_blank">
                            <button style="
                                background-color: #EFEFEF; 
                                color: black; 
                                padding: 10px 20px; 
                                border-radius: 5px; 
                                border: none; 
                                font-size: 16px; 
                                cursor: pointer;">
                                📀 Ver Tráiler
                            </button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("No se encontraron películas que coincidan con los criterios.")