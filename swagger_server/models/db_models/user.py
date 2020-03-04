# coding: utf-8
from swagger_server.__main__ import db
import bcrypt


class User(db.Model):
    """Model for user accounts."""
    __tablename__ = 'user'

    user_id = db.Column(db.INTEGER(), primary_key=True)
    user_name = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(32), nullable=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        """Check hashed password."""
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

    def __repr__(self):
        return '<User {}>'.format(self.user_name)
