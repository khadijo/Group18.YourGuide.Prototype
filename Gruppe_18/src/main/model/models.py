import sqlalchemy
from sqlalchemy import Table, Column, String, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
import uuid


Base = sqlalchemy.orm.declarative_base()

tour_account_association = Table(
    'tour_account_association', Base.metadata,
    Column('tour_id', String, ForeignKey('Tour.id')),
    Column('account_id', String, ForeignKey('User.id'))
)


class Account(Base):
    __tablename__ = "User"
    account_id = Column("id", String, primary_key=True)
    username = Column("username", String)
    password = Column("password", String)
    phoneNumber = Column("phoneNumber", String)
    emailAddress = Column("emailAddress", String)
    tours = relationship("Tour", secondary=tour_account_association, back_populates="participants")

    def __init__(self, username, password, phoneNumber, emailAddress):
        self.account_id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress

    def __repr__(self):
        return f"({self.account_id}) {self.username} {self.password} {self.phoneNumber} {self.emailAddress}"


class Tour(Base):
    # duration in hours
    # cost in dollars
    __tablename__ = "Tour"
    tour_id = Column("id", String, primary_key=True)
    title = Column("title", String)
    date = Column("date", DATETIME)
    destination = Column("destination", String)
    duration = Column("duration", Integer)
    cost = Column("cost", Integer)
    max_travelers = Column("max_travelers", Integer)
    language = Column("language", String)
    pictureURL = Column("pictureURL", String)
    booked = Column("booked", Integer, default=0)
    participants = relationship("Account", secondary=tour_account_association, back_populates="tours")

    def __init__(self, title, date, destination, duration, cost, max_travelers, language, pictureURL):
        self.tour_id = str(uuid.uuid4())
        self.title = title
        self.date = date
        self.destination = destination
        self.duration = duration
        self.cost = cost
        self.language = language
        self.max_travelers = max_travelers
        self.pictureURL = pictureURL

    def __repr__(self):
        return f"({self.tour_id}) {self.title} {self.destination} {self.duration} {self.cost} {self.language} {self.max_travelers} {self.pictureURL} {self.booked}"
