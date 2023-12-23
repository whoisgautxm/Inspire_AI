# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# from bs4 import BeautifulSoup
# import csv

# class WiredSearch(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     def test_search_in_wired(self):
#         driver = self.driver
#         driver.get("https://www.nytimes.com/")
#         print("Title:", driver.title)  # Debugging line
#         self.assertIn("The New York Times", driver.title)  # Adjusted assertion for NYT website
#         search_icon = driver.find_element(By.CLASS_NAME, "css-10488qs")  # Updated to find the search icon by class name
#         search_icon.click()
#         search_input = driver.find_element(By.NAME, "query")  # Updated to find the search input by name
#         search_input.send_keys("USA")  # Replace 'your_search_keywords' with actual keywords
#         search_input.submit()

#         # Wait for the page to load
#         driver.implicitly_wait(5)  # Adjust the waiting time as needed

#         articles_data = []  # List to store article data

#         max_articles = input('no of artclies:' )  # Define the maximum number of articles to process
#         i = 0
#         while i < int(max_articles):
#             search_results = driver.find_elements(By.TAG_NAME, 'h4')  # Find all 'h4' elements
#             if i >= len(search_results):
#                 break  # Break the loop if the index exceeds available elements

#             article = search_results[i]
#             article.click()
#             time.sleep(2)  # Wait for the page to load

#             # Use Beautiful Soup to parse the page source obtained by Selenium
#             soup = BeautifulSoup(driver.page_source, 'html.parser')

#             article_title = soup.find('h1').text.strip() if soup.find('h1') else "N/A"
#             paragraphs = [p.text.strip() for p in soup.find_all('p', class_='css-at9mc1 evys1bk0')] if soup.find_all('p', class_='css-at9mc1 evys1bk0') else ["N/A"]
#             print('Number of paragraphs:', len(paragraphs))
            
#             description = soup.find(id='article-summary')
#             description_text = description.text.strip() if description else "N/A"

#             # Append article data to the list
#             articles_data.append({'Title': article_title, 'Content': '\n'.join(paragraphs), 'Description': (description_text)})

#             driver.execute_script("window.history.go(-1)")  # Navigate back to search results
#             time.sleep(3)  # Wait for the page to load again before proceeding
#             i += 1
#         # ...
#         # Write data to a CSV file
#         with open('article_data.csv', mode='w', newline='', encoding='utf-8') as file:
#             fieldnames = ['Title', 'Content', 'Description']
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(articles_data)

#     def tearDown(self):
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv

class WiredSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_wired(self):
        driver = self.driver
        driver.get("https://www.nytimes.com/")
        print("Title:", driver.title)  # Debugging line
        self.assertIn("The New York Times", driver.title)  # Adjusted assertion for NYT website
        search_icon = driver.find_element(By.CLASS_NAME, "css-10488qs")  # Updated to find the search icon by class name
        search_icon.click()
        search_input = driver.find_element(By.NAME, "query")  # Updated to find the search input by name
        search_input.send_keys("USA")  # Replace 'your_search_keywords' with actual keywords
        search_input.submit()

        # Wait for the page to load
        driver.implicitly_wait(5)  # Adjust the waiting time as needed

        articles_data = []  # List to store article data

        max_articles = input('no of articles: ')  # Define the maximum number of articles to process
        i = 0
        while i < int(max_articles):
            search_results = driver.find_elements(By.TAG_NAME, 'h4')  # Find all 'h4' elements
            if i >= len(search_results):
                break  # Break the loop if the index exceeds available elements

            article = search_results[i]
            article.click()
            time.sleep(10)  # Wait for the page to load

            # Scroll down to load more content if needed

            # Use Beautiful Soup to parse the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract article title from the main page
            article_title = soup.find('h1').text.strip() if soup.find('h1') else "N/A"

            # Extract content from the div with a specific class
            content_div = soup.find('div', class_='css-53u6y8')
            content_text = content_div.text.strip() if content_div else "N/A"

            author = soup.find('p', class_='css-4anu6l e1jsehar1').text.strip() if soup.find('p', class_='css-4anu6l e1jsehar1') else "N/A"

            # Extract description if available
            description_element = soup.find('p', id='article-summary')
            description = description_element.text.strip() if description_element else "N/A"

            # Append article data to the list
            articles_data.append({'Title': article_title, 'Description': description, 'Content': content_text , 'Author': author})

            driver.execute_script("window.history.go(-1)")  # Navigate back to search results
            time.sleep(3)  # Wait for the page to load again before proceeding
            i += 1

        # Write data to a CSV file
        with open('article_data.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Title', 'Description', 'Content' , 'Author']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(articles_data)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
