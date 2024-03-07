from model import db, connect_to_db, User, Samps

def create_user(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def create_sample(sample_name, description, bpm, key, file_path):
    new_sample = Samps(
        sample_name=sample_name,
        description=description,
        bpm=bpm,
        key=key,
        file_path=file_path
    )
    db.session.add(new_sample)
    db.session.commit()

def get_samples():
    return Samps.query.all()

def get_sample_by_id(id):
    return Samps.query.get(id)

def get_users():
    return User.query.all()

def get_user_by_id(id):
    return User.query.get(id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)