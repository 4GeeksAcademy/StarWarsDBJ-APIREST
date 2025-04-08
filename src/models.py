from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(120),unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    #relationships
    favuser = relationship('Favorites', back_populates = 'user')


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_name: Mapped[str] = mapped_column(String(120))

    #relationships
    favplanet = relationship('Favorites', back_populates = 'planet')

class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    char_name: Mapped[str] = mapped_column(String(120))

    #relationships
    favchara = relationship('Favorites', back_populates = 'chara')

class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'),nullable=True)
    char_id: Mapped[int] = mapped_column(ForeignKey('characters.id'),nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    #relationships
    chara = relationship('Characters', back_populates = 'favchara')
    planet = relationship('Planets', back_populates = 'favplanet')
    user = relationship('User', back_populates = 'favuser')