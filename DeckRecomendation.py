import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Carregar os dados
labeled_decks = pd.read_csv('data/labeled_decks.csv')
structured_decks = pd.read_csv('output/structured_decks.csv')

# Pré-processamento dos dados
# No labeled_decks, as cartas são combinadas em um texto
labeled_decks['Deck Text'] = labeled_decks['Deck Text'].apply(lambda x: ' '.join(x.split(',')))

# Vetorização com TF-IDF para transformar as cartas em números
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(labeled_decks['Deck Text'])

# Labels: O nome do deck correspondente (coluna 'Matched Deck')
y = labeled_decks['Matched Deck']

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Balancear os dados de treino com SMOTE (se necessário)
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Definir o modelo RandomForest e fazer ajuste de hiperparâmetros com GridSearchCV
rf = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2', None]
}

grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train_res, y_train_res)

# Melhor modelo encontrado
best_rf = grid_search.best_estimator_

# Avaliar o modelo no conjunto de teste
y_pred = best_rf.predict(X_test)

# Relatório de desempenho
print("Desempenho do modelo:")
print(classification_report(y_test, y_pred))

# Agora, use o modelo para fazer o matching de decks no structured_decks
# Pré-processamento para o structured_decks
structured_decks['Deck Text'] = structured_decks['Deck Text'].apply(lambda x: ' '.join(x.split(',')))

# Vetorização para os decks estruturados
X_structured = vectorizer.transform(structured_decks['Deck Text'])

# Fazer previsões de match de deck
structured_decks['Predicted Deck'] = best_rf.predict(X_structured)

output_file = 'data/matching_trained_results.csv'

# Limpar o conteúdo do arquivo antes de salvar (opcional, redundante com to_csv)
with open(output_file, 'w') as f:
    f.write('')

structured_decks[['Deck Text', 'Predicted Deck']].to_csv(output_file, index=False)
