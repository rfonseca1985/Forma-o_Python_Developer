from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import func

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

# Criando uma classe base para modelos declarativos
Base = declarative_base()


# Definindo a classe User, que representa a tabela 'user_account'
class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    # Estabelecendo um relacionamento um-para-muitos com a classe Address
    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


# Definindo a classe Address, que representa a tabela 'address'
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'), nullable=False)

    # Estabelecendo um relacionamento de referência inversa com a classe User
    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"


# Criando um mecanismo (engine) para o banco de dados SQLite em memória
engine = create_engine('sqlite://')

# Criando todas as tabelas definidas no modelo declarativo (Base) no banco de dados
Base.metadata.create_all(engine)

# Criando um inspetor para examinar o banco de dados
inspector = inspect(engine)

# Verificando se a tabela 'user_account' existe no banco de dados
print(inspector.has_table(table_name='user_account'))

# Obtendo a lista de todas as tabelas presentes no banco de dados
print(inspector.get_table_names())

# Obtendo e imprimindo o nome do esquema padrão associado ao banco de dados
print(inspector.default_schema_name)

# Criando uma sessão para interagir com o banco de dados
with Session(engine) as session:
    # Criando uma instância da classe User com informações para Juliana e seu endereço
    juliana = User(name="Juliana", fullname="Juliana Silva",
                   address=[Address(email_address="juliana_silva@email.com"),
                            Address(email_address="juliana_s@email.com")])

    # Criando uma instância da classe User com informações para Luiz e seu endereço
    luiz = User(name="Luiz", fullname="Luiz Augusto",
                address=[Address(email_address="luiz_augusto@email.com")])

    # Adicionando as instâncias criadas à sessão para posteriormente serem adicionadas ao banco de dados
    session.add_all([juliana, luiz])

    # Efetivando as mudanças pendentes na sessão e persistindo-as no banco de dados
    session.commit()

from sqlalchemy import select

# Criando uma declaração (statement) SELECT para buscar usuários pelo nome
stmt = select(User).where(User.name.in_(['Juliana', 'Luiz']))

# Utilizando session.scalars() para executar a declaração e obter os resultados
for user in session.scalars(stmt):
    print(user)

# Criando uma declaração (statement) SELECT para buscar endereços com user_id igual a 1
stmt_address = select(Address).where(Address.user_id.in_([1]))

# Utilizando session.scalars() para executar a declaração e obter os resultados
for address in session.scalars(stmt_address):
    print(address)

# Criando uma declaração (statement) SELECT para buscar usuários ordenados pelo campo fullname em ordem decrescente
stmt_order = select(User).order_by(User.fullname.desc())

# Utilizando session.scalars() para executar a declaração e obter os resultados
for user in session.scalars(stmt_order):
    print(user)

# Criando uma declaração (statement) SELECT com junção (join) entre as tabelas User e Address
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)

# Utilizando session.scalars() para executar a declaração e obter os resultados
for result in session.scalars(stmt_join):
    print(result)

# Conectando diretamente ao banco de dados e executando a declaração SELECT
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()

# Iterando sobre os resultados e imprimindo cada resultado
for result in results:
    print(result)

# Criando uma declaração (statement) SELECT para contar o número total de registros na tabela User
stmt_count = select(func.count()).select_from(User)

# Utilizando session.scalars() para executar a declaração e obter os resultados
for result in session.scalars(stmt_count):
    print(result)

