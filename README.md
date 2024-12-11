# Agentes de matching entre listas de cartas(decks reais) e os decks mais jogados no metagame(nomes dos decks)
O intuito do projeto é a criação de um agente inteligente que consiga a partir de uma lista de cartas identificar
o nome do deck dentro de um contexto dos decks do metagame, ou seja, um modelo que classifique corretamente qual
o deck que aquela lista representa

# Coleta de dados
Os dados das listas foram coletados através do algoritmo DeckScrapping.py, onde os dados são buscados através do HTML
do site [limitlesstcg.com](https://limitlesstcg.com/).

Para o processamento(treino e teste) dos agentes foi realizado o 'scrapping' dos melhores 16 decks dos torneios da atual
temporada.

Devido algumas irregularidades do HTML do site(tags diferentes para mesmo objeto) e depedência do forçamento do clique de
botões para obtenção das listas houveram algumas divergências com o ranking real, mas que não influenciaram na aplicação desses
dados para os agentes.

Os dados dos decks do metagame também foram buscados do mesmo site através do MetagameScrapping.py

Esses dados estão nos arquivos output/decks e output/metagame.

# Estruturação dos dados
Após coleta das listas de decks, eles passaram por um processamento que estruturou um novo csv separando por cartas e criando
colunas que auxiliaram no processamento desses dados pelos agentes.

Essas estruturação foi feita no Structure.py e os dados estão em structured_decks.csv

# Agente baseado em regras
No agente presente em MatchingDeckByRules.py o matching é realizado baseado em regras, ou seja, o sistema toma decisões baseado
em regras definidas previamente.

Métricas de Desempenho do Agente Baseado em Regras:
Acurácia: 0.8154

Relatório de Classificação:
                         precision    recall  f1-score   support

            Ancient Box       0.00      0.00      0.00         2
             Banette ex       0.00      0.00      0.00         1
           Charizard ex       0.00      0.00      0.00         2
   Chien-Pao Baxcalibur       1.00      1.00      1.00         1
 Cornerstone Ogerpon ex       0.33      1.00      0.50         2
           Dragapult ex       1.00      1.00      1.00         2
           Gardevoir ex       0.67      1.00      0.80         2
           Gholdengo ex       1.00      0.50      0.67         2
        Gouging Fire ex       1.00      1.00      1.00         1
         Iron Thorns ex       0.95      1.00      0.97        18
Klawf Unhinged Scissors       1.00      1.00      1.00         2
          Lost Zone Box       0.00      0.00      0.00         2
         Lugia Archeops       0.00      0.00      0.00         2
            Miraidon ex       1.00      1.00      1.00         2
           Palkia VSTAR       0.00      0.00      0.00         0
        Pidgeot Control       0.00      0.00      0.00         1
         Raging Bolt ex       1.00      1.00      1.00         5
        Regidrago VSTAR       1.00      1.00      1.00        10
        Roaring Moon ex       0.40      1.00      0.57         2
      Snorlax Stall PGO       0.00      0.00      0.00         1
           Terapagos ex       1.00      1.00      1.00         5

               accuracy                           0.82        65
              macro avg       0.54      0.60      0.55        65
           weighted avg       0.77      0.82      0.78        65

Como pode ser observado no arquivo matching_results.csv, o agente baseado em regras preve muitos corretamente, principalmente as listas
que são mais padronizadas(decks que não possuem muitas cartas divergentes do padrão definido em labeled_decks.csv), mas ele tem dificuldade
de prever decks que são mais abertos, além de alguns ele não conseguir identificar e não realizar o matching(Sem Rótulo Verdadeiro).

# Agente criado utilizando regressão
A Regressão Logística, apesar do nome, é um algoritmo de classificação, não de regressão. Ele é usado para prever classes categóricas 
(neste caso, o deck correspondente).

Acurácia média após 1 iterações: 0.7500

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.8333
Recall Média: 0.7778
F1-Score Média: 0.6296

-------------------------------------------------------------

Acurácia média após 10 iterações: 0.6625

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.7447
Recall Média: 0.7553
F1-Score Média: 0.5426

-------------------------------------------------------------

Acurácia média após 50 iterações: 0.6275

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.7571
Recall Média: 0.7478
F1-Score Média: 0.5368

------------------------------------------------------------

Acurácia média após 500 iterações: 0.6172

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.7586
Recall Média: 0.7320
F1-Score Média: 0.5260

------------------------------------------------------------

Como observado, aumentando o número de iterações e a quantidade de treino, diminuiu a acurácia.
Utilizando uma iteração se obteve um resultado mais satisfatório com esse agente.

------------------------------------------------------------

Acurácia média após 1 iterações: 1.0000

Média do Classification Report (precision, recall, f1-score):
Precision Média: 1.0000
Recall Média: 1.0000
F1-Score Média: 1.0000

------------------------------------------------------------

# Agente criado utilizando Random Forest

------------------------------------------------------------

Início do modelo:

Acurácia média após 5 iterações: 0

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0
Recall Média: 0
F1-Score Média: 0

------------------------------------------------------------

No início do modelo estava utilizando apenas uma definição por deck no arquivo labeled_decks.csv, o que causava um resultado muito pobre.
Houveram alguns acertos práticos, mas não foram emitidos dados suficientes para serem observados.

Após aumentar a definição dos decks no arquivo labeled_decks.csv foram obtidos os seguintes resultados:

------------------------------------------------------------

Acurácia média após 1 iterações: 0.7500

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.8889
Recall Média: 0.7778
F1-Score Média: 0.6667

------------------------------------------------------------

Acurácia média após 5 iterações: 0.5750

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.6961
Recall Média: 0.7255
F1-Score Média: 0.4444

------------------------------------------------------------

Acurácia média após 100 iterações: 0.6138

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.7475
Recall Média: 0.7370
F1-Score Média: 0.5148

------------------------------------------------------------

Acurácia média após 500 iterações: 0.6048

Média do Classification Report (precision, recall, f1-score):
Precision Média: 0.7465
Recall Média: 0.7295
F1-Score Média: 0.5046

------------------------------------------------------------

Assim como no agente por regressão, o aumento do número de vezes que é realizado o treino
diminuiu a eficácia do algoritmo.

Os melhores desempenhos para 39 linhas de dados no labeled_decks.csv foram os algoritmos de regressão e random forest utilizando apenas uma iteração

Para ambos foi utilizado 80% de treino e 10% de teste.

Após isso, dobrei os dados do labeled_decks e realizei novo teste com o random forest:

------------------------------------------------------------

Acurácia média após 1 iterações: 1.0000

Média do Classification Report (precision, recall, f1-score):
Precision Média: 1.0000
Recall Média: 1.0000
F1-Score Média: 1.0000

[[2 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 1 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 2 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 2 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 1]]

------------------------------------------------------------

Com mais dados o resultado foi bem mais satisfatório, onde o agente previu corretamente quase 100% dos decks.

Os que não foram previstos corretamente foi por haverem divergências mínimas na listas que resultam na variação do nome do deck na prática.

# Dificuldades durante o desenvolvimento

As maiores dificuldades durante o desenvolvimento foi a realização do scrapping dos dados.

Desde o início eu quis criar um csv próprio com um algoritmo próprio de obtenção e estruturação, para que dessa forma
possa ser alterado e manipulado no futuro conforme desejado.

Outra dificuldade foi corrigir os agentes inteligentes e a base de dados de aprendizado para melhores resultados de aprendizagem.

# Possíveis melhorias

Aumento dos dados para treinamento do agente

Implementação de um agente para recomendar decks baseado no rank que eles obtiveram nos torneios ao redor do mundo.