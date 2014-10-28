import model
from datetime import datetime
from sqlalchemy import or_


def years(session):
    query = session.query(model.Movie)
    start_date = datetime(year=1970, month=01, day=01)
    end_date = datetime(year=1972, month=12, day=31)
    query = query.filter(model.Movie.released_at.between(start_date, end_date)) 
    results = query.all()
    return results 

def q_finder(session):
    query = session.query(model.Movie)
    # query = query.filter(or_(model.Movie.name.like('q%'), model.Movie.name.like('Q%')))
    query = query.filter(model.Movie.name.like('Q%')) 
    results = query.all()
    print results 

def main():
    session = model.connect()
    years(session)
    q_finder(session)

if __name__ == "__main__":
    main()
