from ufc import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    fight = db.Column(db.String(100), nullable=False)
    fight_date = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Record('{self.email}', '{self.fight}', '{self.fight_date}') "
