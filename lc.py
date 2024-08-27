from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Instantiate the webdriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# The base URL for the pages to scrape
page_URL = "https://pubmed.ncbi.nlm.nih.gov/?term=machine%20learning&page="

# Function to get all the 'a' tags with class 'docsum-title' from a given URL
def get_a_tags(url):
    # Load the URL in the browser
    driver.get(url)
    # Wait for the page to fully load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "docsum-title"))
    )
    # Find all 'a' elements with the class 'docsum-title'
    links = driver.find_elements(By.CLASS_NAME, "docsum-title")
    ans = []
    # Iterate over each 'a' element
    for link in links:
        href = link.get_attribute("href")
        if href:
            ans.append(href)
    # Remove duplicate links using set
    ans = list(set(ans))
    return ans

# List to store the final list of links
my_ans = []
# Loop through the pages you're interested in (in this case, pages 1-10)
for i in range(1, 504):
    # Call the function to get the 'a' tags from each page and append the results to your list
    my_ans += get_a_tags(page_URL + str(i))

# Remove any duplicates that might have been introduced in the process
my_ans = list(set(my_ans))

# Open a file to write the results to
with open('b.txt', 'a') as f:
    # Iterate over each link in your final list
    for j in my_ans:
        # Write each link to the file, followed by a newline
        f.write(j + '\n')

# Print the total number of unique links found
print(len(my_ans))

# Close the browser
driver.quit()
