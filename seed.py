import model
import csv
from datetime import datetime

def load_users(session):
    # use u.user

    with open('seed_data/u.user', 'rb') as csvfile:
        all_users = csv.reader(csvfile, delimiter = "|")
        for line in all_users:
            u = model.User()
            u.id = int(line[0])
            u.age = int(line[1])
            u.zipcode = line[4]
            print (u.id, u.age, u.zipcode)
            session.add(u)



    

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as csvfile:
        all_movies = csv.reader(csvfile, delimiter = "|")
        for line in all_movies:
            u = model.Movie()
            u.id = int(line[0])
            u.name = line[1].decode("latin-1")
            if line[2]:
                u.released_at = datetime.strptime(line[2], "%d-%b-%Y")
            print(u.released_at)
            u.imdb_url = line[4].decode("latin-1")
            session.add(u)

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as csvfile:
        all_ratings = csv.reader(csvfile, delimiter= "\t")
        for line in all_ratings:
            u = model.Rating()
            print line[0]
            u.user_id = int(line[0])
            u.movie_id = int(line[1])
            u.rating = int(line[2])
            session.add(u)


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # load_users(session)
    #load_movies(session)
    load_ratings(session)
    session.commit()



if __name__ == "__main__":
    s= model.connect()
    main(s)
