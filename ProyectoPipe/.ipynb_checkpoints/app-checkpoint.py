import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import folium
import numpy as np
import seaborn as sns

#Función para cargar los datos desde la base de datos SQLite
def load_data(year):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('happiness_data.db')  # Ajusta la ruta si es necesario
    
    # Cambiar la consulta para la región correcta
    latam_data = pd.read_sql_query(f"SELECT * FROM happiness_{year} WHERE Region = 'Latin America and Caribbean'", conn)
    top_happiness_data = pd.read_sql_query(f"SELECT * FROM happiness_{year} ORDER BY Happiness_Score DESC LIMIT 6", conn)  # Limitamos a los 5 primeros países globales
    top_happiness_data = top_happiness_data.drop(0)
    
    conn.close()
    
    # Depuración: Mostrar la cantidad de datos cargados
    st.write(f"Datos de LATAM cargados: {latam_data.shape[0]} filas")
    st.write(f"Datos de Top Global (5 primeros) cargados: {top_happiness_data.shape[0]} filas")
    
    return latam_data, top_happiness_data



# Función para calcular las diferencias de felicidad y crear el DataFrame de comparación
def calculate_comparison(latam_data, top_happiness_data):
    factor_columns = [
        'Happiness_Score', 
        'Economy_GDP_per_Capita', 
        'Family', 
        'Health_Life_Expectancy', 
        'Freedom', 
        'Trust_Government_Corruption', 
        'Generosity', 
        'Dystopia_Residual'
    ]
    
    # Calcular promedios de LATAM y top de felicidad
    latam_avg = latam_data[factor_columns].mean()
    top_avg = top_happiness_data[factor_columns].mean()

    # Crear DataFrame comparativo
    comparison_df = pd.DataFrame({
        'LATAM_Average': latam_avg,
        'Top_Happiness_Average': top_avg
    })
    comparison_df['Difference'] = comparison_df['Top_Happiness_Average'] - comparison_df['LATAM_Average']
    comparison_df['Percentage_Difference'] = (comparison_df['Difference'] / comparison_df['LATAM_Average']) * 100

    return comparison_df

# Función para graficar la comparación de las diferencias
def plot_comparison(comparison_df, year):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=comparison_df.index, y=comparison_df['Percentage_Difference'], palette='coolwarm')
    
    plt.title(f'Diferencia Porcentual de Factores de Felicidad: LATAM vs Top Global en {year}', fontsize=16)
    plt.xlabel('Factores', fontsize=12)
    plt.ylabel('Diferencia Porcentual (%)', fontsize=12)
    
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(plt)


# Función para mostrar mapas de LATAM y Top Global
def display_maps(year):

    if year == 2015:
        # Coordenadas de los países LATAM y globales
        latam_coordinates = {
            'Costa Rica': [9.7489, -83.7534],
            'Mexico': [23.6345, -102.5528],
            'Brazil': [-14.2350, -51.9253],
            'Venezuela': [6.4238, -66.5897],
            'Panama': [8.5380, -80.7821]
        }
    
        global_coordinates = {
            'Switzerland': [46.8182, 8.2275],
            'Iceland': [64.9631, -19.0208],
            'Denmark': [56.2639, 9.5018],
            'Norway': [60.4720, 8.4689],
            'Canada': [56.1304, -106.3468]
        }
    else: 
        #Paises de latam
        latam_coordinates = {
            'Costa Rica': [9.7489, -83.7534],
            'Puerto Rico': [18.2208, -66.5901],
            'Brazil': [-14.2350, -51.9253],
            'Mexico': [23.6345, -102.5528],
            'Chile': [-35.6751, -71.5429]
        }
        
        global_coordinates = {
            'Denmark': [56.2639, 9.5018],
            'Iceland': [64.9631, -19.0208],
            'Switzerland': [46.8182, 8.2275],
            'Norway': [60.4720, 8.4689]
        }



    # Crear un mapa base centrado en LATAM
    mapa = folium.Map(location=[10, -30], zoom_start=2)

    # Agregar marcadores para los países de LATAM con números
    for idx, (country, coord) in enumerate(latam_coordinates.items(), start=1):
        folium.Marker(
            location=coord,
            popup=f"<b>{country}</b>: #{idx} en LATAM",
            icon=folium.Icon(color='blue', icon=f'{idx}')
        ).add_to(mapa)

    # Agregar marcadores para los países globales con números
    for idx, (country, coord) in enumerate(global_coordinates.items(), start=1):
        folium.Marker(
            location=coord,
            popup=f"<b>{country}</b>: #{idx} Global",
            icon=folium.Icon(color='red', icon=f'{idx}')
        ).add_to(mapa)

    # Mostrar el mapa interactivo
    st.write(f"### Paises más felices en {year}")
    #Quiero que sea el color con el label representando
    st.markdown("""
    <div style="background-color: red; padding: 10px; font-size: 16px; color: white; text-align: center;">
        Rojos = Top Global
    </div>
    <div style="background-color: blue; padding: 10px; font-size: 16px; color: white; text-align: center;">
        Azules = Top Latam
    </div>
    """, unsafe_allow_html=True)
    st.components.v1.html(mapa._repr_html_(), height=500)

def plot_happiness_comparison(latam_data, top_happiness_data):
    # Concatenar los datos de LATAM y Top Global
    latam_top_countries = latam_data.nlargest(5, 'Happiness_Score')[['Country', 'Happiness_Score']]
    global_top_countries = top_happiness_data[['Country', 'Happiness_Score']].head(5)

    # Añadir una columna para la región (LATAM o Global) para diferenciarlos
    latam_top_countries['Region'] = 'LATAM'
    global_top_countries['Region'] = 'Top Global'
    
    # Unir los DataFrames de LATAM y Top Global
    comparison_data = pd.concat([latam_top_countries, global_top_countries], axis=0)
    
    # Graficar
    plt.figure(figsize=(12, 6))
    
    # Usar un color diferente para LATAM y Top Global
    sns.barplot(data=comparison_data, x='Country', y='Happiness_Score', hue='Region', palette=["orange", "purple"])
    
    # Título y etiquetas
    plt.title('Comparación de Happiness Score entre LATAM y el Top Global', fontsize=14)
    plt.ylabel('Happiness Score', fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    
    # Mostrar el gráfico
    st.pyplot(plt)




def plot_factor_comparison_heatmap(latam_data, top_happiness_data):
    # Calcular la media de los factores para LATAM y Top Global
    latam_avg = latam_data[['Economy_GDP_per_Capita', 'Family', 'Health_Life_Expectancy', 
                            'Freedom', 'Trust_Government_Corruption', 'Generosity']].mean()
    top_avg = top_happiness_data[['Economy_GDP_per_Capita', 'Family', 'Health_Life_Expectancy', 
                                  'Freedom', 'Trust_Government_Corruption', 'Generosity']].mean()
    
    # Crear el DataFrame de comparación
    comparison_df = pd.DataFrame({
        'LATAM': latam_avg,
        'Top Global': top_avg
    })
    
    # Asegurarse de que los datos sean numéricos
    comparison_df = comparison_df.apply(pd.to_numeric, errors='coerce')
    
    # Verificar si hay valores nulos y manejarlos
    if comparison_df.isnull().values.any():
        st.warning("Algunos valores son nulos y serán ignorados en el gráfico.")
        comparison_df = comparison_df.fillna(0)  # Llenar los valores nulos con 0 o con el valor que consideres adecuado
    
    # Graficar el heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(comparison_df.T, annot=True, cmap='coolwarm', center=0)
    plt.title('Comparación de Factores de Felicidad entre LATAM y Top Global')
    st.pyplot(plt)

# Función para mostrar gráficos específicos de cada país
def plot_specific_country_analysis(latam_data, top_happiness_data, year, country_filter, region_filter):
    # Filtrar datos del país seleccionado
    country_data = latam_data[latam_data['Country'] == country_filter] if region_filter == 'LATAM' else top_happiness_data[top_happiness_data['Country'] == country_filter]

    # Si el país está en LATAM, se compara con el top global
    if region_filter == 'LATAM':
        # Extraemos las primeras 5 variables de interés para la comparación
        latam_factors = country_data[['Economy_GDP_per_Capita', 'Family', 'Health_Life_Expectancy', 
                                      'Freedom', 'Trust_Government_Corruption', 'Generosity']].values.flatten()
        
        # Promedio global para comparar
        top_avg = top_happiness_data[['Economy_GDP_per_Capita', 'Family', 'Health_Life_Expectancy', 
                                      'Freedom', 'Trust_Government_Corruption', 'Generosity']].mean().values.flatten()
        
        # Configuración del gráfico con barras separadas
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Definir los colores con alta diferencia
        color_latam = 'orange'
        color_top_global = 'purple'
        
        # Barras para LATAM
        ax.barh(['Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity'], latam_factors, 
                color=color_latam, alpha=0.7, label=f'LATAM: {country_filter}', edgecolor='black', height=0.4)
        
        # Barras para Top Global
        ax.barh(['Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity'], top_avg, 
                color=color_top_global, alpha=0.7, label='Top Global', edgecolor='black', height=0.4, left=latam_factors)
    
        # Mejorar la legibilidad del gráfico
        ax.set_xlabel('Happiness Score', fontsize=12)
        ax.set_title(f'Comparación de Factores de Felicidad: {country_filter} vs Top Global ({year})', fontsize=14)
        ax.legend()
    
        # Ajustar tamaño de los ticks para mejor legibilidad
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
    
        st.pyplot(fig)
        
        # Explicación de las diferencias clave
        st.write(f"### Análisis de las Diferencias Clave: {country_filter} vs Top Global ({year})")
        st.write(f"""
            En este gráfico comparamos los factores de felicidad de **{country_filter}** con el promedio global de los países en el top.
            Se puede observar que el país de LATAM tiene puntuaciones más bajas en ciertos factores, especialmente en **Confianza en el Gobierno** y **Generosidad**, lo que puede explicar por qué los países globales tienen mejores niveles de felicidad en estos aspectos.
        """)


    
    # Si el país está en el top global, resaltar qué lo hace estar en el top
    else:
        # Extraemos las puntuaciones del país en los factores de felicidad
        global_factors = country_data[['Economy_GDP_per_Capita', 'Family', 'Health_Life_Expectancy', 
                                       'Freedom', 'Trust_Government_Corruption', 'Generosity']].values.flatten()

        # Gráfico de barras comparativo
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(['Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity'], global_factors, color='green', alpha=0.6, label=f'{country_filter} (Top Global)')
        ax.set_xlabel('Score')
        ax.set_title(f'Factores Clave de Felicidad en {country_filter} ({year}) - Top Global')
        ax.legend()
        st.pyplot(fig)
        
        # Mostrar explicaciones sobre lo que hace al país estar en el top
        st.write(f"### Análisis de Factores Clave: {country_filter} ({year}) - Top Global")
        st.write("""
            En este gráfico se destacan los factores que han posicionado a **{country_filter}** entre los países más felices globalmente.
            Se observa que el país tiene puntuaciones altas en factores como **Generosidad** y **Confianza en el Gobierno**, lo que lo coloca en el top global.
        """)



    
def main():
    # Título de la aplicación
    st.title('Análisis de Felicidad en LATAM y el Mundo')
    # Introducción del estudio
    st.write("""
        Este análisis se centra en comparar los niveles de felicidad entre los países de LATAM y los países del top global según los datos de felicidad.
        Nos propusimos identificar las diferencias clave que afectan los niveles de felicidad en estos dos grupos de países. Para simplificar el análisis y hacerlo más manejable, decidimos centrarnos en los 5 países más felices de cada grupo (LATAM y global) como muestra representativa.
        A través de este enfoque, buscamos entender mejor qué factores influyen en la felicidad y cómo estos varían entre las regiones.
    """)
    
    # Filtro de año
    year = st.sidebar.selectbox('Seleccionar Año', [2015, 2016])
    
    # Cargar datos según el año seleccionado
    latam_data, top_happiness_data = load_data(year)
    
    # Verificación de los datos cargados
    if latam_data.empty:
        st.error("No se encontraron datos para LATAM en el año seleccionado.")
    
    # Filtro de "Información General" o "Específica"
    info_filter = st.sidebar.selectbox('Seleccionar tipo de información', ['Información General', 'Información Específica'])
    
    # Si se selecciona "Información Específica"
    if info_filter == 'Información Específica':
        # Filtro de región (LATAM o Global)
        region_filter = st.sidebar.selectbox('Seleccionar Región', ['LATAM', 'Global'])

        # Filtros de selección de países
        st.sidebar.header('Filtros de Selección')
        
        # Si se selecciona LATAM, solo mostramos los primeros 5 países más felices de LATAM
        if region_filter == 'LATAM':
            if not latam_data.empty:  # Verificamos que haya datos
                top_latam_countries = latam_data.nlargest(10, 'Happiness_Score')['Country'].tolist()
            else:
                top_latam_countries = []
        else:
            if not top_happiness_data.empty:  # Verificamos que haya datos
                top_latam_countries = top_happiness_data['Country'].tolist()
            else:
                top_latam_countries = []

        # Si no hay países disponibles, mostramos un mensaje de error
        if not top_latam_countries:
            st.error("No hay países disponibles para la selección en la región elegida.")
            return
        
        country_filter = st.sidebar.selectbox('Seleccionar un país', top_latam_countries)
        st.sidebar.markdown('---')
        
        # Muestra los datos del país seleccionado
        country_data = latam_data[latam_data['Country'] == country_filter] if region_filter == 'LATAM' else top_happiness_data[top_happiness_data['Country'] == country_filter]
        
        st.write(f'**Datos para {country_filter} ({year}):**')
        st.write(country_data)

        plot_specific_country_analysis(latam_data, top_happiness_data, year, country_filter, region_filter)


        # Mostrar graficos especificos para cada pais, para los de latam mostrar comparaciones de por que les ganan los del top global, y para los del top globar resaltar que los hace estar en el top
    
    # Si se selecciona "Información General"
    else:
        # Mostrar las gráficas generales (porcentaje de diferencia entre LATAM y Top Global)
        st.header('Análisis General por Año')
        comparison_df = calculate_comparison(latam_data, top_happiness_data)
        plot_comparison(comparison_df, year)
        
        # Explicaciones específicas para los años 2015 y 2016
        if year == 2015:
            st.markdown("""
            **En 2015, lo que más contribuyó a la diferencia de felicidad entre el Top Global y LATAM fue la confianza en el gobierno.** 
            Los países con mayor felicidad en el ranking global, como Dinamarca y Suiza, tienen niveles de confianza en las instituciones gubernamentales mucho más altos en comparación con muchos países de LATAM. Esto se traduce en una mayor sensación de seguridad y bienestar, lo que impacta directamente en los niveles de felicidad general de la población.
            """)
        elif year == 2016:
            st.markdown("""
            **En 2016, la generosidad fue el factor clave que diferenció el Top Global de LATAM.**
            A pesar de que LATAM tiene una fuerte red de apoyo familiar y social, los países más felices globalmente, como Dinamarca y Noruega, mostraron altos niveles de generosidad, medida por la disposición de los ciudadanos a donar tiempo o dinero. Esta generosidad está asociada con una mayor cohesión social y un sentido de comunidad, lo cual tiene un impacto directo en los niveles de felicidad de esos países.
            """)


        # Mostrar mapa de LATAM y países globales
        st.header('Mapa de LATAM y Países Globales')
        display_maps(year)
        
        # Explicación sobre la ubicación geográfica y su relación con la felicidad
        st.markdown("""
        Aunque podríamos suponer que la ubicación geográfica de los países podría tener una influencia directa en sus niveles de felicidad, 
        la comparación entre los países de LATAM y los países globales más felices no muestra una correlación clara entre la ubicación y la felicidad.
        
        Si observamos el mapa, vemos que, por ejemplo, países como Costa Rica en LATAM y Dinamarca en Europa están ubicados en diferentes continentes, 
        pero ambos están entre los países con mayor felicidad en sus respectivas regiones. Sin embargo, no hay una tendencia uniforme que sugiera que los países geográficamente cercanos 
        tienen niveles de felicidad similares, ni que aquellos en ciertas latitudes sean más felices que otros. 
        
        Esto indica que factores como la **economía**, **confianza en el gobierno**, **libertad individual**, y la **generosidad** tienen un peso mucho más significativo en los niveles de felicidad 
        que la ubicación geográfica en sí misma. En resumen, los datos sugieren que la felicidad global está más influenciada por variables sociales y políticas que por la proximidad geográfica.
        """)

        # Llamar la función para mostrar el gráfico
        st.header(f'Gráfico de barras comparativo entre los países de LATAM y el Top Global por Happiness Score para {year}')
        plot_happiness_comparison(latam_data, top_happiness_data)
        
        # Conclusiones
        st.write("""
        ### Conclusiones:
        
        1. **Desempeño global**: Los países del **Top Global** (principalmente los países nórdicos y de Europa Occidental) mantienen **puntajes significativamente más altos** en comparación con los países de LATAM. Esto refleja las diferencias en los niveles de felicidad, impulsadas por factores como la **confianza en el gobierno**, **generosidad** y una **economía estable**.
        
        2. **Diferencias clave**: Los países de LATAM, aunque con avances en áreas como **Economía** y **Familia**, siguen estando rezagados en aspectos como la **confianza en el gobierno** y la **generosidad**, lo que afecta negativamente su puntaje general de felicidad.
        
        3. **Tendencia estable**: En los años 2015 y 2016, la diferencia entre los países de LATAM y los del Top Global se mantiene constante, con **LATAM** mostrando consistentemente puntajes más bajos en comparación.
        
        4. **Impacto de los factores clave**: El gráfico evidencia que, aunque los países de LATAM tienen altos puntajes en **familia** y **salud**, siguen enfrentando desafíos en áreas críticas como la **confianza institucional** y la **generosidad**. Estos factores parecen ser cruciales para que los países del **Top Global** alcancen niveles superiores de felicidad.
        
        5. **Recomendaciones**: Para mejorar la felicidad en LATAM, sería fundamental enfocarse en mejorar la **confianza en el gobierno**, la **generosidad** y fortalecer las **políticas económicas** que fomenten la estabilidad social y financiera.
        
        En resumen, las diferencias en los puntajes de felicidad entre LATAM y el Top Global se deben en gran parte a aspectos sociales y políticos que requieren atención para promover el bienestar de la población en la región LATAM.
        """)


        # Llamar la función para mostrar el gráfico
        st.header(f'Comparación de factores de felicidad entre los países LATAM y el Top Global (Heatmap de correlación) para {year}')
        plot_factor_comparison_heatmap(latam_data, top_happiness_data)

        if year == 2015:
        # Conclusiones para 2015
            st.write("""
            ### Conclusiones:
            
                **Factores clave para la felicidad**:
               - El **Heatmap de correlación** para el año 2015 revela que la **confianza en el gobierno** fue el factor más influyente que diferenció a los países del **Top Global** frente a los países de **LATAM**. Los países del Top Global mostraron una mayor confianza en sus gobiernos, lo que se reflejó en niveles de felicidad más altos.
               - Además, la **generosidad** en los países del Top Global fue significativamente mayor, lo cual podría haber influido positivamente en sus niveles de bienestar y cohesión social.
               - **Familia** y **Economía** mostraron correlaciones relativamente fuertes en ambos grupos, aunque los países de LATAM quedaron por debajo de los puntajes de los países en el Top Global.
            """)
        else:
            st.write("""
            ### Conclusiones:
            
                **Factores clave para la felicidad**:
               - El **Heatmap de correlación** para el año 2016 muestra que **la generosidad** fue un factor aún más destacado en los países del **Top Global**, lo que refleja una mayor disposición de los ciudadanos a compartir recursos, contribuyendo al bienestar general y la cohesión social. Este factor fue clave para que los países del Top Global mantuvieran altos niveles de felicidad en comparación con LATAM.
               - A diferencia de 2015, la **confianza en el gobierno** no fue tan decisiva en 2016. Aunque los países del Top Global continuaron mostrando una mayor confianza, la **salud** y **libertad** se destacaron como factores de mayor impacto en la felicidad, lo que puede reflejar avances en la calidad de vida y en la autonomía de los ciudadanos en esos países.
               - **Economía** y **Familia** mantuvieron una correlación importante, aunque los países de LATAM todavía presentaron deficiencias en áreas como **confianza** y **generosidad**, lo que los coloca por debajo del promedio de felicidad global.
        
            """)

    st.write("""
    ### Referencias:
    
    Los datos utilizados en este análisis provienen del siguiente dataset:
    
    - **World Happiness Report**: El dataset utilizado para este análisis se extrajo de la plataforma Kaggle. Puedes acceder al conjunto de datos original en el siguiente enlace:
      [World Happiness Report Dataset - Kaggle](https://www.kaggle.com/datasets/unsdsn/world-happiness/data)
    
    Este conjunto de datos contiene información sobre los niveles de felicidad en diferentes países a lo largo de los años, y fue proporcionado por el *Sustainable Development Solutions Network* (SDSN).
    """)



# Ejecutar la aplicación
if __name__ == "__main__":
    main()


