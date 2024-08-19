#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from IPython.display import display, HTML
from bs4 import BeautifulSoup
import mysql.connector


# In[2]:


username = 'root'
password = 'Rockypine@pple53'
host = 'localhost'
database = 'FF2023'


# In[3]:


connect = mysql.connector.connect(
    user = username, password = password, host = host, db = database
)
insert_statement = "INSERT INTO Fantasy23Top100 (Name, Position, total_Points, ppg) VALUES (%s, %s, %s, %s);"
cursor = connect.cursor()


# In[4]:


# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# URL of the webpage containing the table and getting it
url = 'https://www.thefantasyfootballers.com/2023-fantasy-football-stats/'
driver.get(url)


# In[5]:


soup = BeautifulSoup(driver.page_source, 'html.parser')
# Extracting rows from the body
tbody = soup.find('tbody')
rows = tbody.find_all('tr')


# In[6]:


# Extracting data from the rows
data = []
for row in rows[:100]:  #Gets the 100 highest fantasy scorers of 2023
    cells = row.find_all('td')
    player_name_div = cells[1].find('div', class_='player-name')
    player_name = player_name_div.find('a').text.strip() if player_name_div else 'N/A' #this is because it would normally say Josh AllenBUF instead of just Josh Allen
    position = cells[2].get_text(strip=True)
    total_points = cells[3].get_text(strip=True)
    points_per_game = cells[4].get_text(strip=True)
    row_data = [player_name, position, total_points, points_per_game]
    cursor.execute(insert_statement, row_data)
    data.append(row_data)


# In[7]:


# Close the WebDriver
driver.quit()

connect.commit()

# Close the connection
cursor.close()
connect.close()

