from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from facebook_scraper import get_posts
from multiprocessing import Pool, cpu_count
import pandas as pd
import time
from dotenv import load_dotenv, dotenv_values
import sys
from art import *

load_dotenv()
config = dotenv_values(".env")

def rechercheGoogle(localite1,localite2,nombrePage):
    # chargement de webdriver et du navigateur
    driver = webdriver.Firefox(executable_path=config["GECKO_DRIVER_PATH"])
    # aller sur facebook
    driver.get('http://www.google.com')
    # recherche le champs de saisi
    search_query = driver.find_element(By.NAME,'q')
    search_query.send_keys('site:facebook.com AND'+'"('+localite1+' "OR" '+localite2+') "AND "'+ "maison" +'"')
    search_query.send_keys(Keys.RETURN)
    test=True
    n=0
    lienGroup=[]
    time.sleep(5)
    while test:
        if n<nombrePage:
            try:
            ####### recuperer les liens des differents groupes
                facebook_urls = driver.find_elements(By.XPATH,"//*[@class='yuRUbf']/a")
                for url in facebook_urls:
                    if "facebook" in url.get_attribute("href"):
                        for id in range(len(url.get_attribute("href").split("/"))):
                            if url.get_attribute("href").split("/")[id]=="groups":
                                lienGroup.append(url.get_attribute("href").split("/")[id+1])
                                break    
                suivantpage = driver.find_element(By.ID,'pnnext')
                sleep(5)
                suivantpage.click()
                n=n+1
            except:
                    test=False
                    continue
        else:
                test=False
    return lienGroup

            
def postGroup(nbpage,idGroup):
    n=1
    ListPost=[]
    for post in get_posts(idGroup, cookies=config["COOKIES_FILE_PATH"], extra_info=True, pages=nbpage, options={"comments": False}):
        print("post "+str(n)+"✅")
        n=n+1
        ListPost.append(post)
    return ListPost


def multiprocessing(postGroup , list):
    with Pool(cpu_count()) as p:
        print("\nNombre de processeur disponible pour la parallelisation : ")
        print(cpu_count())
        rec=p.starmap( postGroup,list)    
        p.terminate()
        p.join()
        return rec

# Lanceur du script
nb_page_google = sys.argv[3]
nb_page_fb_group= sys.argv[4]

ListIdGroup=rechercheGoogle(sys.argv[1],sys.argv[2],int(nb_page_google))
items=[(int(nb_page_fb_group),x) for x in ListIdGroup]

if __name__ == '__main__':
    # PARTIE 1 : recuperation des donnees
    tprint("EXTRACTOR")
    print("Processus de recuperation des donnees en cours veuillez patienter ...\n")
    print("\nNombre de page a traiter : "+str(nb_page_google))
    print("\nNombre de groupes a traiter : "+str(len(ListIdGroup)))

    start_time = time.time()

    list = items
    ListeDictionnaire=multiprocessing(postGroup , list)

    df = pd.concat([pd.DataFrame(lst) for lst in ListeDictionnaire])
    df.to_csv("data/output.csv")

    # sauvegarder que la colonne post_text
    df.to_csv("data/data.csv", columns=['post_text'])

    end_time = time.time() - start_time
    print("\nTemps total de compilation :"+str(end_time))