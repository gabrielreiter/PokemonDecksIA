import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Carregar os dados
structured_decks = pd.read_csv('output/structured_decks.csv')  # Dados dos decks estruturados
metagame = pd.read_csv('output/metagame.csv')  # Metagame decks
labeled_decks = pd.read_csv('data/labeled_decks.csv')  # Dados de treino rotulados

# Filtrar apenas as cartas de Pokémon (ignorando Trainers e Energias)
structured_decks_pokemon = structured_decks[structured_decks['Category'] == 'Pokémon']

# Agrupar as cartas do mesmo deck usando o 'ID' e criar a coluna 'Deck Text'
structured_decks_pokemon['Deck Text'] = structured_decks_pokemon.groupby('ID')['Card Name'].transform(lambda x: ' '.join(x))

# Remover duplicatas para garantir que cada ID de deck tenha apenas um texto concatenado
structured_decks_unique = structured_decks_pokemon[['ID', 'Deck Text']].drop_duplicates()

# Preparar os dados de treinamento a partir do CSV de decks rotulados
X = labeled_decks['Deck Text']  # Características (Deck Text)
y = labeled_decks['Matched Deck']  # Rótulos (Matched Deck)

print("Distribuição dos rótulos no conjunto de dados:")
print(y.value_counts())

# Vetorizar os textos dos decks (transformar as palavras em números)
vectorizer = CountVectorizer(
    stop_words='english', 
    ngram_range=(1, 2),  # Unigramas e bigramas
    max_df=0.95,  # Ignorar termos muito frequentes
    min_df=2,  # Ignorar termos muito raros
    max_features=5000  # Limitar número total de características
)

# Armazenar as métricas de avaliação
accuracy_scores = []
classification_reports = []

# Número de iterações de treinamento
n_iterations = 1

# Loop para treinar e avaliar o modelo várias vezes
for iteration in range(n_iterations):
    print(f"\nIniciando iteração {iteration+1}/{n_iterations}")
    
    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42 + iteration)

    # Vetorizar os dados de treino e teste
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Treinar o modelo Random Forest
    rf_classifier = RandomForestClassifier(n_estimators=1000, max_depth=50, min_samples_split=10, random_state=42 + iteration, class_weight='balanced')
    rf_classifier.fit(X_train_vec, y_train)

    # Fazer previsões nos decks de teste
    predictions = rf_classifier.predict(X_test_vec)

    print("Distribuição das classes no conjunto de treinamento:")
    print(y_train.value_counts())

    print("Distribuição das classes no conjunto de teste:")
    print(y_test.value_counts())

    # Avaliar o modelo
    print(f"Classification Report - Iteração {iteration+1}:")
    class_report = classification_report(y_test, predictions, zero_division=1, output_dict=True)
    print(class_report)
    classification_reports.append(class_report)
    accuracy_scores.append(class_report['accuracy'])

    # Matriz de confusão
    print(f"Confusion Matrix - Iteração {iteration+1}:")
    print(confusion_matrix(y_test, predictions))

# Exibir o desempenho médio após todas as iterações
average_accuracy = np.mean(accuracy_scores)
print(f"\nAcurácia média após {n_iterations} iterações: {average_accuracy:.4f}")

# Calcular a média dos valores de precision, recall e f1-score para cada classe
def average_class_report(classification_reports):
    # Inicializar listas para cada métrica
    precision = []
    recall = []
    f1_score = []
    
    # Iterar sobre cada relatório de classificação e coletar as métricas para cada classe
    for report in classification_reports:
        for label, metrics in report.items():
            if label not in ['accuracy', 'macro avg', 'weighted avg']:  # Ignorar as médias gerais
                precision.append(metrics['precision'])
                recall.append(metrics['recall'])
                f1_score.append(metrics['f1-score'])
    
    # Calcular a média das métricas
    avg_precision = np.mean(precision)
    avg_recall = np.mean(recall)
    avg_f1_score = np.mean(f1_score)
    
    return avg_precision, avg_recall, avg_f1_score

# Calcular as médias
avg_precision, avg_recall, avg_f1_score = average_class_report(classification_reports)
print("\nMédia do Classification Report (precision, recall, f1-score):")
print(f"Precision Média: {avg_precision:.4f}")
print(f"Recall Média: {avg_recall:.4f}")
print(f"F1-Score Média: {avg_f1_score:.4f}")

# Realizar as previsões finais para o 'structured_decks' usando o último modelo treinado
structured_decks_predictions = rf_classifier.predict(vectorizer.transform(structured_decks_unique['Deck Text']))

# Adicionar as previsões no dataframe
structured_decks_unique['Matched Deck'] = structured_decks_predictions

# Salvar os resultados no arquivo CSV
output_file = 'data/matching_trained_results.csv'
structured_decks_unique[['ID', 'Deck Text', 'Matched Deck']].to_csv(output_file, index=False)

print(f"\nPrevisões de matching salvas em {output_file}")
