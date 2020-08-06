import requests
import pandas as pd
import time
import random

from bs4 import BeautifulSoup
from pathlib import Path

listLogin = []
listName = []
listVerification = []
listRating = []
listCountry = []
listWebsite = []
listWorks = []
listProducts = []
listSignals = []
listFacebook = []
listLinkedin = []
listTwitter = []
listVk = []
listSkype = []
listTg = []
listInsta =[]
listYoutube = []
listOther = []
proxyDic = []


def ss(url):
    listLogin.clear()
    listName.clear()
    listVerification.clear()
    listRating.clear()
    listCountry.clear()
    listWebsite.clear()
    listWorks.clear()
    listProducts.clear()
    listSignals.clear()
    listFacebook.clear()
    listLinkedin.clear()
    listTwitter.clear()
    listVk.clear()
    listSkype.clear()
    listTg.clear()
    listInsta.clear()
    listYoutube.clear()
    listOther.clear()

    try:
        #page = requests.get("https://www.mql5.com/ru/users/" + url , proxies={'https': proxy.strip()})
        page = requests.get("https://www.mql5.com/en/users/" + url)
        listLogin.append(url)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, 'html')
    except:
        print("400")
    try:
        Name = soup.find("h1", {"class": "profileHeaderTitle"}).text
        if Name == 'None':
            listName.append("None")
        else:
            listName.append(Name)

        WebSite = soup.find('table', class_="profileMainDetails").next.next
        children = WebSite.findChildren('a')
        for child in children:
            if "maps.google" in child.get('href'):
                listWebsite.append("None")
            else:
                web = child
                web = str(web)
                web = web.split('>')
                web = web[1].split("</a")
                listWebsite.append(web[0])

        Verified = soup.find("span", {"class": "icoVerified"})
        Verified = str(Verified)
        if Verified == 'None':
            Verified = "No"
        else:
            Verified = "Yes"
        listVerification.append(Verified)

        Rating = soup.find_all("a", rel="nofollow")
        for line in Rating:
            line = str(line.text)
            if line.isdigit():
                line = line
                listRating.append(line)

        soupus = soup.find_all('a', target="_blank")
        Products = soup.find_all('div', class_='counterValue')
        for line in Products:
            struct = line.a['href']
            if "products" in struct:
                products = line.text
                listProducts.append(products)
            if "signals" in struct:
                signals = line.text
                listSignals.append(signals)
        if not listProducts:
            listProducts.append("None")
        if not listSignals:
            listSignals.append("None")

        try:
            Works = soup.find('td', class_="userinfo__table-block profile__main-details__works").text
            listWorks.append(Works)
        except:
            Works = "None"
            listWorks.append(Works)

        Twitter_all = ""
        Facebook_all = ""
        linkedIn_all = ""
        vkontakte_all = ""
        maps_all = ""

        for tagCountry in soupus:
            tagCountry = str(tagCountry)
            if "twitter" in tagCountry:
                Twitter = soup.find("a", {"class": "socialIco twitter"}).get('href')
                Twitter = Twitter.split("/go?link=")
                Twitter_all += Twitter[1] + " | "
            if "facebook" in tagCountry:
                Facebook = soup.find("a", {"class": "socialIco facebook"}).get('href')
                Facebook = Facebook.split("/go?link=")
                Facebook_all += Facebook[1] + " | "
            if "linkedIn" in tagCountry:
                linkedIn = soup.find("a", {"class": "socialIco linkedIn"}).get('href')
                linkedIn = linkedIn.split("/go?link=")
                linkedIn_all += linkedIn[1] + " | "
            if "vkontakte" in tagCountry:
                vkontakte = soup.find("a", {"class": "socialIco vkontakte"}).get('href')
                vkontakte = vkontakte.split("/go?link=")
                vkontakte_all += vkontakte[1] + " | "
            if "skype" in tagCountry:
                skype = soup.find("a", {"class": "socialIco skype"}).get('href')
                listSkype.append(skype)
            if "maps.google.com" in tagCountry:
                country = tagCountry
                country = country.split('">')
                country = country[1].split("</a>")
                maps_all += country[0] + " | "

        if Twitter_all:
            listTwitter.append(Twitter_all)
        else:
            listTwitter.append("None")

        if Facebook_all:
            listFacebook.append(Facebook_all)
        else:
            listFacebook.append("None")

        if linkedIn_all:
            listLinkedin.append(linkedIn_all)
        else:
            listLinkedin.append("None")

        if vkontakte_all:
            listVk.append(vkontakte_all)
        else:
            listVk.append("None")

        if not listSkype:
            listSkype.append("None")

        if maps_all:
            listCountry.append(maps_all)
        else:
            listCountry.append("None")


        all_other = ""
        tme_all = ""
        youtube_all = ""
        instagram_all = ""

        try:
            other = soup.find('div', class_="profileAboutMe")
            children = other.findChildren("a", recursive=False)
            for child in children:
                if 't.me' in child.get('title'):
                    tme = child.get('title')
                    tme_all += tme + " | "
                elif 'youtube' in child.get('href'):
                    youtube = child
                    youtube = str(youtube)
                    youtube = youtube.split('>')
                    youtube = youtube[1].split("</a")
                    youtube_all += youtube[0] + " | "
                elif 'instagram' in child.get('href'):
                    instagram = child
                    instagram = str(instagram)
                    instagram = instagram.split('>')
                    instagram = instagram[1].split("</a")
                    instagram_all += instagram[0] + " | "
                else:
                    other = child.get('title')
                    if "mql5" in other:
                        other = ""
                    else:
                        all_other += other + " | "

        except:
            other = other
        print("OK: " + url)
        if all_other:
            listOther.append(all_other)
        else:
            listOther.append("None")

        if tme_all:
            listTg.append(tme_all)
        else:
            listTg.append("None")

        if youtube_all:
            listYoutube.append(youtube_all)
        else:
            listYoutube.append("None")

        if instagram_all:
            listInsta.append(instagram_all)
        else:
            listInsta.append("None")

        if not listWebsite:
            listWebsite.append("None")

        data = dict(login=listLogin, name=listName, verification=listVerification, rating=listRating,
                    country=listCountry, website=listWebsite, works=listWorks, products=listProducts,
                    signals=listSignals, facebook=listFacebook, linkedin=listLinkedin, twitter=listTwitter, vk=listVk,
                    skype=listSkype, telegram=listTg, insta=listInsta, youtube=listYoutube, other=listOther)
        df = pd.DataFrame(data)
        home = str(Path.home())
        df.to_csv(home + r"\Desktop\output.csv", mode='a+', sep=';', index=False, encoding='utf-8')
    except:
        print("Can't find page OR you got blocked OR end of file")

    # data = [listLogin, listName, listVerification, listRating, listCountry,
    #             listWebsite, listWorks, listProducts, listSignals, listFacebook,
    #             listLinkedin, listTwitter, listVk, listSkype, listTg, listInsta,
    #             listYoutube, listOther]

    # path = "C:\\Users\\Skayloo\\Desktop\\output.csv"
    # with open(path, "a+", newline='') as csv_file:
    #     writer = csv.writer(csv_file, delimiter=',')
    #     for line in data:
    #         writer.writerow(line)
    # csv_file.close()


def main():
    home = str(Path.home())
    f = open(home+r"\Desktop\ss.txt")
    #
    # proxy = fp.readline().rstrip()
    # while proxy:
    #     proxyDic.append(proxy)
    #     proxy = fp.readline().rstrip()
    # fp.close()
    urls = []
    url = f.readline().rstrip()
    ss(url)

    '''
    k = 0
    while url:
        k = k + 1
        if k == len(proxyDic):
            k = 0
        urls.append(url)
        url = f.readline().rstrip()
        ss(url, proxyDic[k])
    '''
    cnt = 0
    while url:
        #if cnt == random.randint(30,40):
            #ime.sleep(random.randint(5,10))
            #cnt = 0
        urls.append(url)
        url = f.readline().rstrip()
        ss(url)
        time.sleep(random.randint(4, 4))
    f.close()
'''
    data = [listLogin,listName,listVerification,listRating,listCountry,listWebsite,listWorks,listProducts,listSignals,listFacebook,listLinkedin,listTwitter,listVk,listSkype,listTg,listInsta,listYoutube,listOther]
    path = "C:\\Users\\Skayloo\\Desktop\\output.csv"
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)
'''
if __name__ == "__main__":
    main()
