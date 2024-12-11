import pandas as pd
from difflib import SequenceMatcher
from sklearn.metrics import classification_report, accuracy_score

# Função para calcular a similaridade entre duas strings
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Função para encontrar o melhor match entre um deck e a lista de metagame decks
def find_best_match(deck_text, metagame_decks):
    best_match = None
    highest_similarity = 0
    for metagame_deck in metagame_decks:
        sim = similarity(deck_text, metagame_deck)
        if sim > highest_similarity:
            highest_similarity = sim
            best_match = metagame_deck
    return best_match

# Carregar os dados
structured_decks = pd.read_csv('output/structured_decks.csv')  # CSV com os decks estruturados
metagame = pd.read_csv('output/metagame.csv', header=None, names=['Matched Deck'])  # Decks do metagame
labeled_decks = pd.read_csv('data/labeled_decks.csv')  # CSV com os rótulos verdadeiros para avaliação

# Obter os nomes dos decks no metagame
metagame_decks = metagame['Matched Deck'].tolist()

# Filtrar apenas as cartas de Pokémon
pokemon_decks = structured_decks[structured_decks['Category'] == 'Pokémon']

# Agrupar as cartas por ID e criar o texto de cada deck
deck_texts = (
    pokemon_decks.groupby('ID')['Card Name']  # Agrupa pelos IDs e usa os nomes das cartas
    .apply(lambda x: ' '.join(x))  # Junta todas as cartas de um deck em um único texto
    .reset_index(name='Deck Text')  # Cria uma nova coluna 'Deck Text' com o texto do deck
)

# Fazer o matching entre os decks estruturados e os do metagame
deck_texts['Matched Deck_predicted'] = deck_texts['Deck Text'].apply(
    lambda x: find_best_match(x, metagame_decks)
)

# Garantir que as colunas de rótulos verdadeiros estejam presentes
if 'Deck Text' in labeled_decks.columns and 'Matched Deck' in labeled_decks.columns:
    labeled_decks.rename(columns={'Matched Deck': 'Matched Deck_true'}, inplace=True)
else:
    raise ValueError("As colunas 'Deck Text' ou 'Matched Deck' não existem em 'labeled_decks.csv'.")

# Combinar com os rótulos verdadeiros (mantendo todos os decks)
results = pd.merge(deck_texts, labeled_decks, on='Deck Text', how='left')

# Preencher valores ausentes nos rótulos verdadeiros com "Sem Rótulo Verdadeiro"
results['Matched Deck_true'].fillna('Sem Rótulo Verdadeiro', inplace=True)

# Calcular métricas apenas para os decks com rótulo verdadeiro
filtered_results = results[results['Matched Deck_true'] != 'Sem Rótulo Verdadeiro']
y_true = filtered_results['Matched Deck_true']
y_pred = filtered_results['Matched Deck_predicted']

if len(filtered_results) > 0:
    accuracy = accuracy_score(y_true, y_pred)
    classification_report_str = classification_report(y_true, y_pred)
else:
    accuracy = 0.0
    classification_report_str = "Não há dados suficientes para calcular as métricas."

# Exibir os resultados
print("Métricas de Desempenho do Agente Baseado em Regras:")
print(f"Acurácia: {accuracy:.4f}")
print("\nRelatório de Classificação:")
print(classification_report_str)

# Salvar os resultados em um novo arquivo CSV
output_file = 'data/matching_results.csv'
results.to_csv(output_file, index=False)
