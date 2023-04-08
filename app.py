import json
import time
import string
import random
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

with open('config.json', 'r') as conf:
	config = json.load(conf)

month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day = random.randint(1, 29)
year = random.randint(1989, 2004)

class App:
	def __init__(self):
		self.username = str(config['username']) + '_' + str(random.randint(10000, 99999))
		self.password = ''.join(random.choice(string.hexdigits) for i in range(8))

	def invoke(self):
		driver = webdriver.Chrome()
		driver.get('https://roblox.com/')

		driver.find_element(By.XPATH, '//*[@id="MonthDropdown"]').send_keys(random.choice(month))
		driver.find_element(By.XPATH, '//*[@id="DayDropdown"]').send_keys(day)
		driver.find_element(By.XPATH, '//*[@id="YearDropdown"]').send_keys(year)

		username = driver.find_element(By.XPATH, '//*[@id="signup-username"]')
		username.send_keys(self.username)

		password = driver.find_element(By.XPATH, '//*[@id="signup-password"]')
		password.send_keys(self.password)

		female = lambda: driver.find_element(By.XPATH, '//*[@id="FemaleButton"]/div').click()
		male = lambda: driver.find_element(By.XPATH, '//*[@id="MaleButton"]/div').click()

		if random.randint(0, 1) == 0: female()
		else: male()
		""" click signup button """
		driver.find_element(By.XPATH, '//*[@id="signup-button"]').click()

		while 'https://www.roblox.com/home?nu=true' != str(driver.current_url):
			time.sleep(1)

		if 'https://www.roblox.com/home?nu=true' == str(driver.current_url):
			print(f'( + ) > Account created successfully!')
			open('data/accounts.txt', 'a').write(f'{self.username}:{self.password}\n')

			if config['webhook_url'] != None:
				requests.post(config['webhook_url'], json={
					"embeds": [
					    {
					    	"description": f"`Username : {self.username}\nPassword : {self.password}`",
					      	"color": 39423,
					      	"author": {
					        	"name": "Roblox Account Creator"
					      	}
					    }
					],
				})
			else: pass
			driver.quit()

if __name__ == ('__main__'):
	amount = input('( ? ) Please enter the number of accounts to generate: ')
	for _ in range(int(amount)):
		App().invoke()
