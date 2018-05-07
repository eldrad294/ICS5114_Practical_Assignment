from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get('https://www.youtube.com/watch?v=6ValJMOpt7s&t=14117s')
driver.execute_script('window.scrollTo(1,500);')

for i in range(10):
    driver.execute_script('window.scrollTo(1,3000);')
    time.sleep(5)

comment_div=driver.find_element_by_xpath('//*[@id="contents"]')
comments=comment_div.find_elements_by_xpath('//*[@id="content-text"]')
for comment in comments:
    print(comment.text)
