from pydantic import BaseModel

class User(BaseModel):
    user_id:int
    fname: str
    lname:str
    phone_no:int
    email: str
    
class User_update(BaseModel):

    fname: str
    lname:str
    phone_no:int
    email: str
    
class Book(BaseModel):
    book_id:int
    book_name: str
    author:str
    publisher:str
    availability:int
    isbn_no:str
    
class User_borrowed(BaseModel):
    user_id:int
    fname: str
    lname:str
    phone_no:int
    email: str
    borrowed_books:list
    