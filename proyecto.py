import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import time

# Configuración de la conexión
user = "root"
password = "Maicha12345#"
host = 'localhost'
database = "us_airline_db"
connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
engine = create_engine(connection_string)

# Función para cargar datos con caching
@st.cache_data(ttl=60)  # Cachear los datos durante 60 segundos
def load_data():
    return pd.read_sql('SELECT * FROM `us_airline_db`', con=engine)

# Título de la aplicación
st.title('Análisis de Datos del las Aerolíneas')

# Contenedores para la tabla y gráficos
table_placeholder = st.empty()
chart_placeholder = st.empty()

# Función para dibujar gráficos
def draw_charts(df):
    chart_placeholder.empty()  # Limpiar el contenedor de gráficos
    
    # Gráfico de distribución de pasajeros por ciudad
    with chart_placeholder.container():
        st.subheader('Distribución de Pasajeros por Ciudad')
        fig1, ax1 = plt.subplots()
        ax1.hist(df['city2'].dropna(), bins=30, color='skyblue', edgecolor='black')
        ax1.set_title('Top 10 Ciudades por Tráfico de Pasajeros')
        ax1.set_xlabel('Ciudad Destino')
        ax1.set_ylabel('Total de Pasajeros')
        st.pyplot(fig1)

# Función para mostrar la tabla
def show_table(df):
    table_placeholder.empty()  # Limpiar el contenedor de la tabla
    with table_placeholder.container():
        st.subheader('Datos de la Tabla')
        st.write(f'Cantidad de registros: {len(df)}')  # Mostrar cantidad de datos
        st.write(df.head())  # Mostrar los primeros registros
        
# Botón para actualizar los datos
if st.button('Actualizar gráficos y tabla'):
    df = load_data()  # Cargar los datos actualizados
    show_table(df)  # Mostrar la tabla actualizada
    draw_charts(df)  # Dibujar gráficos actualizados

# Refresco automático
while True:
    df = load_data()
    show_table(df)  # Mostrar la tabla actualizada
    draw_charts(df)  # Dibujar gráficos actualizados
    time.sleep(10)  # Esperar 10 segundos antes de actualizar
