from selenium import webdriver
import pandas as pd
import csv
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from functions import bet_ratio, odds_arbitrage
from datetime import datetime


path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)
df = pd.DataFrame()

# Defining variables to check against so that scanner scans until betting suspended for at least one of the sites
check1 = 'Open'
check2 = 'Open'

while (check1 == 'Open') and (check2 == 'Open'):
    # Getting Sportsbet live odds
    driver.get('https://www.sportsbet.com.au/betting/basketball-us/nba/milwaukee-bucks-at-phoenix-suns-5953593')

    try:
        data = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                      By.XPATH, '//*[@id="base"]/div/div[2]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div[2]/div/ul/li/div/div/div')))
    except:
        check1 = 'Bad'

    # Creating data vector for sportsbet live odds
    dataSportsbet = ['Sportsbet']
    i = 0
    while i <= 3:
        bracket = []
        bracket.append(str(data.text.split()[0 + i]) + ' ' + str(data.text.split()[1 + i])) # Appending team 1/2
        bracket.append(str(data.text.split()[2 + i])) # Appending oddswin team 1/2
        dataSportsbet.append(bracket)
        i += 3

    print(dataSportsbet)


    # Getting Pointsbet live odds
    driver.get('https://pointsbet.com.au/sports/basketball/NBA')

    try:
        data = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                      By.XPATH, '//*[@id="mainContent"]/div[1]/div/div/div[2]/div/div/div/div/div[2]')))
    except:
        check2 = 'Bad'

    # Creating data vector for pointsbet live odds
    dataPointsbet = []
    i = 0
    while i <= 3:
        bracket = []
        bracket.append(str(data.text.split()[0 + i]) + ' ' + str(data.text.split()[1 + i])) # Appending team 1/2
        bracket.append(str(data.text.split()[2 + i])) # Appending oddswin team 1/2
        dataPointsbet.append(bracket)
        i += 3

    # Reversing data vector for pointsbet if does not match up with data vector for sportsbet
    if dataSportsbet[0][0] != dataPointsbet[0][0]:
        dataPointsbet.reverse()
    dataPointsbet.insert(0, 'Pointsbet')

    print(dataPointsbet)

    # Checking if arbitrage bet possible
    print(odds_arbitrage(dataSportsbet, dataPointsbet))
    print('')

    # Putting data into dataframe
    dict = {'time':'', 'team 1':'', 'team 2':'', 'Sportsbet odds team 1 win':'', 'Sportsbet odds team 2 win':'', 'Pointsbet odds team 1 win':'', 'Pointsbet odds team 2 win':'', 'Action':''}
    now = datetime.now()
    dict['time'] = current_time = now.strftime("%H:%M:%S")
    dict['team 1'] = dataSportsbet[1][0]
    dict['team 2'] = dataSportsbet[2][0]
    dict['Sportsbet odds team 1 win'] = dataSportsbet[1][1]
    dict['Sportsbet odds team 2 win'] = dataSportsbet[2][1]
    dict['Pointsbet odds team 1 win'] = dataPointsbet[1][1]
    dict['Pointsbet odds team 2 win'] = dataPointsbet[2][1]
    dict['Action'] = odds_arbitrage(dataSportsbet, dataPointsbet)
    df = df.append(dict, ignore_index=True)

driver.quit()

# Creating CSV file for dataframe of odds
path = r'C:\Users\61437\Desktop'
os.chdir(path)
df.to_csv('Live games odds data.csv', index=False)
