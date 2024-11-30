from sqlmodel import SQLModel, Field, Session, create_engine


class Config:
    ENGINE = create_engine("sqlite:///books.db")
    SESSION = Session(bind=ENGINE)

    @classmethod
    def restart_db(cls):
        SQLModel.metadata.drop_all(bind=cls.ENGINE)
        SQLModel.metadata.create_all(bind=cls.ENGINE)
    
    @classmethod
    def migrate(cls):
        books = [Book(title=f"title{x}", 
                      author=f"author{x}", 
                      year=x*1000,
                      description=f"description{x}",
                      rating=x%5) for x in range(10)]
        
        book = Book(title="really looooooooooooooooooong title", 
                    author="and author tooooooooooooooooooooo", 
                    year=4242,
                    description="description tooooooooooooooooooooooooooooo but it doesn't matter",
                    rating=4.2)
        
        cls.SESSION.add(book)
        cls.SESSION.add_all(books)
        cls.SESSION.commit()


class AutoID(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)


class Book(AutoID, table=True):
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    year: int = Field(nullable=False)
    description: str = Field(nullable=False)
    rating: float = Field(default=0)
    image_url: str = Field(default="https://picsum.photos/200/300?blur=5") # https://picsum.photos/200/300?grayscale
