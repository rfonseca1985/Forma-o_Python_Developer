import pymongo

# Credenciais de conexão
USERNAME = "pymongo"
PASSWORD = "123456780"

# Conectar ao banco de dados MongoDB
client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.wpzznia.mongodb.net/"
                             "?retryWrites=true&w=majority&appName=Cluster0")
"""
Estabelece uma conexão com o banco de dados MongoDB usando o nome de usuário e senha fornecidos.
"""

# Selecionando o banco de dados 'banco'
db = client['banco']
"""
Seleciona o banco de dados 'banco' do cliente MongoDB.
"""

# Selecionando a coleção 'clientes'
clientes = db['clientes']
"""
Seleciona a coleção 'clientes' do banco de dados 'banco'.
"""

# Selecionando a coleção 'contas'
contas = db['contas']
"""
Seleciona a coleção 'contas' do banco de dados 'banco'.
"""

# Inserindo documentos na coleção 'clientes'
cliente_pedro_id = clientes.insert_one(
    {'nome': 'Pedro', 'cpf': '055.515.650-84', 'endereco': 'Rua Logo Ali, 100'}).inserted_id
cliente_luiz_id = clientes.insert_one(
    {'nome': 'Luiz', 'cpf': '648.388.400-12', 'endereco': 'Rua Ladeira Ingrime, 400'}).inserted_id
cliente_marcia_id = clientes.insert_one(
    {'nome': 'Marcia', 'cpf': '935.637.590-90', 'endereco': 'Rua Torta, 1000'}).inserted_id
"""
Insere novos documentos na coleção 'clientes' e armazena os IDs dos documentos inseridos.
"""

# Inserindo documentos na coleção 'contas'
conta_pedro_id = contas.insert_one({'tipo': 'Corrente', 'agencia': '0001', 'numero': '0001', 'saldo': '1000.00',
                                    'id_cliente': cliente_pedro_id}).inserted_id
conta_luiz_id = contas.insert_one({'tipo': 'Poupança', 'agencia': '0002', 'numero': '0002', 'saldo': '2000.00',
                                   'id_cliente': cliente_luiz_id}).inserted_id
conta_marcia_id = contas.insert_one({'tipo': 'Investimento', 'agencia': '0003', 'numero': '0003', 'saldo': '3000.00',
                                     'id_cliente': cliente_marcia_id}).inserted_id
"""
Insere novos documentos na coleção 'contas' e armazena os IDs dos documentos inseridos.
"""


def get_cliente_by_id(id):
    """
    Retorna um cliente pelo seu ID.
    """
    return clientes.find_one({'_id': id})


def get_all_clientes():
    """
    Retorna todos os clientes.
    """
    return list(clientes.find())


def get_contas_by_cliente_id(id):
    """
    Retorna todas as contas associadas a um cliente específico.
    """
    return list(contas.find({'id_cliente': id}))


def get_conta_by_id(id):
    """
    Retorna uma conta pelo seu ID.
    """
    return contas.find_one({'_id': id})


def get_all_contas():
    """
    Retorna todas as contas.
    """
    return list(contas.find())


def get_cliente_by_conta_id(id):
    """
    Retorna o cliente associado a uma conta específica.
    """
    conta = get_conta_by_id(id)
    if conta:
        return get_cliente_by_id(conta['id_cliente'])


# Obtendo um cliente específico pelo ID
cliente = get_cliente_by_id(cliente_pedro_id)
print(cliente)  # Imprime as informações do cliente com o ID fornecido

# Obtendo todos os clientes
todos_os_clientes = get_all_clientes()
for cliente in todos_os_clientes:
    print(cliente)  # Imprime as informações de cada cliente

# Obtendo todas as contas de um cliente específico
contas_do_cliente = get_contas_by_cliente_id(cliente_pedro_id)
for conta in contas_do_cliente:
    print(conta)  # Imprime as informações de cada conta do cliente

# Obtendo uma conta específica pelo ID
conta = get_conta_by_id(conta_pedro_id)
print(conta)  # Imprime as informações da conta com o ID fornecido

# Obtendo todas as contas
todas_as_contas = get_all_contas()
for conta in todas_as_contas:
    print(conta)  # Imprime as informações de cada conta

# Obtendo o cliente associado a uma conta específica
cliente_da_conta = get_cliente_by_conta_id(conta_pedro_id)
print(cliente_da_conta)  # Imprime as informações do cliente da conta
