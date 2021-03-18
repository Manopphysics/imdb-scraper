#This file provides a database connection to postgres server to store the extracted IMDB movie info
import psycopg2


class MovieDatabase(object):
    def __init__(self, dbname, user, password):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password)
        self.cur = self.conn.cursor()
        self.sql_insert_movie = "INSERT INTO top_movies1000 (title, year, certificate, runtime, genre, imdb_rating, description, directors, stars) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"


    def insert_movie(self, movie_name, year, certificate, runtime, genre, imdb_rating, description, directors, stars) -> bool:
        self.cur.execute(self.sql_insert_movie, (movie_name, year, certificate, runtime, genre, imdb_rating, description, directors, stars))
        self.conn.commit()
