import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from data.db_session import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin


class User(BaseModel, UserMixin):
    __tablename__ = "users"
    __repr_attrs__ = ["surname", "name"]
    serialize_only = ("id",
                      "name",
                      "surname",
                      "patronymic",
                      "fullname",
                      "city",
                      "birthday",
                      "email",
                      "is_creator",
                      "link",
                      )
    
    short_serialize_only = ("id",
                            'name',
                            'surname',
                            "fullname",
                            "email"
                            )

    surname = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    patronymic = sa.Column(sa.String, nullable=True)
    city = sa.Column(sa.String, nullable=True)
    birthday = sa.Column(sa.Date)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    is_creator = sa.Column(sa.Boolean, default=False)

    @property
    def fullname(self):
        if self.patronymic:
            return "{0} {1} {2}".format(self.surname, self.name, self.patronymic)
        else:
            return "{0} {1}".format(self.surname, self.name)

    @property
    def link(self) -> str:
        return "/profile/{0}".format(self.id)

    def __str__(self):
        return self.fullname

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def years_old(self):
        today = datetime.date.today()
        birth = self.birthday
        years = today.year - birth.year
        if int(today.strftime("%j")) < int(birth.strftime("%j")):
            years -= 1
        return years

    @property
    def is_admin(self):
        return self.id == 1
    
    
class AnonymousUser(AnonymousUserMixin):
    id = 0
    is_admin = False