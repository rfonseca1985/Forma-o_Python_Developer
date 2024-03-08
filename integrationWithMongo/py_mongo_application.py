"""
Exemplo do como usar MongoDB com pymongo
"""

from datetime import datetime
import pprint
import pymongo

# Credenciais de conexão
USERNAME= "pymongo"
PASSWORD= "123456780"

# Conectar ao banco de dados MongoDB
client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.wpzznia.mongodb.net/"
                             "?retryWrites=true&w=majority&appName=Cluster0")

# Selecionar o banco de dados e a coleção
db = client.test
posts_collection = db.posts

# Inserir um documento na coleção
posts = {
    "author": "Mike",
    "text": "my first application based on python",
    "tags": ["python3", "mongodb", "pymongo"],
    "date": datetime.utcnow()
}

post_id = posts_collection.insert_one(posts).inserted_id
print(f"Documento inserido com o ID: {post_id}")

# Encontrar e imprimir o documento recém-inserido
print(posts_collection.find_one())

# Usar pprint para imprimir de forma mais legível
pprint.pprint(posts_collection.find_one())

new_post = [{
    "author": "Mike",
    "text": "my first text",
    "tags": ["python3", "mongodb"],
    "date": datetime.utcnow(),
},
    {
        "author": "Joe",
        "text": "my second text",
        "tags": ["python3", "mongodb"],
        "date": datetime.utcnow()

    }]

result = posts_collection.insert_many(new_post)
print(result.inserted_ids)

for post in posts_collection.find():
    pprint.pprint(post)
