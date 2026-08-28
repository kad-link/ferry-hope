from database import session

def get_db():
    with session() as db:
        yield db