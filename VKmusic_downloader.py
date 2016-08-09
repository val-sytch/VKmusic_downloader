import json
import os
import requests
import time
from selenium import webdriver


user = "type your login here"
password = "type your password"


driver = webdriver.Firefox()

# Go to the link
# client_id - identificator of our application
# scope - access rights
driver.get("https://oauth.vk.com/authorize?"
           "client_id=4591034&scope=audio"
           "&redirect_uri=http://api.vk.com/blank.html"
           "&display=page&response_type=token")

# Finding the elements of the form and enter our data
user_input = driver.find_element_by_name("email")
user_input.send_keys(user)
password_input = driver.find_element_by_name("pass")
password_input.send_keys(password)

# click the button
submit = driver.find_element_by_id("install_allow")
submit.click()

# Receive data which required for processing API requests
current = driver.current_url
access_list = (current.split("#"))[1].split("&")
access_token = (access_list[0].split("="))[1] # acces_token
expires_in = (access_list[1].split("="))[1] # period of time while token is valid
user_id = (access_list[2].split("="))[1] # id our VK account
# close browser window
driver.close()

print ("Connecting")
# request to audio.get method API
url = "https://api.vkontakte.ru/method/" \
      "audio.get?uid=" + user_id +\
      "&access_token=" + access_token
# Create lists for store data
artists_list = []
titles_list = []
links_list = []

# counter for debug and step through the lists elements
number = 0
# Read the response from the server and store it in the variable
page = requests.get(url)
html = page.text
my_dict = json.loads(html) # Decoding JSON

for i in my_dict['response']:
    artists_list.append(i['artist'])
    titles_list.append(i['title'])
    links_list.append(i['url'])
    number += 1

path = "downloads"
if not os.path.exists(path):
    os.makedirs(path)

print ("Need to download: ", number)

# Downloading files

for i in range(0, number):
# The path where a specific audio recording will be stored / download 
    new_filename = path+"/"+artists_list[i] + " - " + titles_list[i] + ".mp3"
    print ("Downloading: ", new_filename, i)
# Check if this audio is currently in the folder
    if not os.path.exists(new_filename):
# Download file itself, cut off from all arguments from link and 
#set the path where to download
        with open(new_filename, "wb") as out:
            response = requests.get(links_list[i].split("?")[0])
            out.write(response.content)
            time.sleep(5)

print ("Download complete.")

