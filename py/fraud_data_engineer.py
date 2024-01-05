from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler, StandardScaler
from pyspark.sql.functions import col, when

class FraudDataEngineer:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def calculate_balance_differences(self):
        self.dataframe = self.dataframe.withColumn(
            'originBalanceError',
            col('oldbalanceOrg') - col('newbalanceOrig') - col('amount')
        ).withColumn(
            'destinationBalanceError',
            col('oldbalanceDest') + col('amount') - col('newbalanceDest')
        )

    def calculate_discrepancies(self):
        self.dataframe = self.dataframe.withColumn(
            'originBalanceZero',
            when((col('oldbalanceOrg') == 0) & (col('newbalanceOrig') == 0), 1).otherwise(0)
        ).withColumn(
            'destinationBalanceZero',
            when((col('oldbalanceDest') == 0) & (col('newbalanceDest') == 0), 1).otherwise(0)
        )

    def apply_one_hot_encoding(self):
        string_indexer = StringIndexer(inputCol='type', outputCol='typeIndex')
        model = string_indexer.fit(self.dataframe)
        indexed = model.transform(self.dataframe)

        encoder = OneHotEncoder(inputCols=['typeIndex'], outputCols=['typeVec'])
        self.dataframe = encoder.fit(indexed).transform(indexed)
        self.dataframe = self.dataframe.drop('type', 'typeIndex')

    def apply_standard_scaling(self):
        columns_to_scale = ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest', 'originBalanceError', 'destinationBalanceError']
        assembler = VectorAssembler(inputCols=columns_to_scale, outputCol="features")
        self.dataframe = assembler.transform(self.dataframe)

        scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
        self.dataframe = scaler.fit(self.dataframe).transform(self.dataframe)

    def add_origin_destination_match(self):
        self.dataframe = self.dataframe.withColumn(
            'originDestinationMatch',
            when(col('nameOrig') == col('nameDest'), 1).otherwise(0)
        )

    def add_fraud_flag_match(self):
        self.dataframe = self.dataframe.withColumn(
            'fraudFlagMatch',
            when(col('isFraud') == col('isFlaggedFraud'), 1).otherwise(0)
        )