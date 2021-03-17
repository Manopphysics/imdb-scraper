import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import psycopg2


conn = psycopg2.connect(dbname="postgres",user="postgres", password="postgres")
cur = conn.cursor()
sql = "INSERT INTO top_movies1000 (title, year, certificate, runtime, genre, imdb_rating, description, directors, stars) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
sql_desc = "UPDATE top_movies1000 SET description = %s"

chrome_driver = r"C:\Users\manop\Desktop\YEAR 4 TERM 2\Software VV\SVV files\chromedriver.exe"
url = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
urls = []
urls.append(url)

#generate url for all the imdb movie pages to 1000
for i in range(1,10):
    urls.append("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(i)+"01&ref_=adv_nxt")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=chrome_driver,options=options)


def main():
    for ui,url in enumerate(urls):
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for i,content in enumerate(soup.find_all("div",{"class": "lister-item-content"}),1):

            #get movie name
            movie_name = content.find(class_= "lister-item-header" ).find("a").get_text()
            #get movie year

            year = int(re.sub('[^0-9]+','', content.find(class_="lister-item-year").get_text()))

            #get movie certificate
            try:
                certificate = content.find("span","certificate").get_text() #[0].find(class_="certificate") #find_all("span",class_= "certificate" )
            except Exception:
                certificate = "Not Rated"

            #get movie run time
            runtime = int(content.find("span","runtime").get_text().strip().replace("min",""))

            #get movie genre
            genre = content.find("span","genre").get_text().strip()

            #get imdb rating
            imdb_rating = float(content.find("div","ratings-bar").find("strong").get_text().strip())

            #get movie description
            description = content.find_all("p","text-muted")[1].get_text()

            #get movie directors and stars
            people = content.find("p",class_="").text
            people = people.strip()
            directors,stars = people.split("|")[0].strip().replace("\n","").replace("Director:","").split(","), people.split("|")[1].strip().replace("\n","").replace("Stars:","").split(",")

            directors = str(directors).replace("[","").replace("]","")
            stars = str(stars).replace("[","").replace("]","")
            print(i+(ui*100),movie_name)
            #print(i+(ui*100),movie_name, year, "|", certificate, "|", runtime, "|", genre, "|", imdb_rating, "|", description, "|", directors, "|", stars)
            #print(type(description),description)
            #print(description)
            #cur.execute(sql_desc,(description,))
            cur.execute(sql,(movie_name, year, certificate, runtime, genre, imdb_rating, description, directors, stars))
            conn.commit()

            #SELECT * FROM top_movies1000 WHERE imdb_rating>8 AND year>1990 AND certificate !='R' AND genre LIKE '%Comedy%' ORDER BY imdb_rating asc


    


if __name__ == '__main__':
    main()
