import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

web = 'https://www.audible.com/charts/best'

options = Options()
# options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome()
driver.get(web)

pagination = driver.find_element('class name', 'pagingElements')
pages = pagination.find_elements('tag name', 'li')
last_page = int(pages[-2].text)

book_title = []
book_author = []
book_length = []

current_page = 1
while current_page <= last_page:
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'productListItem'))
    )

    for product in products:
        book_title.append(product.find_element('xpath', './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element('xpath', './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element('xpath', './/li[contains(@class, "runtimeLabel")]').text)

    try:
        next_page_button = driver.find_element('xpath', '//span[contains(@class, "nextButton")]')
        next_page_button.click()
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        break

    current_page += 1

driver.quit()

df = pd.DataFrame({
    'Title': book_title,
    'Author': book_author,
    'Length': book_length
})
df.to_csv('books.csv', index=False)
