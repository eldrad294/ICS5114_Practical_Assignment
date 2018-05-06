import json
from selenium import webdriver

def run_scraper():
    browser = webdriver.Firefox()
    url = "https://www.youtube.com/watch?v=6ValJMOpt7s&t=14317s"
    browser.get(url)
    browser.implicitly_wait(10)
    chats = []
    for chat in browser.find_elements_by_css_selector("span[class='yt-live-chat-text-message-renderer']"):
    #for chat in browser.find_element_by_xpath('//span[@class="yt-live-chat-text-message-renderer"]'):
        author_name = chat.find_element_by_css_selector("#author-name").get_attribute('innerHTML')
        message = chat.find_element_by_css_selector("#message").get_attribute('innerHTML')
        #author_name_encoded = author_name.encode('utf-8').strip()
        #message_encoded = message.encode('utf-8').strip()
        obj = json.dumps({'author_name': author_name, 'message': message})
        chats.append(json.loads(obj))
        print('Entry')

    browser.quit()
    return chats
#
chats = run_scraper()
for chat in chats:
    print(chat)