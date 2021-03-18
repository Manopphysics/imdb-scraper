from bs4 import BeautifulSoup
from selenium import webdriver
from scraper import Scraper
from imdbpg import MovieDatabase

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
        #establish connection with the imdb page and get page source
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #Initialize the databse
        db = MovieDatabase("postgres", "postgres", "postgres")

        #Initialize the scraper
        imdb_scraper = Scraper()



        for i,content in enumerate(soup.find_all("div",{"class": "lister-item-content"}),1):

            #get movie name
            movie_name = imdb_scraper.get_movie_name(content)
            #get movie year

            year = imdb_scraper.get_movie_year(content)

            #get movie certificate
            certificate = imdb_scraper.get_movie_certificate(content)

            #get movie run time
            runtime = imdb_scraper.get_movie_runtime(content)

            #get movie genre
            genre = imdb_scraper.get_movie_genre(content)

            #get imdb rating
            imdb_rating = imdb_scraper.get_imdb_rating(content)

            #get movie description
            description = imdb_scraper.get_movie_description(content)

            #get movie directors and stars
            directors, stars = imdb_scraper.get_movie_directors_and_stars(content)

            print(i+(ui*100),movie_name)
            
            db.insert_movie(movie_name, year, certificate, runtime, genre, imdb_rating, description, directors, stars)

    


if __name__ == '__main__':
    main()
