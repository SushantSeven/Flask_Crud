from flask import Flask, jsonify, request
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Sample data (can be replaced with a database)
books = [
    {"id": 1, "title": "Poems", "author": "Jane Smith"},
    {"id": 2, "title": "Short stories", "author": "William"}
]

@app.route('/', methods=['GET'])
def home():
    return 'HOme Page try /books , /books/id , /books/fetch_data_json , /books/fetch_data_xml'

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return books


# Get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id']==book_id:
            return book

    return {'error':'Book not found'}

# Create a book
@app.route('/books', methods=['POST'])
def create_book():
    new_book={'id':len(books)+1, 'title':request.json['title'], 'author':request.json['author']}
    books.append(new_book)
    return new_book


# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    for book in books:
        if book['id']==book_id:
            book['title']=request.json['title']
            book['author']=request.json['author']
            return book 
    return {'error':'Book not found'}

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id']==book_id:
            books.remove(book)
            return {"data":"Book Deleted Successfully"}

    return {'error':'Book not found'}

# fetch json data and parse
@app.route('/books/fetch_data_json', methods=['GET'])
def fetch_data():
    url = 'https://dummyjson.com/products'
    response = requests.get(url)
    if response.ok:
        json_response = response.json()
        print(json_response)
        return {'Response Captured':'True','Product':json_response['products'][0]['description'], 'Description':json_response['products'][1]['description']}

    else:
        print("Invalid request")
        return {'Respone Captured':'False'}

# fetch xml data and parse    
@app.route('/books/fetch_data_xml', methods=['GET'])
def fetch_data_xml():
    url = 'https://www.w3schools.com/xml/note.xml'
    response = requests.get(url)
    if response.ok:
        xml_data = BeautifulSoup(response.content, 'lxml')
        print(xml_data)
        xml_tag = xml_data.find('body')
        return str(xml_tag)

    else:
        print("Invalid request")
        return {'Respone Captured':'False'}
    

if __name__ == '__main__':
    app.run(debug=True)