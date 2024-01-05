from pyspark.sql.functions import col


class DataPreparation:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def split_data(self, target_column, test_size=0.2, seed=42, columns_to_exclude=None):
        if columns_to_exclude is None:
            columns_to_exclude = []

        # Seleccionar las columnas relevantes
        columns_to_include = [column for column in self.dataframe.columns if
                              column not in columns_to_exclude + [target_column]]

        # Dividir el DataFrame
        train_df, test_df = self.dataframe.randomSplit([1.0 - test_size, test_size], seed=seed)

        # Combinar características y etiquetas
        train_df = train_df.select([col(target_column).alias("label")] + columns_to_include)
        test_df = test_df.select([col(target_column).alias("label")] + columns_to_include)

        return train_df, test_df