from flask_sqlalchemy import SQLALchemy

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float,nullable=False)

    def __repr__(self):
        return f'<Value {self.value}>'
