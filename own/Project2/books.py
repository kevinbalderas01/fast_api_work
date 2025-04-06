from fastapi import FastAPI
from fastapi.param_functions import Body
from book_class import Book, BookRequest
from fastapi import Path, Query, HTTPException
from starlette import status


app = FastAPI()

BOOKS = [
    Book(1, 'Computer Science Pro', 'doginqiroby', 'Niceee', 5, 2000),
    Book(2, 'Be fast with fast api', 'doginqiroby', 'Niceee', 5, 2012),
    Book(3, 'Javascript for experts', 'doginqiroby', 'Bad', 2, 2024),
    Book(4, 'Recursion', 'doginqiroby', 'May improve', 4, 1998),
    Book(5, 'Computer Science Pro', 'doginqiroby', 'Could have been better', 3, 1999),
    Book(6, 'Computer Science Pro', 'doginqiroby', 'Ugggh', 1, 2008)

]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:   
            return book
    raise HTTPException(status_code=404, detail="Item not Found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(publish_date: int = Query(gt=1800, lt=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == publish_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_books_id(new_book))

def find_books_id(book: Book):
    book.book_id = 1 if len(BOOKS)==0 else BOOKS[-1].book_id+1
    return book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item does not exist')

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book.book_id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')