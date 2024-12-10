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

#------------------------------------------------------------
#ÚLTIMOS PASOS - GRÁFICOS

# Dividimos en dos columnas para mejorar la presentación
col1, col2 = st.columns([2, 1])

# Columna 1: Gráfico de Estrenos por Año
with col1:
    # Centramos el subtítulo del gráfico
    st.markdown("<h2 style='text-align: center; color: blue;'>Gráfico: Estrenos por Año</h2>", unsafe_allow_html=True)
    
    # Creamos del diccionario de Estrenos por año
    Estrenos_por_año = {
        '2000': 5, '2001': 9, '2002': 10, '2003': 19, '2004': 19, '2005': 19, '2006': 17, '2007': 28,
        '2008': 26, '2009': 28, '2010': 38, '2011': 40, '2012': 32, '2013': 47, '2014': 41, '2015': 67,
        '2016': 53, '2017': 59, '2018': 61, '2019': 56, '2020': 41, '2021': 70, '2022': 75, '2023': 81
    }

    # Extraemos los años y los valores de estrenos
    años = list(Estrenos_por_año.keys())
    estrenos = list(Estrenos_por_año.values())

    # Creamos la figura y el gráfico con un tamaño mayor
    plt.figure(figsize=(12, 8))
    
    # Creamos el gráfico de barras (histograma) usando los estrenos
    plt.bar(años, estrenos, color='gold', edgecolor='black')

    # Añadimos título y etiquetas de manera más estilizada
    plt.title('Estrenos por Año', fontsize=16, color='navy')
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Número de Estrenos', fontsize=12)
    
    # Ajustar el diseño para que todo se vea bien
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

# Columna 2: Tabla de Películas más Rankeadas
with col2:
    #Centramos el subtítulo de la tabla
    st.markdown("<h2 style='text-align: center; color: green;'>Tabla: Películas más Rankeadas</h2>", unsafe_allow_html=True)

    #Creamos las listas de 'películas' y 'espectadores'
    peliculas = ['¡Asu mare! 2','¡Asu mare!','¡Asu mare! 3', 'A los 40', 'Locos de amor', 'Soltera, casada, viuda, divorciada', 'La Foquita: El 10 de la calle', 'Calichín', 'Locos de amor 2', 'No me digas solterona', 'Once machos', 'Guerrero', 'Cebiche de tiburón', 'Av. Larco, la película', 'Cementerio General', 'Lusers', 'La peor de mis bodas', '¡Asu mare! Los amigos', 'El gran León', 'Condorito', 'Sí, mi amor', 'La paisana Jacinta: En búsqueda de Wasaberto', 'Once machos 2', 'Locos de amor 3', 'Siete semillas', 'Utopía, la película', 'Margarita', 'Recontra loca', 'Secreto Matusita', 'Soltera codiciada', 'Viejos amigos', 'Django: Sangre de mi sangre', 'El delfín: la historia de un soñador', 'Sobredosis de amor', 'Caiga quien caiga', 'Cementerio General 2', 'Gemelos sin cura', 'Somos Néctar', 'Mañana te cuento', 'Piratas en el Callao', 'No me digas solterona 2', 'Dragones: Destino de fuego', 'Margarita 2', 'Hasta que la suegra nos separe', 'La teta asustada', 'Ciudad de M', 'Paloma de papel', 'Django: La otra cara', 'No estamos solos', 'Como en el cine', 'A tu lado', 'La hora final', 'La peor de mis bodas 2', 'Los ilusionautas', 'El vientre', 'La cara del diablo', 'Papá Youtuber', '¿Nos casamos? Sí, mi amor', 'F-27', 'Django: En el nombre del hijo', 'Mañana te cuento 2', 'La Gran Sangre: La película', 'Macho peruano que se respeta', 'Baño de damas', 'Al filo de la ley', 'Intercambiadas', 'La entidad','Rodencia y el diente de la princesa', 'Chicha tu madre', 'Un día sin sexo', 'Motor y motivo', 'Perro guardián', 'Amigos en apuros', 'Tarata', 'Manual del pisado', 'La herencia', 'Polvo enamorado', 'Atacada: La teoría del dolor', 'Valentino y El Clan del Can','Japy Ending', 'Mariposa negra', 'Loco cielo de Abril', 'Vidas paralelas', 'El candidato', 'Una aventura gigante', 'Cosas de amigos', 'Papá x tres', '¿Mi novia es él?', 'Tinta roja']
    espectadores = [3082942, 3037677, 2042567, 1686367, 1221932, 1014812, 971636, 928858, 882937, 868482, 804852, 796311, 784282, 774864, 747000, 740650, 722106, 716331, 690502, 679606, 663804, 653095, 653014, 649466, 611256, 565045, 550279, 525132, 509120, 503080, 460953, 433047, 373628, 364111, 363477, 339714, 311892, 308523, 288242, 285509, 279812, 270724, 258585, 252321, 250601, 249511, 248296, 228510, 228464, 227370, 226360, 224732, 217186, 214905, 214078, 211119, 206885, 201908, 194594, 193193, 188931, 185138, 177686, 169244, 168720, 168008, 163950, 160497, 157498, 156020, 144979, 140788, 137768, 137629, 134478, 127714, 122657, 116996, 115791, 113764, 112704, 112594, 110941, 108783, 106386, 105782, 105610, 105313, 105170]

    # Creamos un DataFrame con pandas
    df = pd.DataFrame({
        'Película': peliculas,
        'Cantidad_espectadores': espectadores
    })

    # Mostramos la tabla interactiva con un tamaño reducido
    st.dataframe(df, use_container_width=True, width=300, height=450)
