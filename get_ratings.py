#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from pyquery import PyQuery
import requests


def get_local_movies():
    """ Get movies showing at the local theater. """
    GOOGLE_THEATER_ID = os.environ.get('GOOGLE_THEATER_ID')
    url = 'http://www.google.com/movies?hl=en&tid={0}'.format(GOOGLE_THEATER_ID)
    d = PyQuery(url=url)
    p = d('.movie')
    # for element in p:
    #     print PyQuery(element)(".name").text()
    return [PyQuery(element)(".name").text() for element in p]

def get_box_office_movies():
    """ Get data for 50 box office movies from Rotten Tomatoes. """
    url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json'
    ROTTEN_TOMATOES_API_KEY = os.environ.get('ROTTEN_TOMATOES_API_KEY')
    payload = {'apikey': ROTTEN_TOMATOES_API_KEY, 'limit': '50'}
    r = requests.get(url, params=payload)
    movie_dict = json.loads(r.content)
    return movie_dict

def get_box_office_movies_from_file():
    """ Get data for 50 box office movies from Rotten Tomatoes, from local JSON file. """
    with open('box_office.json') as f:
        movie_dict = json.load(f)
        return movie_dict

def print_movie_table(movies):
    """ Print movies with critics' and audience score. """
    print("{0:35} {1:7} {2:8}".format("Movie", "Critics", "Audience"))
    for movie in movies:
        print(
            "{0:35} {1:7} {2:8}".format(
                movie['title'], 
                movie['ratings']['critics_score'], 
                movie['ratings']['audience_score']
                )
            )

def print_movie_table_from_file():
    """ Given a .json movie file, print movies/ratings as a table. """
    movie_dict = get_box_office_movies_from_file()
    print_movie_table(movie_dict['movies'])
    
def print_movie_table_from_api():
    """ Given JSON from the Rotten Tomatoes API, print movies/ratings as a table. """
    movie_dict = get_box_office_movies()
    print_movie_table(movie_dict['movies'])

def print_ratings(movies, movie_data):
    """ Given list of movie strings and dict of movie data, print their ratings. """
    print("{0:35} {1:7} {2:8}".format("Movie", "Critics", "Audience"))
    for movie in movies:
        print("{0}...".format(movie))
        for m in movie_data['movies']:
            if movie == m['title']:
                print("{0:35} {1:7} {2:8}".format(
                    movie, 
                    m['ratings']['critics_score'], 
                    m['ratings']['audience_score']))
                break

if __name__ == "__main__":
    local_movies = get_local_movies()
    movie_dict = get_box_office_movies_from_file()

    print_ratings(local_movies, movie_dict)
