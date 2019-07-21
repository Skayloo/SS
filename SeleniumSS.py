import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

delay = 10
driver = webdriver.Firefox(executable_path=r'C:\Users\skayl\Desktop\geckodriver.exe')
driver.get("https://www.facebook.com/2915212041854560")
try:
    elem_comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div[2]/form/div/div[2]/div[1]/div/div[3]/span[1]/a')))[0].click()
    try:
        if len(elem_comments) == 0:
            elem_comments_second_chance = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Комментарии:")))[0].click()
        else:
            print("My methods are sick")
    except:
        print("Comments ok")
except IndexError:
    print("Can't display comments")
try:
    elem_show_actual = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Самые актуальные")))[0].click()
except:
    print("Can't find box with actual comments")
try:
    driver.execute_script("window.scrollTo(0, 300)")
    elem_show_all = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Все")))[0].click()
except:
    print("Can't find button all comments")
k = 0
flag1 = True
driver.execute_script("window.scrollTo(0, 500)")
while flag1:
    try:
        elem_show_more = driver.find_elements(By.PARTIAL_LINK_TEXT, "Показать")[0].click()
        time.sleep(3)
        element_bottom = driver.find_element_by_id("bottomContent")
        driver.execute_script("arguments[0].scrollIntoView();", element_bottom)
        time.sleep(2)
        try:
            elem_not_now = driver.find_elements_by_partial_link_text("Не сейчас")[0].click()
            time.sleep(1)
            element_bottom = driver.find_element_by_id("bottomContent")
            dragger = ActionChains(driver)
            dragger.move_to_element(element_bottom).perform()
            time.sleep(0.5)
        except:
            k += 1
            print(k)
    except:
        print("Can't find show more")
        flag1 = False


coms = []
id_coms = []
showing_class_comments = driver.find_elements_by_class_name("_3l3x")
for showing_com in showing_class_comments:
    coms.append(showing_com.text)
showing_class_id_comments = driver.find_elements_by_class_name("_6qw4")
for showing_id_com in showing_class_id_comments:
    id_coms.append(showing_id_com.text)


f = open('C:\\Users\\skayl\\Desktop\\Comments.txt', 'w', encoding='utf-8')
res = list(zip(id_coms,coms))
for index in res:
    f.write(str(index) + '\n')
f.close()
driver.close()