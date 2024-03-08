from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, text

# Criando um mecanismo (engine) para um banco de dados SQLite em memória
engine = create_engine('sqlite:///:memory:')

# Criando um objeto de metadados
metadata_obj = MetaData()

# Criando uma tabela chamada 'user' com colunas específicas
user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40)),
    Column('email_address', String(60)),
    Column('nickname', String(60), nullable=False)
)

# Criando uma tabela chamada 'user_prefs' com colunas específicas
user_prefs = Table(
    'user_prefs',
    metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100)),
)

financial_info = Table(
    'financial_info',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False),
)

# Criando todas as tabelas no banco de dados associado ao mecanismo
metadata_obj.create_all(engine)

# Criando um objeto de Connection
connection = engine.connect()

# Inserindo dados usando o método insert() do SQLAlchemy
insert_statement = user.insert().values(user_name='rafael', email_address='rafael@email.com', nickname='rf')
connection.execute(insert_statement)

# Executando uma consulta SQL simples
sql = text('SELECT * FROM user')

# Executando a consulta SQL
result = connection.execute(sql)

# Iterando sobre os resultados e imprimindo-os
for row in result:
    print(row)

# Fechando a conexão
connection.close()
