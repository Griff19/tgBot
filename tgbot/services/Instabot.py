
from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from tgbot.services.DB import DB


def click_button_by_text(browser, text: str):
    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.text.find(text) > -1:
            button.click()
            break

parent_user = 'ivan_gredasov'
options = Options()
options.add_argument("user-data-dir=C:/Users/griff/selenium")
browser = webdriver.Chrome(options=options)
browser.get('https://www.instagram.com')

sleep(4)
try:
    username_input = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = browser.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys("ivan_gredasov")
    password_input.send_keys("W@E#i8h6")
    sleep(1)
    login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
except NoSuchElementException:
    click_button_by_text(browser, "Продолжить как")

# input("Ждем...")
# click_button_by_text(browser, "Не сейчас")
# sleep(5)
# click_button_by_text(browser, "Не сейчас")

sleep(4)
browser.get(f'https://www.instagram.com/{parent_user}/followers')

sleep(4)
dialog = browser.find_element(By.CSS_SELECTOR, "div[role='dialog']")
elements = dialog.find_elements(By.CSS_SELECTOR, "div[aria-labelledby]")
current = dialog.find_element(By.CSS_SELECTOR, "button[type='button']")

link_followers = browser.find_element(By.CSS_SELECTOR, "a[href*='/followers']")
total_followers = int(link_followers.text.split(" ")[0])
print(total_followers)

db = DB("D:/WORK/python/Telegram/TestBot/base.db")
followers = []
nn = 0
while len(followers) < total_followers:
    current.send_keys(Keys.TAB)
    current = browser.switch_to.active_element
    current.send_keys(Keys.TAB)
    current = browser.switch_to.active_element
    current.send_keys(Keys.TAB)
    current = browser.switch_to.active_element
    sleep(1)

    elements = dialog.find_elements(By.CSS_SELECTOR, "div[aria-labelledby]:nth-last-child(-n+20)")
    for element in elements:
        a = element.find_element(By.CSS_SELECTOR, "a[href]")
        link = a.get_attribute('href')
        name = link.replace('https://www.instagram.com/', '@')
        name = name.replace('/', '')
        if [name, link] in followers:
            if followers.index([name, link], 0, 5) :
                break
            continue
        followers.append([name, link])
        db.cursor.execute('INSERT INTO account (parent, alias, link, status) VALUES (?, ?, ?, ?);', (f'@{parent_user}', name, link, 'new'))

        nn += 1
        print(nn, name, link)

print("Запись а базу данных", nn, "элементов...")
db.connection.commit()
print("Обработка завершена.")
db.connection.close()
browser.close()
