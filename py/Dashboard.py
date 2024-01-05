import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from data_visualizer import DataVisualizer
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnan, isnull, countDistinct, avg, stddev, min, max, corr, round

# Tu clase DataVisualizer debería estar definida aquí o importada si está en otro archivo

# Inicializar Spark
spark = SparkSession.builder.appName("DataVisualizationApp").getOrCreate()

# Supongamos que tienes un DataFrame de Spark llamado 'spark_df' listo para visualizar
# Aquí, usarás un DataFrame de Pandas para fines de demostración.
# Deberás reemplazar esto con tu DataFrame de Spark real.
pandas_df = pd.DataFrame({
    'step': [1, 2, 3, 4, 5],
    'isFraud': [0, 1, 0, 1, 0],
    'isFlaggedFraud': [0, 0, 0, 1, 0],
    'type': ['TRANSFER', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'],
    'amount': [10.5, 20.0, 5.0, 7.5, 8.0]
})

# Convertir el DataFrame de Pandas a un DataFrame de Spark
spark_df = spark.createDataFrame(pandas_df)

# Crear una instancia de la clase DataVisualizer con tu DataFrame de Spark
visualizer = DataVisualizer(spark_df)

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Definir la disposición de la aplicación
app.layout = html.Div([
    html.H1("Data Visualization App"),
    dcc.Graph(id='distribution-graph'),
    dcc.Dropdown(
        id='distribution-column',
        options=[{'label': col, 'value': col} for col in spark_df.columns],
        value='step'
    ),
    html.Hr(),
    html.H2("Correlation Matrix"),
    dcc.Graph(figure=visualizer.plot_correlation_matrix("Correlation Matrix"), id='correlation-matrix')
])

# Definir la interactividad de la aplicación
@app.callback(
    Output('distribution-graph', 'figure'),
    [Input('distribution-column', 'value')]
)
def update_graph(column_name):
    return visualizer.plot_distribution(column_name, f'Distribution of {column_name}')

# Correr la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
