import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import folium_static
import folium

#PASO 00
#Cargamos la base de datos de películas
#Lo cargamos como un DataFrame para acceder a él
df = pd.read_csv("Peliculas.csv")

#PASO 01 - Encabezado, mostramos el título al centro, mejora la estética visual
st.markdown("<h1 style='text-align: center; color: #FF5733;'>Detalle de Películas</h1>", unsafe_allow_html=True)

#PASO 02 - Sidebar para seleccionar cada una de las películas
pelicula_seleccionada = st.sidebar.selectbox(
    "Selecciona una película:",
    df['Título'].unique()
)
# Filtrar datos de la película seleccionada
datos_pelicula = df[df['Título'] == pelicula_seleccionada].iloc[0]

# PASO 03 - Diseño del contenido principal
# Agregamos columnas para separar la información y permitir que la interfaz se vea ordenada
col1, col2 = st.columns([1, 2])

# Columna izquierda: Imagen y enlaces
with col1:
    #Agregamos la portada y los enlaces que redireccionen a las páginas de fichas técnicas y tráiler's
    st.image(datos_pelicula['Portada Imagen'], use_container_width=True)
    
    st.markdown(f"""
    <div style="text-align: center;">
        <a href="{datos_pelicula['URL - IMDb / FilmAffinity']}" target="_blank">
            <button style="background-color: #EFEFEF; color: black; padding: 10px 20px; border-radius: 5px; border: none; font-size: 16px; cursor: pointer;">
                🌐 Ver en IMDb/FilmAffinity
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center;">
        <a href="{datos_pelicula['Trailer']}" target="_blank">
            <button style="background-color: #EFEFEF; color: black; padding: 10px 20px; border-radius: 5px; border: none; font-size: 16px; cursor: pointer;">
                📀 Ver Tráiler
            </button>
        </a>
    </div>
 """, unsafe_allow_html=True)

# Columna derecha: Información detallada
with col2:
    # Crear un contenedor interactivo para toda la información
    with st.expander("🖹 Datos Generales", expanded=True):
        # Información de la película con estilo
        st.markdown(f"<p style='font-size: 16px; color: #008080;'>Año: <span style='color: #333'>{datos_pelicula['Año']}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; color: #8A2BE2;'>Género: <span style='color: #333'>{datos_pelicula['Género']}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; color: #FF6347;'>Duración: <span style='color: #333'>{datos_pelicula['Tiempo (min)']} minutos</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; color: #FFD700;'>Director: <span style='color: #333'>{datos_pelicula['Directores']}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; color: #20B2AA;'>Actores Protagónicos: <span style='color: #333'>{datos_pelicula['Actores Protagónicos']}</span></p>", unsafe_allow_html=True)

    # Resumen con una caja de texto destacada, dado en un contenedor colapsable
    with st.expander("🖹 Resumen", expanded=False):
        st.markdown(f"<p style='font-size: 16px; color: #333: <br><span style='color: #696969'>{datos_pelicula['Resumen']}</span></p>", unsafe_allow_html=True)


   # Aquí usamos un slider interactivo para las valoraciones de las películas
    movie_key = f"rating_{datos_pelicula['Título']}"

    # Inicializamos el valor en session_state solo si aún no existe
    if movie_key not in st.session_state:
        st.session_state[movie_key] = 5  # Valor predeterminado (5 estrellas)

    # Mostrar un slider interactivo para la valoración
    valoracion = st.slider(
        'Valoración (de 1 a 5 estrellas)', 
        min_value=1, 
        max_value=5, 
        value=st.session_state[movie_key],  # Usamos el valor guardado en session_state
        key=movie_key  # Clave única para la película
    )

    # Actualizamos el valor en session_state solo si el slider fue movido
    if valoracion != st.session_state[movie_key]:
        st.session_state[movie_key] = valoracion

    # Mostrar la calificación seleccionada en formato de estrellas
    st.markdown(f"Tu valoración: {'⭐' * valoracion}", unsafe_allow_html=True)

    #Con la valoración, buscamos que el usuario interactúe con la plataforma, explicando los pasos: st.slider da un control ajustable a números, y st.session_state mantiene el número almacenado, es decir que, aunque cambie la película, el dato sifue guardado.
