import argparse
import pickle
import requests
import csv

from settings import url_auth, url_edit


def send_ratings_single(ratings, username, password):
    payload = {'si_username': username,
               'si_password': password}
    files = []
    ratings['fl_submit_batch'] = None
    s = requests.Session()
    response = s.request("POST", url_auth, data=payload, files=files, allow_redirects=False)
    for key in ratings:
        url = f"https://www.criticker.com/ajax/submitRating.php?f={key}&s={ratings[key]}&m=fi_container&ext=https%3A%2F%2Fwww.criticker.com%2Fforum%2F"

        response2 = s.request("GET", url)


def main():
    parser = argparse.ArgumentParser(description='Criticker ratings import.')
    parser.add_argument("ratings_csv")
    args = parser.parse_args()
    username = input("Username: ")
    password = input("Password: ")

    with open('all_films.pkl', 'rb') as f:
        films = pickle.load(f)

    ratings = {}
    names = []
    with open(args.ratings_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        next(reader, None)  # skip header

        for row in reader:
            imdb_id = row[-1]
            score = row[0]

            if imdb_id in films:
                crit_id = films[imdb_id]
                ratings[crit_id] = int(score)
            else:
                print(f"Film {imdb_id} not in database")
    send_ratings_single(ratings, username, password)

def send_ratings(ratings, username, password):
    payload = {'si_username': username,
               'si_password': password}
    files = []
    ratings['fl_submit_batch'] = None
    s = requests.Session()
    response = s.request("POST", url_auth, data=payload, files=files, allow_redirects=False)
    response2 = s.request("POST", url_edit, data=ratings, files=files, allow_redirects=False)


if __name__ == '__main__':
    main()
