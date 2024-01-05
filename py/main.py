# Importar las clases necesarias
from data_loader import DataLoader
from data_visualizer import DataVisualizer
from fraud_data_engineer import FraudDataEngineer
from data_preparation import DataPreparation
from fraud_model import FraudModel

def main():
    # Ruta al archivo CSV
    filepath = '/Users/adrianinfantes/Desktop/AIR/COLLEGE AND STUDIES/Data_Scientist_formation/Portfolio/BankProjects/OnlineFraud/data/onlinefraud.csv'

    # Inicialización y carga de datos
    data_loader = DataLoader(filepath)
    data_loader.load_data()

    # Visualización de datos
    data_visualizer = DataVisualizer(data_loader.data)
    data_visualizer.analyze_specific_columns()

    # Ingeniería de características
    data_engineer = FraudDataEngineer(data_loader.data)
    data_engineer.calculate_balance_differences()
    data_engineer.calculate_discrepancies()
    data_engineer.apply_one_hot_encoding()
    data_engineer.apply_standard_scaling()
    data_engineer.add_origin_destination_match()
    data_engineer.add_fraud_flag_match()

    # Preparación de los datos para el modelo
    data_preparation = DataPreparation(data_engineer.dataframe)
    train_df, test_df = data_preparation.split_data('isFraud', columns_to_exclude=['nameOrig', 'nameDest'])

    # Entrenamiento y evaluación del modelo
    fraud_model = FraudModel(train_df, test_df)
    fraud_model.train_model()
    evaluation_results = fraud_model.evaluate_model()
    print(evaluation_results)

    # Guardar el modelo
    fraud_model.model.write().overwrite().save('model/fraud_model')

if __name__ == "__main__":
    main()
