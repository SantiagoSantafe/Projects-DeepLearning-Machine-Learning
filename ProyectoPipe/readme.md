# Análisis de Felicidad: Proyecto en Streamlit

Este proyecto tiene como objetivo analizar los niveles de felicidad en los países de LATAM y los países del Top Global, utilizando los datos del **World Happiness Report**. La aplicación está desarrollada en **Streamlit**, y hace uso de herramientas como **pandas**, **matplotlib**, **seaborn**, **sqlite3** y **folium** para la carga, procesamiento y visualización de los datos.

## Tabla de Contenidos

1. [Cómo correr el código](#cómo-correr-el-código)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Uso de la Aplicación](#uso-de-la-aplicación)
4. [Cómo ejecutar el archivo `.ipynb`](#cómo-ejecutar-el-archivo-ipynb)
5. [Referencias](#referencias)

## Cómo correr el código

Sigue estos pasos para ejecutar la aplicación y realizar el análisis:

### Paso 1: Clonar el repositorio
Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/tu-usuario/proyecto-happiness
```

## Paso 2: Crear un entorno virtual (opcional, pero recomendado)
Es recomendable crear un entorno virtual para gestionar las dependencias del proyecto. Si estás utilizando **venv**, ejecuta:

```bash
python -m venv venv
```

## Paso 3: Activar el entorno virtual

- En **Windows**:
```bash
venv\Scripts\activate
```

- En **macOS/Linux**:
```bash
source venv/bin/activate
```

## Paso 4: Instalar las dependencias
Instala las dependencias necesarias ejecutando:
```bash
pip install streamlit pandas matplotlib seaborn sqlite3 folium numpy
```
## Paso 5: Preparar la base de datos
Asegúrate de tener los archivos de datos necesarios en el proyecto:

- `happiness_data.db`: Base de datos SQLite con los datos de felicidad.
- `2015.cv` y `2016.cv`: Archivos de datos con la información para esos años.

## Paso 6: Ejecutar la aplicación en Streamlit
Para iniciar la aplicación, ejecuta:
```bash
streamlit run app.py
```

Esto abrirá una ventana en tu navegador donde podrás interactuar con la aplicación y visualizar los análisis.

## Estructura del Proyecto

La estructura del proyecto es la siguiente:
```bash
/proyecto-happiness │ ├── app.py # Archivo principal con la aplicación en Streamlit ├── happiness_data.db # Base de datos SQLite con los datos de felicidad ├── 2015.cv # Datos del año 2015 ├── 2016.cv # Datos del año 2016 ├── ProyectoTomaDecisiones.ipynb # Notebook de análisis complementario ├── requirements.txt # Archivo de dependencias del proyecto └── README.md # Este archivo
```


- **app.py**: Código principal de la aplicación en Streamlit que procesa y visualiza los datos.
- **happiness_data.db**: Base de datos con los datos de felicidad por país.
- **2015.cv y 2016.cv**: Archivos de datos para los años correspondientes.
- **ProyectoTomaDecisiones.ipynb**: Jupyter Notebook adicional con análisis complementarios.
- **requirements.txt**: Archivo con las dependencias necesarias para ejecutar el proyecto.

---

## Uso de la Aplicación

La aplicación permite visualizar y analizar los datos de felicidad para los países de LATAM y los países del Top Global. Las características principales incluyen:

- **Seleccionar Año**: Elige entre los años 2015 y 2016.
- **Información General vs Específica**: Selecciona entre ver análisis general o información específica de países de LATAM o del Top Global.
- **Comparación de Factores de Felicidad**: Gráficos comparativos de felicidad entre las dos regiones y factores de felicidad.
- **Mapas Interactivos**: Mapa interactivo mostrando la ubicación de los países de LATAM y el Top Global.

---

## Cómo ejecutar el archivo `.ipynb`

El archivo **`ProyectoTomaDecisiones.ipynb`** proporciona un análisis complementario sobre la toma de decisiones basada en los datos de felicidad. Sigue estos pasos para ejecutarlo:

1. **Instalar Jupyter Notebook** (si aún no lo tienes instalado):
```bash
pip install notebook
```

2. **Ejecutar el Notebook**:

Navega hasta el directorio que contiene el archivo **`ProyectoTomaDecisiones.ipynb`** y ejecuta:

```bash
jupyter notebook
```


3. **Abrir y ejecutar el archivo**:

En la interfaz de Jupyter, abre el archivo **`ProyectoTomaDecisiones.ipynb`** y ejecuta todas las celdas para obtener los resultados.

---

## Referencias

Los datos utilizados en este análisis provienen del siguiente dataset:

- **World Happiness Report**: El dataset utilizado para este análisis se extrajo de la plataforma Kaggle. Puedes acceder al conjunto de datos original en el siguiente enlace:

[World Happiness Report Dataset - Kaggle](https://www.kaggle.com/datasets/unsdsn/world-happiness/data)

Este conjunto de datos contiene información sobre los niveles de felicidad en diferentes países a lo largo de los años, y fue proporcionado por el *Sustainable Development Solutions Network* (SDSN).







