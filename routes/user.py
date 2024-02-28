from bson import ObjectId
from fastapi import APIRouter
from models.library_model import User,Book,User_update
from config.db import customers_collection,books_collection

user= APIRouter()

def bson_to_str(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, ObjectId):
                obj[key] = str(value)
    return obj

@user.get('/get_users',tags=['USER'])
async def find_all_users():
    all_users =list(customers_collection.find())
    user_list = [bson_to_str(user) for user in all_users]
    return user_list
 
@user.get("/get-user/{user_id}",response_model=User,tags=['USER'])
async def find_user_by_id(user_id:int):
        user_details = customers_collection.find_one({"user_id":user_id})
        if  user_details:
            return user_details    
        else:
            return {"user_details not found"}
       
@user.post('/post_user',tags=['USER'])
async def create_user(user:User):
    try:
        result = customers_collection.insert_one(dict(user))
        return {"message": "User created successfully", "user_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}
    
@user.put("/update-user/",tags=['USER'])
async def update_user(fname: str, lname: str, update_choice: str, new_value: str):
    try:
        existing_user = customers_collection.find_one({"$and":[{"fname": fname}, {"lname":lname}]})
        if existing_user:
            update_data = {}
            if update_choice == "fname":
                update_data["fname"] = new_value
            elif update_choice == "lname":
                update_data["lname"] = new_value
            elif update_choice == "phone_no":
                update_data["phone_no"] = new_value
            elif update_choice == "email":
                update_data["email"] = new_value
            else:
                raise ValueError("Invalid update choice")
           
            result = customers_collection.update_one({"fname": fname, "lname":lname} ,{"$set": update_data})
            if result.modified_count == 1:
                return update_data
            else:
                return {"message": "No user found"}
        else:
            return {"message": "User not found"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}

@user.delete("/delete-user/{user_id}",tags=['USER'])
async def delete_user(user_id :int ):
    user_details = customers_collection.find_one({"user_id":user_id})
    if user_details:
        customers_collection.delete_one(user_details)
        return { "User deleted successfully"}
    else:
        return {"User not exists"}

@user.get('/get_books',tags=['BOOK'])
async def find_all_books():
    all_books =list(books_collection.find())
    book_list = [bson_to_str(book) for book in all_books]
    return book_list

@user.get("/get-book/{book_id}",tags=['BOOK'],response_model=Book)
async def find_book_by_id(book_id:int ):
    book_details = books_collection.find_one({"book_id":book_id})
    if not book_details:
        return {"Book not found"}
   
    return book_details

@user.post('/post_book',tags=['BOOK'])
async def create_book(book:Book):
    try:
        result = books_collection.insert_one(dict(book))
        return {"message": "Book created successfully", "book_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}


@user.put("/update-book/",tags=['BOOK'])
async def update_book(book_name: str ,author:str , update_choice: str, new_value: str):
    try:
        existing_user = books_collection.find_one({"$and":[{"book_name": book_name}, {"author":author}]})
        if existing_user:
            update_data = {}
            if update_choice == "book_id":
                update_data["book_id"] = new_value
            elif update_choice == "author":
                update_data["author"] = new_value
            elif update_choice == "book_name":
                update_data["book_name"] = new_value
            elif update_choice == "publisher":
                update_data["publisher"] = new_value
            elif update_choice == "availability":
                update_data["availability"] = new_value
            elif update_choice == "isbn_no":
                update_data["isbn_no"] = new_value
            else:
                raise ValueError("Invalid update choice")
           
            result = books_collection.update_one({"book_name": book_name, "author":author} ,{"$set": update_data})
            if result.modified_count == 1:
                return update_data
            else:
                return {"message": "No book found"}
        else:
            return {"message": "book not found"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}
    
@user.put("/borrow_book",tags=['BOOK'])
async def borrow_book(user_id: int, book_name: str,author:str):
    try:
        existing_user = customers_collection.find_one({"user_id":user_id})
        if existing_user:
            existing_book = books_collection.find_one({"$and":[{"book_name": book_name, "author":author,"availability": {"$gt": 0}}]}) 
            if existing_book:
                books_collection.update_one({"book_id": existing_book['book_id'], "availability": {"$gt": 0}}, {"$inc": {"availability": -1}})
                customers_collection.update_one({"user_id": user_id}, {"$addToSet": {"borrowed_books": existing_book['book_name']}})
                return {"Book borrowed successfully."}
            else:
                return {"Book not found or not available."}
        else:
                return {"Userf not existing"}
    except Exception as e:
        return{"Error finding book"}

@user.put("/return-book/{user_id}",tags=['BOOK']) 
async def return_book(user_id: int,book_name: str,author:str ,):
    try:
        existing_user =customers_collection.find_one({"user_id":user_id})
        if existing_user:                                     
            existing_book = books_collection.find_one({"$and":[{"book_name": book_name, "author":author,"availability": {"$gt": 0}}]}) 
            if existing_book:
                books_collection.update_one({"book_id": existing_book['book_id'],}, {"$inc": {"availability": 1}})
                customers_collection.update_one({"user_id": user_id}, {"$pull": {"borrowed_books": existing_book['book_name']}})
                return {"Returned Book"}
            else:
                return {"Book not found or not available."}
        else:
            return {"User not found."}
    except Exception as e:
        return{e}

@user.delete("/delete-book/{book_id}",tags=['BOOK'])
async def delete_book(book_id:int):
    book_details = books_collection.find_one({"book_id":book_id})
    if book_details:
        books_collection.delete_one(book_details)
        return {"Book deleteed Successfully"}
    else:
        return {"Book not found"}