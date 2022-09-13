import argparse
import pickle
import requests
import csv

from settings import url_edit, url_auth


def main():
    parser = argparse.ArgumentParser(description='Criticker ratings import.')
    parser.add_argument("ratings_csv")
    args = parser.parse_args()
    username = input("Username: ")
    password = input("Password: ")

    with open('films.pkl', 'rb') as f:
        films = pickle.load(f)

    ratings = {}

    with open(args.ratings_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        next(reader, None)  # skip header

        for row in reader:
            imdb_id = row[-1]
            score = row[0]
            if imdb_id in films:
                crit_id = films[imdb_id]
                ratings[f'fi_batchedit_input_{crit_id}'] = score
        else:
            print(f"Film {row[1]} not in database")

    send_ratings(ratings, username, password)


def send_ratings(ratings, username, password):
    payload = {'si_username': username,
               'si_password': password}
    files = []
    s = requests.Session()
    response = s.request("POST", url_auth, data=payload, files=files, allow_redirects=False)
    response2 = s.request("POST", url_edit, data=ratings, files=files, allow_redirects=False)

    print(response.text)


if __name__ == '__main__':
    main()
