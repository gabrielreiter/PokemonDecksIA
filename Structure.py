import pandas as pd
import re

# Carregar o arquivo CSV corrigido
file_path = 'output/decks.csv'  # Substitua pelo caminho do arquivo corrigido
raw_data = pd.read_csv(file_path, header=None)

# Estruturar os dados
structured_data = {
    'ID': [],
    'Rank': [],
    'Category': [],
    'Copies': [],
    'Card Name': [],
    'Set': []
}

id = 0 # Inicializa o ID
current_rank = 0  # Inicializa o rank
current_category = None  # Inicializa a categoria como None
new_deck = True  # Flag para identificar quando um novo deck começa

# Expressão regular para separar as partes do texto (carta, cópias, coleção)
card_pattern = re.compile(r'(\d+)\s(.+)\s([A-Z0-9]+\s\d+)')

# Iterar pelas linhas do arquivo CSV
for line in raw_data[0]:
    line = line.strip()  # Remover espaços extras
    
    # Identificar as categorias e quando uma nova seção começa
    if "Pokémon:" in line:  # Identificar a seção Pokémon
        current_category = "Pokémon"
        if (current_rank >= 16):
            current_rank = 1
        else:
            current_rank += 1
        id += 1
    elif "Trainer:" in line:  # Identificar a seção Trainer
        current_category = "Trainer"
    elif "Energy:" in line:  # Identificar a seção Energy
        current_category = "Energy"
    
    # Quando encontramos a primeira linha de um novo deck, incrementamos o rank
    if line == '' and not new_deck:  # Se a linha está vazia e o deck já foi processado
        new_deck = True  # Define que o próximo deck vai começar
    
    # Processar as cartas do deck
    elif line and current_category:  # Quando encontrar uma carta e a categoria estiver definida
        match = card_pattern.match(line)
        if match:
            copies, card_name, set_name = match.groups()
            copies = int(copies)
            if new_deck:  # Apenas incrementa o rank na primeira carta do deck
                new_deck = False  # Após processar a primeira carta, não incrementa mais o rank
            # Adiciona o rank para todas as cartas dentro do mesmo deck
            structured_data['ID'].append(id)
            structured_data['Rank'].append(current_rank)
            structured_data['Category'].append(current_category)
            structured_data['Copies'].append(copies)
            structured_data['Card Name'].append(card_name.strip())
            structured_data['Set'].append(set_name.strip())

# Verificar se todas as listas têm o mesmo comprimento
list_lengths = [len(structured_data[key]) for key in structured_data]
if len(set(list_lengths)) != 1:
    print("Erro: As listas não têm o mesmo comprimento.")
    print(f"Tamanhos das listas: {list_lengths}")
else:
    # Criar DataFrame estruturado
    deck_data = pd.DataFrame(structured_data)

    # Salvar o DataFrame estruturado em um novo arquivo CSV
    output_path = 'output/structured_decks.csv'  # Nome do arquivo de saída
    deck_data.to_csv(output_path, index=False)

    print(f"Arquivo estruturado salvo em: {output_path}")