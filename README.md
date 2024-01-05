# Proyecto de Detección de Fraude en Línea

## Descripción
Este proyecto implementa un sistema de detección de fraude en línea utilizando PySpark y técnicas de aprendizaje automático para identificar transacciones fraudulentas en datos de tarjetas de crédito.

## Características
- Análisis exploratorio de datos utilizando PySpark y Plotly para visualizaciones.
- Preprocesamiento y ingeniería de características para preparar los datos para el modelado.
- Entrenamiento de modelos de clasificación de aprendizaje automático como Random Forest y Gradient Boosting.
- Evaluación de modelos utilizando AUC-ROC y Precisión-Recuerdo.
- Interfaz de usuario para cargar datos y visualizar resultados utilizando Streamlit o Dash.

## Estructura del Proyecto

- data_loader.py: Clase para cargar y previsualizar los datos.
- data_visualizer.py: Clase para visualizar los datos.
- fraud_data_engineer.py: Clase para la ingeniería de características.
- data_preparation.py: Clase para la preparación de los conjuntos de datos de entrenamiento y prueba.
- fraud_model.py: Clase para el entrenamiento y evaluación del modelo.
- app.py (Opcional): Una aplicación Streamlit para demostrar el uso del modelo.
- dashboard.py (Opcional): Un dashboard Dash para visualizaciones interactivas.
- /models: Directorio donde se almacenan los modelos entrenados.
- requirements.txt: Archivo con las dependencias del proyecto.

## Configuración del Entorno
Se recomienda utilizar un entorno virtual para las dependencias del proyecto.
```bash
python -m venv venv
source venv/bin/activate  # En Windows use `venv\Scripts\activate`
pip install -r requirements.txt



## Uso

Cargue sus datos en formato CSV utilizando la interfaz de usuario de Streamlit o Dash.
Revise las visualizaciones generadas para comprender los datos.
Ejecute el modelo para detectar posibles transacciones fraudulentas.
(Opcional) Ajuste los parámetros del modelo y reentrénelo según sea necesario.


## Licencia

Este proyecto está bajo la licencia [MIT].

Contacto
[https://www.linkedin.com/in/adrianinfantes]