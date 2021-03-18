import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

class Scraper(object):
    def __init__(self):
        pass
    def get_movie_name(self, content) -> str:
        """Extract movie name from the imdb top 100 movie page source"""

        movie_name = content.find(class_= "lister-item-header" ).find("a").get_text()
        return movie_name
        
    def get_movie_year(self, content) -> int:
        """Extract the year the movie was released"""

        year = int(re.sub('[^0-9]+', '', content.find(class_="lister-item-year").get_text()))
        return year

    def get_movie_certificate(self, content) -> str:
        """Extract the movie certificate (R, PG, PG13, etc.)"""

        try:
            certificate = content.find("span", "certificate").get_text()
        except Exception:
            certificate = "Not Rated"
        return certificate

    def get_movie_runtime(self, content) -> int:
        """Extract movie runtime"""

        runtime = int(content.find("span", "runtime").get_text().strip().replace("min",""))
        return runtime

    def get_movie_genre(self, content) -> str:
        """Extract movie genre"""
        genre = content.find("span","genre").get_text().strip()
        return genre

    def get_imdb_rating(self, content) -> float:
        """Extract IMDB movie rating (out of 10)"""

        imdb_rating = float(content.find("div","ratings-bar").find("strong").get_text().strip())
        return imdb_rating
        
    def get_movie_description(self, content) -> str:
        """Extract the movie description"""

        movie_description = content.find_all("p","text-muted")[1].get_text()
        return movie_description

    def get_movie_directors_and_stars(self, content) -> tuple:
        """Extracts the movie directors and stars, returns as a tuple
        the first element of the tuple is the string of all directors, the second 
        element is all the main cast"""

        people = content.find("p",class_="").text
        people = people.strip()
        directors,stars = people.split("|")[0].strip().replace("\n","").replace("Director:","").split(","), people.split("|")[1].strip().replace("\n","").replace("Stars:","").split(",")

        directors = str(directors).replace("[","").replace("]","")
        stars = str(stars).replace("[","").replace("]","")

        return (directors, stars)



