from app_config import db


class user_account(db.Model):
    __tablename__ = 'user_account'

    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_ID = db.Column(db.String(200), nullable=False)
    route_account = db.Column(db.String(20), nullable=False)
    route_password = db.Column(db.String(30), nullable=False)
    authority_level = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, open_ID, route_account, route_password):
        self.open_ID = open_ID
        self.route_account = route_account
        self.route_password = route_password

