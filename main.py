import pandas as pd

from selenium import webdriver

web = 'https://www.audible.com/search'

driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

book_title = []
book_author = []
book_length = []

products = driver.find_elements('class name', 'productListItem')
for product in products:
    book_title.append(product.find_element('xpath', './/h3[contains(@class, "bc-heading")]').text)
    book_author.append(product.find_element('xpath', './/li[contains(@class, "authorLabel")]').text)
    book_length.append(product.find_element('xpath', './/li[contains(@class, "runtimeLabel")]').text)

driver.quit()

df = pd.DataFrame({
    'Title': book_title,
    'Author': book_author,
    'Length': book_length
})
df.to_csv('books.csv', index=False)
