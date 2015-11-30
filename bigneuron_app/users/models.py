from bigneuron_app.users.constants import *
from bigneuron_app.utils import id_generator
from bigneuron_app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(264), nullable=False)
    iam_username = Column(String(128))
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, onupdate=func.now())
    job = relationship('Job', backref=backref('users'))

    def __init__(self, email, iam_username=DEFAULT_IAM_USER):
        self.email = email
        self.iam_username = iam_username

      
    def __repr__(self):
        return '<User %r>' % (self.email)