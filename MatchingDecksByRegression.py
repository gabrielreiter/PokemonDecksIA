import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Carregar os dados
structured_decks = pd.read_csv('output/structured_decks.csv')  # Dados dos decks estruturados
labeled_decks = pd.read_csv('data/labeled_decks.csv')  # Dados de treino rotulados

# Filtrar apenas as cartas de Pokémon
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

# Vetorizar os textos dos decks
vectorizer = CountVectorizer(
    stop_words='english', 
    ngram_range=(1, 2),  # Unigramas e bigramas
    max_df=0.95, 
    min_df=2, 
    max_features=5000
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
    
    # Treinar o modelo
    lr_classifier = LogisticRegression(max_iter=1000, class_weight='balanced')
    lr_classifier.fit(X_train_vec, y_train)
    predictions = lr_classifier.predict(X_test_vec)

    # Armazenar as métricas
    accuracy = accuracy_score(y_test, predictions)
    accuracy_scores.append(accuracy)

    report = classification_report(y_test, predictions, output_dict=True, zero_division=1)
    classification_reports.append(report)

    print("Relatório de Classificação - Logistic Regression:")
    print(classification_report(y_test, predictions, zero_division=1))

# Exibir o desempenho médio após todas as iterações
average_accuracy = np.mean(accuracy_scores)
print(f"\nAcurácia média após {n_iterations} iterações: {average_accuracy:.4f}")

# Calcular a média dos valores de precision, recall e f1-score para cada classe
def average_class_report(reports):
    precision = []
    recall = []
    f1_score = []
    
    for report in reports:
        for label, metrics in report.items():
            if label not in ['accuracy', 'macro avg', 'weighted avg']:
                precision.append(metrics['precision'])
                recall.append(metrics['recall'])
                f1_score.append(metrics['f1-score'])
    
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
structured_decks_predictions = lr_classifier.predict(vectorizer.transform(structured_decks_unique['Deck Text']))

# Adicionar as previsões no dataframe
structured_decks_unique['Matched Deck'] = structured_decks_predictions

# Salvar os resultados no arquivo CSV
output_file = 'data/matching_trained_results.csv'
structured_decks_unique[['ID', 'Deck Text', 'Matched Deck']].to_csv(output_file, index=False)

print(f"\nPrevisões de matching salvas em {output_file}")
