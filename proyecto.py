import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de la conexión
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', 'Maicha12345#')
host = 'localhost'
database = "us_airline_db"
connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
engine = create_engine(connection_string)

# Función para cargar datos con caching
@st.cache_data(ttl=60)
def load_data():
    return pd.read_sql('SELECT * FROM `us_airline_db`', con=engine)

# Título de la aplicación
st.title('Análisis de Datos de las Aerolíneas')

# Cargar los datos
df = load_data()  
st.subheader('Datos de la Tabla')
st.markdown("""
    Aqui se van a visualizar el conjunto de datos que se trabajo con sus respectivas variables y el numero de registro que tiene.
        """)
st.write(f'Cantidad de registros: {len(df)}')  
st.write(df.head())  

# Calcular el costo promedio por aeropuerto y el total de pasajeros por ciudad
avg_fare_per_airport = df.groupby('airport_1')['fare'].mean().sort_values(ascending=False)
total_passengers_per_city = df.groupby('city1')['passengers'].sum().sort_values(ascending=False)


# Función para dibujar gráficos
def draw_charts(df):
    sns.set(style="whitegrid")
    
    # Gráfico de distribución de pasajeros por ciudad
    top_cities = df['city2'].value_counts().nlargest(10)
    
    st.subheader('Distribución de Pasajeros por las 10 Ciudades Principales')
    st.markdown("""
        Este gráfico de barras muestra las 10 ciudades destino más populares, ordenadas según la cantidad total de pasajeros que llegan a cada ciudad. El gráfico ayuda a identificar los principales destinos en términos de volumen de pasajeros. Las ciudades están etiquetadas en el eje X,
        y el eje Y muestra el número total de pasajeros. Las barras están coloreadas con una paleta de colores para hacer más visuales las diferencias entre las ciudades.
        """)
    fig1, ax1 = plt.subplots()
    bars = ax1.bar(top_cities.index, top_cities.values, color=plt.cm.viridis(range(len(top_cities))))
    ax1.set_title('Top 10 Ciudades por Tráfico de Pasajeros')
    ax1.set_xlabel('Ciudad Destino')
    ax1.set_ylabel('Total de Pasajeros')
    ax1.set_xticklabels(top_cities.index, rotation=45, ha='right', fontsize=10)


    for bar in bars:
        ax1.text(
            bar.get_x() + bar.get_width() / 2, 
            bar.get_height(), 
            f'{int(bar.get_height())}', 
            ha='center', 
            va='bottom', 
            fontsize=9
        )
        
    plt.tight_layout()  
    st.pyplot(fig1)

    # Gráfico de distribución de distancia (millas)
    st.subheader('Distribución de la Distancia (Millas)')
    st.markdown("""
        En este histograma, se representa la frecuencia con la que ocurren ciertas distancias en millas entre aeropuertos. El eje X muestra las distancias (en millas) y 
        el eje Y la frecuencia de vuelos que cubren esas distancias. Además de las barras que indican cuántos vuelos recorren cada distancia, se incluye una línea de densidad (KDE) para visualizar de manera suave cómo se distribuyen los datos, mostrando las distancias más comunes.    
        """)
    fig2, ax2 = plt.subplots()
    sns.histplot(df['nsmiles'], kde=True, ax=ax2, color="skyblue")
    ax2.set_title('Distribución de la Distancia (Millas)')
    ax2.set_xlabel('Millas')
    ax2.set_ylabel('Frecuencia')
    plt.tight_layout()
    st.pyplot(fig2)


    # Gráfico de distribución de tarifa (fare)
    st.subheader('Distribución de la Tarifa')
    st.markdown("""
        Este gráfico es un histograma que muestra cómo se distribuyen las tarifas de vuelo en dólares. El eje X representa las diferentes tarifas y el eje Y la frecuencia con que esas tarifas ocurren en los vuelos. La línea de densidad suaviza la curva de las barras, lo que permite identificar las tarifas más frecuentes, 
        y te da una idea de cómo varían los precios de los vuelos en el conjunto de datos.
        """)
    fig3, ax3 = plt.subplots()
    sns.histplot(df['fare'], kde=True, ax=ax3, color="lightgreen")
    ax3.set_title('Distribución de la Tarifa')
    ax3.set_xlabel('Tarifa ($)')
    ax3.set_ylabel('Frecuencia')
    plt.tight_layout()
    st.pyplot(fig3)
 

    # Gráfico de distribución del número de pasajeros
    st.subheader('Distribución del Número de Pasajeros')
    st.markdown("""
    Este gráfico también es un histograma que ilustra la distribución del número de pasajeros por vuelo. En el eje X se encuentran las cantidades de pasajeros por vuelo y el eje Y muestra la frecuencia de los vuelos que tienen ese número de pasajeros. La línea de densidad (KDE) permite observar los valores más comunes de pasajeros por vuelo, 
    facilitando la identificación de si hay una tendencia en el número de pasajeros por vuelo.
        """)
    fig4, ax4 = plt.subplots()
    sns.histplot(df['passengers'], kde=True, ax=ax4, color="salmon")
    ax4.set_title('Distribución del Número de Pasajeros')
    ax4.set_xlabel('Pasajeros')
    ax4.set_ylabel('Frecuencia')
    plt.tight_layout()
    st.pyplot(fig4)



    # Gráfico: Evolución de tarifas por año
    st.subheader('Evolución de las tarifas por año')
    st.markdown("""
        En este gráfico de líneas se visualiza cómo han cambiado las tarifas a lo largo del tiempo, permitiendo ver tendencias en los precios de los boletos año tras año. El eje X representa los años, y el eje Y las tarifas promedio de los vuelos. 
        Este gráfico te permite analizar si las tarifas han subido, bajado o se han mantenido constantes con el tiempo.
        """)
    fig5, ax5 = plt.subplots()
    sns.lineplot(df, x='Year', y='fare', ax=ax5)
    ax5.set_title('Fare Evolution by Year and Airline')
    ax5.set_xlabel('Year')
    ax5.set_ylabel('Fare')
    st.pyplot(fig5)



    st.title("Análisis de Aeropuertos y Ciudades por Tarifas y Pasajeros")
    # Gráfico de las tarifas promedio por aeropuerto
    st.subheader("Aeropuertos con Tarifas Promedio más Altas")
    st.markdown("""
        Aquí se muestra un gráfico de barras donde se comparan los aeropuertos según las tarifas promedio de los vuelos que parten desde ellos. En el eje X están los nombres de los aeropuertos, y en el eje Y las tarifas promedio en dólares. Este gráfico te ayuda a identificar cuáles son los aeropuertos con los costos de viaje más altos, 
        lo que puede ser útil para analizar factores como demanda, ubicación o costos operativos
        """)
    fig6, ax = plt.subplots()
    avg_fare_per_airport.head(10).plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel('Tarifa Promedio (USD)')
    ax.set_xlabel('Aeropuertos')
    ax.set_title('Top 10 Aeropuertos por Tarifa Promedio')
    st.pyplot(fig6)

    # Gráfico de las ciudades con más pasajeros
    st.subheader("Ciudades con Mayor Número de Pasajeros")
    st.markdown("""
        Similar al gráfico anterior, este gráfico de barras muestra las ciudades que tienen el mayor volumen de pasajeros saliendo o llegando. El eje X representa las ciudades, 
        """)
    fig7, ax = plt.subplots()
    total_passengers_per_city.head(10).plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_ylabel('Número Total de Pasajeros')
    ax.set_xlabel('')
    ax.set_title('Top 10 Ciudades por Número de Pasajeros')
    st.pyplot(fig7)
    


# Dibujar gráficos
draw_charts(df)

# Opción para actualizar manualmente
if st.button("Actualizar Datos"):
    df = load_data()
    st.rerun()  # Cambiado a st.rerun()
