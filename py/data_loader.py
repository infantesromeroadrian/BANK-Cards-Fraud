from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnan, when, count

class DataLoader:
    def __init__(self, filepath, sample_size=0.1):
        self.filepath = filepath
        self.sample_size = sample_size
        self.spark = SparkSession.builder.appName("DataLoader").getOrCreate()
        self.data = None

    def load_data(self):
        try:
            full_data = self.spark.read.csv(self.filepath, header=True, inferSchema=True)
            self.data = full_data.sample(withReplacement=False, fraction=self.sample_size, seed=42)
            print("Datos cargados con éxito.")
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            self.data = None

    def show_head(self, n=5):
        """Muestra las primeras 'n' filas del dataset."""
        if self.data is not None:
            return self.data.limit(n).toPandas()
        else:
            print("Datos no cargados. Por favor, carga los datos primero.")

    def get_columns_info(self):
        """Devuelve información sobre las columnas del dataset."""
        if self.data is not None:
            return self.data.dtypes
        else:
            print("Datos no cargados. Por favor, carga los datos primero.")

    def get_null_values(self):
        """Devuelve información sobre las columnas del dataset."""
        if self.data is not None:
            return self.data.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in self.data.columns]).toPandas()
        else:
            print("Datos no cargados. Por favor, carga los datos primero.")

    def check_fraud_balance(self):
        """Comprueba el balance de la columna 'isFraud'."""
        if self.data is not None:
            fraud_count = self.data.groupBy("isFraud").count()
            fraud_count.show()
        else:
            print("Datos no cargados. Por favor, carga los datos primero.")