from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import or_


DATABASE_URI = ''
engine = create_engine(DATABASE_URI)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(Date)

    def __repr__(self):
        return "<Book(title='{}', author='{}', pages={}, published={})>"\
                .format(self.title, self.author, self.pages, self.published)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()

book1 = Book(
    title='Deep Learning',
    author='Ian Goodfellow',
    pages=775,
    published=datetime(2016, 11, 18)
)
book2 = Book(
    title='Databases',
    author='Jean Jeanes',
    pages=342,
    published=datetime(2016, 12, 28)
)
book3 = Book(
    title='Learning sql',
    author='Dimitri Kras',
    pages=814,
    published=datetime(2016, 11, 30)
)
s.add(book1)
s.add_all([book2, book3])
s.commit()
####################### get all data

books = s.query(Book)
for book in books:
    print(book.title, book.author, book.pages)

####################### Get data in order
books = s.query(Book).order_by(Book.title)
for book in books:
    print(book.title, book.author, book.pages)

###################### get data by filtering
book = s.query(Book).filter(Book.pages==342).first()  #one
print(book.title, book.author, book.pages)

books = s.query(Book).filter(or_(Book.pages==342, Book.pages==775)) #more than one
for book in books:
    print(book.title, book.author, book.pages)
###################### counting the results
book_count = s.query(Book).filter(or_(Book.pages==342, Book.pages==775)).count()
print(book_count)


#################### update data in database
book = s.query(Book).filter(Book.pages==100).first()
book.pages = 775
s.commit()

####################delete data
book = s.query(Book).filter(Book.title=="Databases").first()
s.delete(book)
s.commit()

s.close()