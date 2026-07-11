from fastapi import FastAPI, Path, HTTPException, Query, Body, status
import json

app = FastAPI()


# functions for load books
def load_books():
    with open("books.json", "r") as f:
        data = json.load(f)

    return data


# function for  save books
def save_data(data):
    with open("books.json", "w") as f:
        json.dump(data, f)


# creating api get request


# for dashboard or home page
@app.get("/")
def dashboard():
    return "A Book Management System"


# for about page
@app.get("/about")
def about():
    return "A fully functional API to manage our books records"


# for view all books
@app.get("/books")
def view_books():

    data = load_books()
    return data


# for sort books
@app.get("/books/sort")
def view_sorted_books(
    sort_by: str = Query(
        "rating", description="sorted on the basis of pages and rating"
    ),
    order: str = Query("desc", description="choose asc or desc"),
):

    valid_fields = ["pages", "rating"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"invalid input try with {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="choose between asc or desc")

    data = load_books()

    sorted_order = True if order == "desc" else False
    sorted_data = sorted(
        data,
        key=lambda x: x[sort_by],
        reverse=sorted_order,
    )

    return sorted_data


# for specific book
@app.get("/books/{book_id}")
def book_info(book_id: int = Path(..., description="student id", example=1)):
    data = load_books()

    for book in data:
        if book["book_id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="book not found")


# post request


@app.post("/create_books", status_code=status.HTTP_201_CREATED)
def add_books(book: dict = Body()):

    data = load_books()

    data.append(book)

    save_data(data)

    return book
