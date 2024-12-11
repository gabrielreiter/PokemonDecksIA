from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip

# set up the PATHs
URL_WEBSITE = 'https://limitlesstcg.com/tournaments?time=2425&type=all&format=standard&region=all&show=100'
URL_WEBSITE_TEST = 'https://limitlesstcg.com/tournaments?time=1months&type=all&format=standard&region=all&show=100'
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

urls = []

time.sleep(0.01)
elements = driver.find_elements(By.XPATH, '/html/body/main/div/table/tbody//td[3]/a')
for element in elements:
    urls.append(element.get_attribute('href'))

tournaments = []
positions = []
deck_urls = []
players = []

for url in urls:
    time.sleep(0.01)
    driver.get(url)

    # get the link for the decks of the top 16 players

    listElements = driver.find_elements(By.XPATH, '/html/body/main/div/table/tbody//td[5]/a')
    playersElements = driver.find_elements(By.XPATH, '/html/body/main/div/table/tbody//tr')

    i = 0
    for element in listElements:
        deck_url = element.get_attribute('href')
        if len(element.get_attribute('href').split('?')) == 2:
            deck_url = (element.get_attribute('href').split('?')[0] + element.get_attribute('href').split('?')[1])
        deck_urls.append(deck_url)
        player = playersElements[i+1].text
        players.append(player)
        # add tournament multiple times just to print int the end
        i += 1
        if i == 16:
            break

def get_clean_decklist(data):
    # Split the decklist into Pokemon, Trainer and Energy. Then remove Energy.
    card_list = data.split('\n\n')[:2]
    # Remove the first element of each list and separates the cards.
    card_list = [x.split('\n')[1:] for x in card_list]
    # join the both lists (append one into other)
    card_list = card_list[0] + card_list[1]
    # split each element by the ' '
    card_list = [x.split(' ') for x in card_list]
    # get the last two elements of each list
    card_list = [x[-2:] for x in card_list]
    # if the second element has just 2 characters, put a 0 in front of it
    card_list = [[x[0], '0' + x[1]] if len(x[1]) == 2 else x for x in card_list]
    # join the elements of each list (append one into other)
    card_list = [x[0] + x[1] for x in card_list]
    
    return card_list

i = 0
with open(f'output/decks.csv', 'w') as f:
    # write the header
    f.write('decks:\n')
error_counter = 0
for deck_url in deck_urls:
    driver.get(deck_url)
    time.sleep(1)
    try:
    # get the button by class='export'
        button = driver.find_element(By.CLASS_NAME, 'export')
        button.click()
    except:
        error_counter += 1
        continue
    copied_text = pyperclip.paste()
    # save the text in a file
    with open(f'output/decks.csv', 'a', encoding='utf-8') as f:
        playerPrint = players[i] 
        f.write(f'\n{copied_text}\n')
    i += 1
print(f'Error: {error_counter}')
