import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class DataVisualizer:
    def __init__(self, spark_dataframe):
        self.dataframe = spark_dataframe

    def to_pandas_df(self, spark_df):
        """Convierte un DataFrame de Spark a un DataFrame de Pandas."""
        return spark_df.toPandas()

    # Visualización de la distribución de una columna específica
    def plot_distribution(self, column, title):
        pandas_df = self.to_pandas_df(self.dataframe)
        fig = px.histogram(pandas_df, x=column, title=title)
        fig.update_layout(bargap=0.2)
        fig.show()

    # Visualización de un diagrama de caja para una columna específica
    def plot_box(self, column, title):
        pandas_df = self.to_pandas_df(self.dataframe)
        fig = px.box(pandas_df, y=column, title=title)
        fig.show()

    # Visualización de la matriz de correlación
    def plot_correlation_matrix(self, title):
        # Convert Spark DataFrame to Pandas DataFrame
        pandas_df = self.to_pandas_df(self.dataframe)

        # Select only numeric columns for the correlation matrix
        numeric_df = pandas_df.select_dtypes(include=[np.number])

        # Calculate the correlation matrix
        correlation_matrix = numeric_df.corr()

        # Create the figure for the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='Viridis'))
        fig.update_layout(title=title, xaxis_nticks=len(correlation_matrix.columns),
                          yaxis_nticks=len(correlation_matrix.columns))

        # Return the figure
        return fig

    # Análisis específicos para columnas seleccionadas
    def analyze_specific_columns(self):
        self.plot_distribution('step', 'Distribución de Tiempo (Step)')
        self.plot_distribution('isFraud', 'Distribución de Fraudes')
        self.plot_distribution('isFlaggedFraud', 'Distribución de Transacciones Marcadas como Fraude')
        self.plot_distribution('type', 'Distribución de Tipos de Transacciones')
        self.plot_box('amount', 'Distribución de Montos')