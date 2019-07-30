import time
import json
from multiprocessing import Pool

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

def ss(url):
    delay = 20
    firefox_profile = webdriver.FirefoxProfile()

    #firefox_profile.set_preference('permissions.default.image', 2)
    driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=r'C:\Users\skayl\Desktop\geckodriver.exe')
    driver.get("https://www.facebook.com/" + url)
    driver.execute_script("window.scrollTo(0, 200)")
    time.sleep(0.5)
    try:
        driver.execute_script("window.scrollTo(0, 700)")
        time.sleep(0.5)
        driver.find_element_by_partial_link_text("Комментарии:")[0].click()
        time.sleep(0.5)
    except:
        try:
            driver.execute_script("window.scrollTo(0, 700)")
            time.sleep(0.5)
            WebDriverWait(driver, delay).until(
                EC.presence_of_all_elements_located((By.XPATH,
                '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div[2]/form/div/div[2]/div[1]/div/div[3]/span[1]/a')))[
                0].click()
            time.sleep(0.5)
        except:
            try:
                driver.execute_script("window.scrollTo(0, 100)")
                time.sleep(0.5)
                WebDriverWait(driver, delay).until(
                EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Комментарии:")))[0].click()
                time.sleep(0.5)
            except:
                try:
                    driver.execute_script("window.scrollTo(0, 200)")
                    time.sleep(0.5)
                    WebDriverWait(driver, delay).until(
                        EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Комментарии:")))[0].click()
                    time.sleep(0.5)
                except:
                    print("FUCK OFF PLS WITH THIS SHITTY TASK")
    time.sleep(2)

    try:
        time.sleep(0.5)
        WebDriverWait(driver, delay).until(
            EC.presence_of_all_elements_located(
                (By.PARTIAL_LINK_TEXT, "Самые актуальные")))[0].click()
    except:
        try:
            element_actual = driver.find_element_by_partial_link_text("Самые актуальные")
            draggers1 = ActionChains(driver)
            draggers1.move_to_element(element_actual)
            time.sleep(0.5)
            draggers1.perform()
            element_actual.click()
        except:
            print("Can't find actual")

    try:
        driver.execute_script("window.scrollTo(0, 700)")
        time.sleep(0.5)
        WebDriverWait(driver, delay).until(
            EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Все комментарии")))[
            0].click()
    except:
        try:
            element_actual = driver.find_element_by_partial_link_text("Все комментарии")
            draggers2 = ActionChains(driver)
            draggers2.move_to_element(element_actual)
            time.sleep(0.5)
            draggers2.perform()
            WebDriverWait(driver, delay).until(
                EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Все комментарии")))[
                0].click()
        except:
            print("Can't find all coms")

    k = 0
    flag1 = True
    while flag1:
        try:
            flag2 = True
            while flag2:
                try:
                    driver.find_elements(By.CLASS_NAME, "_4sxd")[0].click()
                    time.sleep(1)
                except:
                    flag2 = False
            WebDriverWait(driver, delay).until(
                EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Показать ещё")))[
                0].click()
            time.sleep(3)
            element_bottom = driver.find_element_by_id("bottomContent")
            driver.execute_script("arguments[0].scrollIntoView();", element_bottom)
            time.sleep(2)
            try:
                driver.find_elements_by_partial_link_text("Не сейчас")[0].click()
                time.sleep(1)
                element_bottom = driver.find_element_by_id("bottomContent")
                draggers3 = ActionChains(driver)
                draggers3.move_to_element(element_bottom).perform()
                time.sleep(0.5)
            except:
                k += 50
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

    res = list(zip(id_coms, coms))

    output = []
    with open('C:\\Users\\skayl\\Desktop\\Comments.txt', mode='r', encoding='utf-8') as f:
        try:
            output = json.load(f)
        except:
            pass
    with open('C:\\Users\\skayl\\Desktop\\Comments.txt', mode='w+', encoding='utf-8') as f:
        output.append({
            "Post": url,
            "Info": [str(x) for x in res]
        })
        json.dump(output, f)
    # f = open('C:\\Users\\admin\\Desktop\\ss.txt', 'a', encoding='utf-8')
    # f.write("Post: " + url)
    # for index in res:
    #    f.write(str(index) + '\n')
    # f.close()
    driver.close()

def chunks(list, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(list), n):
        yield list[i:i + n]

def main():
    f = open("C:\\Users\\skayl\\Desktop\\ss.txt")
    urls = []
    url = f.readline()
    while url:
        urls.append(url)
        url = f.readline()
    f.close()
    print(urls[0])
    p = Pool(5)
    chunk_size = 5
    for chunk in chunks(urls, chunk_size):
        p.map(ss, chunk)

if __name__ == "__main__":
    main()