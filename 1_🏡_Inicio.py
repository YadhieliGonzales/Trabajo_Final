#Primero, agregamos el folder al terminal de la computadora
#Segundo, instalamos un entorno virtual en tu computadora -- python -m venv .venv
#Tercero, instalamos Streamlit y las librerías a utilizar en nuestro entorno virtual.
#pip install Streamlit - pip install streamlit pandas (para la base de datos) y plotly
#Cuarto, puedes abrir el tutorial de Streamlit en tu navegador.
#streamlit hello o python -m streamlit hello
#Quinto, ejecutamos en la terminal streamlit run 1_🏡_Inicio.py o python -m streamlit run your_script.py

#----------------------------------------------------------------------------------------------------------------------------------
# Importamos las librerías necesarias
import streamlit as st #Usada para crear el interfaz en donde podremos hacer la página
import pandas as pd #Utilizada para la manipulación y análisis de datos, se usará para manejar la base de datos
import numpy as np #Librería para trabajar con arrays y matrices (por si acaso)
from PIL import Image
import streamlit as st

#Para personalizar nuestra página, cambiaremos la apariencia principal
st.set_page_config(
    page_title="Películas Peruanas", #Configuramos el título que aparecerá en la pestaña de la página (es decir, en la parte superior). En este caso, será "Películas Peruanas".
    page_icon="🎬", #Usamos un emoji que aparecerá junto al título.
    layout="wide") #Hacemos que todo el contenido de la app se extienda en la pantalla.

#Agregamos el título y lo centramos
st.markdown("<h1 style='text-align: center; color: #FF5733;'>Películas Peruanas</h1>", unsafe_allow_html=True)

#Agregamos una portada en la página principal, st. image es una función que se utiliza para mostrar imágenes. 
st.image('Portada.png')

#Como queremos que la página tenga múltiples páginas, creamos una carpeta llamada 'Páginas' en la que agregaremos cada una de las páginas que queramos que tenga nuestra app de Streamlit.
#Cambiamos el nombre de los proyectos, por ejemplo 1_🏡_Inicio.py para la página principal y así, sucesivamente

#En la página principal, agredamos un texto introductorio
texto = """
La presente página interactiva forma parte del proyecto final del curso de Pensamiento Computacional para Comunicadores de la Facultad de Ciencias y Artes de la comunicación.
Está diseñada con el fin de explorar y analizar de manera dinámica el cine peruano. 
Mediante esta plataforma, los usuarios pueden interactuar con datos visuales y mapas que detallan la ficha técnica de la industria cinematográfica peruana de entre periodo específico (2000 - 2024).
"""
# Mostramos el texto
st.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True) 
#En este caso, y como se verá durante todo el proyecto, <div style='text-align: justify; font-size: 15px;'>{texto}</div>: forma parte de una cadena de código de tipo HTML. 
# La etiqueta <div> se utiliza para agrupar contenido en HTML. En este caso, el texto está justificado (text-align: justify;). El tamaño de la fuente se establece en 15 píxeles (font-size: 15px;) y el texto estará dentro de las etiquetas <div>.

#---------------------------------------------------------------------------------------------------------------------------------------
#Recomendaciones en base a películas similares
#Para que el usuario pueda tener una mejore experiencia en la página, la haremos interactica y lo invitaremos a seleccionar sus propias películas, para que así el código pueda generar recomendaciones en base a películas similares.

#PRIMER PASO
#Mostramos y cargamos la base de datos con pandas, que ya subimos anteriormente
df=pd.read_csv("Peliculas.csv")

#SEGUNDO PASO
#Agregamos las funciones para obtener información de las películas y ver la similitud según su género
#Este código busca en el DataFrame la película con el título indicado, luego de encontrarla, arrojará el enlace de este mismo. Si no la encuentra, arrojará el enlace de una imagen por defecto.
#Decidimos mostrar la portada peusto que permitirá al usuario visualizar y, lo más importante, conocer cada película.
def poster_pelicula(nombre_pelicula):
    try:
        pelicula_fila = df[df['Título'] == nombre_pelicula]
        if not pelicula_fila.empty:
            return pelicula_fila.iloc[0]['Portada Imagen']
        else:
            return "https://via.placeholder.com/150"  # Según la guia, esta es una imagen por defecto
    except Exception as e:
        return "https://via.placeholder.com/150"
    
#TERCER PASO
#Agregamos una función ligada a la similitud basada en los géneros
#Este código convierte los géneros en conjuntos para encontrar similitud entre ellos, así retornará la cantidad de géneros similares como puntuación.
def calcular_genero_similar(pelicula_genero, genero_seleccionados):
    # Comparar similitud en géneros (intersección)
    pelicula_genero = set(str(pelicula_genero).split(', '))
    genero_seleccionados = set(str(genero_seleccionados).split(', '))
    puntuacion_similar = len(pelicula_genero & genero_seleccionados)
    return puntuacion_similar

#CUARTO PASO
#Agregamos una función para obtener recomendaciones de películas
#Este código busca la fila de cada película seleccionada y calcula la similitud con todas las demás películas para ordenarlas y luego arrojar las 5 películas más similares a estas. Cabe recalcar, que estamos excluyendo la película original, es decir, la seleccionada con anterioridad.
def recomendacion(pelicula):
    try:
        pelicula_fila = df[df['Título'] == pelicula]
        if pelicula_fila.empty:
            return [], []

        pelicula_genero = pelicula_fila.iloc[0]['Género']

        # Calcular similitud para cada película
        df['similares'] = df['Género'].apply(lambda x: calcular_genero_similar(pelicula_genero, x))

        # Ordenar por similitud y seleccionar las 5 mejores (excluyendo la original)
        recomendaciones = df[df['Título'] != pelicula].sort_values(by='similares', ascending=False).head(5)

        Peliculas_Recomendadas = recomendaciones['Título'].tolist()
        Peliculas_Recomendadas_Poster = recomendaciones['Portada Imagen'].tolist()

        return Peliculas_Recomendadas, Peliculas_Recomendadas_Poster
    except Exception as e:
        return [], []

#QUINTO PASO
#Una vez terminada el código, personalizamos la página
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        margin-top: -70px;
        padding-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title(":rainbow[Películas Similares]")

#SEXTO PASO
#Agregamos un texto que indique de qué se trata el programa de 'Recomendaciones' al usuario
texto = """
Esta interfaz, te permite interactuar con la base de datos para poder proporcionarte
recomendaciones personalizadas basadas en los géneros de las películas. 
¡Disfruta de las recomendaciones con palomitas! 🍿
"""
# Mostramos el texto
st.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True) 


#SÉPTIMO PASO
#Si ninguna película está seleccinada, mostraremos el menú principal (selectbox)
if "movie" not in st.session_state or st.session_state.movie is None:
    option = st.selectbox('Selecciona una película', df['Título'].values)
else:
    option = st.session_state.movie #Para guardar las películs seleccionadas y mantener el estado de las interacciones

#OCTAVO PASO
#Creamos las columnas para mostrar las recomendaciones
col = st.columns(1)
#Llamamos a la función recomendacion(option) para ver los títulos y portadas de las películas recomendadas.
#Usamos las st.columns para organizar en 5 columnas las recomendaciones
#En cada columna, mostramos la portada con la película (st.image) y el título (st.write)
with st.container(border=True):
        name,poster = recomendacion(option)

        col1,col2,col3,col4,col5= st.columns(5, gap='medium', vertical_alignment='top')

        with col1:
            st.image(poster[0])
            st.write(name[0])

        with col2:
            st.image(poster[1])
            st.write(name[1])
            
        with col3:
            st.image(poster[2])
            st.write(name[2])
            
        with col4:
            st.image(poster[3])
            st.write(name[3])
            
        with col5:
            st.image(poster[4])    
            st.write(name[4])
unsafe_allow_html=True
