import model
import csv

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
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    session.commit()



if __name__ == "__main__":
    s= model.connect()
    main(s)
