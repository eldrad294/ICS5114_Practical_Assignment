from selenium import webdriver
from bs4 import BeautifulSoup
import time
#
def scrollDown(pause, driver):
    """
    Function to scroll down till end of page.
    """
    iterations, iteration = 10, 1
    while True:
        driver.execute_script("window.scrollTo(1, 500);")
        time.sleep(pause)
        iteration += 1
        if iteration > iterations:
            return driver

# Main Code
driver = webdriver.Firefox()

# Instantiate browser and navigate to page

driver.get('https://www.youtube.com/watch?v=iFPMz36std4')
driver = scrollDown(3, driver)

# Page soup
soup = BeautifulSoup(driver.page_source, "html.parser")

driver.close()

comments = soup.findAll(attrs={'id':'comment','class':"style-scope ytd-comment-thread-renderer"})
#print(comments)
i = 0
for comment in comments:
    print("".join(comment.text.split()) + "\n------------------")
    i += 1
print(i)