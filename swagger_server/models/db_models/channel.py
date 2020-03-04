from swagger_server.__main__ import db


class Channel(db.Model):
    __tablename__ = 'channel'

    channel_id = db.Column(db.INTEGER(), primary_key=True)
    channel_name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    channel_capacity = db.Column(db.INTEGER(), nullable=False)
    channel_type = db.Column(db.Enum('TEXT', 'VOICE', 'DM'), nullable=False)
    channel_position = db.Column(db.INTEGER(), nullable=False)

    user = db.relationship('User')
