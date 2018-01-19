from selenium import webdriver
from time import sleep


resList = []
driver_path = "/usr/local/bin/chromedriver" 
web = webdriver.Chrome(driver_path)
web.get('https://elwingsite.wordpress.com/')
sleep(1)

for  i in range(5):
    web.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(1)

contentList = web.find_elements_by_class_name(("post-title"))
for i in range(len(contentList)):
    web.find_elements_by_class_name(("post-title"))[i].click()
    sleep(1)
    contentText = web.find_element_by_class_name("post-content").text
    resList.append(contentText)
    print(contentText)
    web.back()
    for i in range(5):
        web.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(1)

print(resList)
web.quit()
