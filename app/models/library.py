from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base
from .enums import DifficultyLevel, Frequency


class LibraryLocation(Base):
    __tablename__ = "library_locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)


class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="publisher")
    magazines = relationship("Magazine", back_populates="publisher")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    publisher = relationship("Publisher", back_populates="books")
    editions = relationship("Edition", back_populates="book")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Edition(Base):
    __tablename__ = "editions"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    year = Column(Integer, nullable=False)
    book = relationship("Book", back_populates="editions")
    authors = relationship("Author", secondary="edition_authors")
    copies = relationship("BookCopy", back_populates="edition")


class EditionAuthor(Base):
    __tablename__ = "edition_authors"
    edition_id = Column(Integer, ForeignKey("editions.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)


class BookCopy(Base):
    __tablename__ = "book_copies"
    id = Column(Integer, primary_key=True)
    edition_id = Column(Integer, ForeignKey("editions.id"))
    location_id = Column(Integer, ForeignKey("library_locations.id"))
    edition = relationship("Edition", back_populates="copies")
    location = relationship("LibraryLocation")


class Magazine(Base):
    __tablename__ = "magazines"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    frequency = Column(Enum(Frequency), nullable=False)
    publisher = relationship("Publisher", back_populates="magazines")
    volumes = relationship("MagazineVolume", back_populates="magazine")


class MagazineVolume(Base):
    __tablename__ = "magazine_volumes"
    id = Column(Integer, primary_key=True)
    magazine_id = Column(Integer, ForeignKey("magazines.id"))
    year = Column(Integer, nullable=False)
    issue_number = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey("library_locations.id"))
    magazine = relationship("Magazine", back_populates="volumes")
    location = relationship("LibraryLocation")
    __table_args__ = (UniqueConstraint('magazine_id', 'year', 'issue_number'),)


class Puzzle(Base):
    __tablename__ = "puzzles"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    pieces = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey("library_locations.id"))
    location = relationship("LibraryLocation")


class Checkout(Base):
    __tablename__ = "checkouts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String, nullable=False)
    item_id = Column(Integer, nullable=False)
    checkout_date = Column(Date, nullable=False)
    return_date = Column(Date)
    user = relationship("User")
