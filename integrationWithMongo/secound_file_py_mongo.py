"""
Segundo exemplo com pymongo
"""

import pprint
import pymongo

# Credenciais de conexão
USERNAME = "pymongo"
PASSWORD = "123456780"

# Conectar ao banco de dados MongoDB
client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.wpzznia.mongodb.net/"
                             "?retryWrites=true&w=majority&appName=Cluster0")

# Selecionar o banco de dados e a coleção
db = client.test
posts_collection = db.posts

# Iterar e imprimir todos os documentos na coleção 'posts'
for post in db.posts.find():
    pprint.pprint(post)

# Contar o número total de documentos na coleção 'posts'
document_count = posts_collection.count_documents({})
print(f"Total de documentos na coleção: {document_count}")

# Recuperando informação de forma ordenada
print('Recuperando de forma ordenada')
for post in db.posts.find({}).sort("date"):
    pprint.pprint(post)

# Criar um índice único na coleção 'profiles' baseado no campo 'author'
result = db.profiles.create_index([("author", pymongo.ASCENDING)], unique=True)
print(sorted(list(db.profiles.index_information())))

# Inserir documentos na coleção 'profiles_user'
user_profile_user = [
    {"user_id": 200, "name": "Luke"},
    {"user_id": 201, "name": "Leia"}]

db.profiles_user.insert_many(user_profile_user)

# Imprimir os nomes das coleções no banco de dados
print(db.list_collection_names())
for collection in db.list_collection_names():
    print(collection)

db['posts'].drop()
