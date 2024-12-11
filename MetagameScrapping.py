from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip

# set up the PATHs
URL_WEBSITE = 'https://limitlesstcg.com/decks?time=2425&type=all&format=all&region=all&division=all&page=1'
# I need to use selenium to scrape the data from the website below
# https://limitlesstcg.com/tournaments?time=12months&type=all&format=standard&region=all&show=100
# And extract the decklists from the top 8 players of each tournament and save them in a csv file
# The csv file should have the following columns:
# Tournament Name, Date, Player Name, Deck Name, Card1, Card2, ..., Card60
# The csv file should have a row for each decklist
# begin now


# Initialize the WebDriver (in this case, for Chrome)
driver = webdriver.Chrome()

# Go to the limitlesstcg website
driver.get(URL_WEBSITE)

# Get all the urls for the tournaments

# all elements have a tag <a> and the href="/tournament/xxxxx" where xxxxx is the tournament id
# I can use the xpath to find all the elements with the tag <a> and then extract the href attribute
# wait for the page to load

decks = []

time.sleep(1)
deckElements = driver.find_elements(By.XPATH, '/html/body/main/div/table/tbody//td[3]')
for element in deckElements:
    decks.append(element.accessible_name)

i = 0
with open(f'output/metagame.csv', 'w') as f:
    # write the header
    f.write('decks:\n')
error_counter = 0

for deck in decks:
    with open(f'output/metagame.csv', 'a', encoding='utf-8') as f:
        f.write(f'\n{deck}\n')
