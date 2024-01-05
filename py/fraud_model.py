from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

class FraudModel:
    def __init__(self, train_data, test_data, label_col='label', features_col='features'):
        self.train_data = train_data
        self.test_data = test_data
        self.label_col = label_col
        self.features_col = features_col
        self.model = None
        self.predictions = None

    def train_model(self, model_type='random_forest'):
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(labelCol=self.label_col, featuresCol=self.features_col)
        elif model_type == 'gradient_boosting':
            self.model = GBTClassifier(labelCol=self.label_col, featuresCol=self.features_col)
        # Añadir más algoritmos según sea necesario

        self.model = self.model.fit(self.train_data)

    def cross_validate_model(self, param_grid, num_folds=5):
        crossval = CrossValidator(estimator=self.model,
                                  estimatorParamMaps=param_grid,
                                  evaluator=BinaryClassificationEvaluator(labelCol=self.label_col),
                                  numFolds=num_folds)
        cv_model = crossval.fit(self.train_data)
        self.model = cv_model.bestModel

    def evaluate_model(self):
        evaluator = BinaryClassificationEvaluator(labelCol=self.label_col, rawPredictionCol="rawPrediction")
        self.predictions = self.model.transform(self.test_data)
        auc = evaluator.evaluate(self.predictions, {evaluator.metricName: "areaUnderROC"})
        auprc = evaluator.evaluate(self.predictions, {evaluator.metricName: "areaUnderPR"})
        # Añadir más métricas si es necesario

        return {"areaUnderROC": auc, "areaUnderPR": auprc}