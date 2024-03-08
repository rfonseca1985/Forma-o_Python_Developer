import sqlalchemy
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Double
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

# Criando uma classe base para modelos declarativos
Base: object = declarative_base()


class Cliente(Base):
    """
    Classe Cliente que representa a tabela 'cliente' no banco de dados.
    """
    __tablename__ = 'cliente'
    id = sqlalchemy.Column(Integer, primary_key=True)
    nome = sqlalchemy.Column(String)
    cpf = sqlalchemy.Column(String)
    endereco = sqlalchemy.Column(String)

    # Estabelecendo um relacionamento um-para-muitos com a classe Conta
    contas = relationship("Conta", back_populates="cliente")

    def __repr__(self):
        """
        Retorna uma representação legível do objeto Cliente.
        """
        return (f"Cliente(id={self.id}, nome: {self.nome}, "
                f"cpf: {self.cpf}, endereco: {self.endereco})")

    @classmethod
    def get_by_id(cls, session, id):
        """
        Retorna um objeto Cliente pelo seu ID.
        """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all(cls, session):
        """
        Retorna todos os objetos Cliente.
        """
        return session.query(cls).all()

    def get_contas(self, session):
        """
        Retorna todas as contas associadas a este Cliente.
        """
        return session.query(Conta).filter_by(id_cliente=self.id).all()


class Conta(Base):
    """
    Classe Conta que representa a tabela 'conta' no banco de dados.
    """
    __tablename__ = 'conta'
    id = sqlalchemy.Column(Integer, primary_key=True)
    tipo = sqlalchemy.Column(String)
    agencia = sqlalchemy.Column(String)
    numero = sqlalchemy.Column(Integer)
    id_cliente = sqlalchemy.Column(Integer, ForeignKey('cliente.id'), nullable=False)
    saldo = sqlalchemy.Column(Double)

    # Estabelecendo um relacionamento muitos-para-um com a classe Cliente
    cliente = relationship("Cliente", back_populates="contas")

    def __repr__(self):
        """
        Retorna uma representação legível do objeto Conta.
        """
        return (f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, "
                f"numero={self.numero}, id_cliente={self.id_cliente}, saldo={self.saldo})")

    @classmethod
    def get_by_id(cls, session, id):
        """
        Retorna um objeto Conta pelo seu ID.
        """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all(cls, session):
        """
        Retorna todos os objetos Conta.
        """
        return session.query(cls).all()

    def get_cliente(self, session):
        """
        Retorna o Cliente associado a esta Conta.
        """
        return session.query(Cliente).filter_by(id=self.id_cliente).first()


# Criando um mecanismo (engine) para o banco de dados SQLite em memória
engine = create_engine('sqlite://')

# Criando todas as tabelas definidas no modelo declarativo (Base) no banco de dados
Base.metadata.create_all(engine)

# Criando um inspetor para examinar o banco de dados
inspector = inspect(engine)

# Criando uma sessão para interagir com o banco de dados
with Session(engine) as session:
    # Criando uma instância da classe Cliente com informações para Pedro
    pedro = Cliente(nome='Pedro', cpf='055.515.650-84', endereco='Rua Logo Ali, 100')
    # Criando uma instância da classe Cliente com informações para Luiz
    luiz = Cliente(nome='Luiz', cpf='648.388.400-12', endereco='Rua Ladeira Ingrime, 400')
    # Criando uma instância da classe Cliente com informações para Marcia
    marcia = Cliente(nome='Marcia', cpf='935.637.590-90', endereco='Rua Torta, 1000')

    # Criando uma instância da classe Conta para cada cliente
    conta_pedro = Conta(tipo='Corrente', agencia='0001', numero='0001', saldo='1000.00')
    conta_luiz = Conta(tipo='Poupança', agencia='0002', numero='0002', saldo='2000.00')
    conta_marcia = Conta(tipo='Investimento', agencia='0003', numero='0003', saldo='3000.00')

    # Adicionando as contas aos clientes correspondentes
    pedro.contas.append(conta_pedro)
    luiz.contas.append(conta_luiz)
    marcia.contas.append(conta_marcia)

    # Adicionando as instâncias criadas à sessão para serem posteriormente adicionadas ao banco de dados
    session.add_all([pedro, luiz, marcia])
    # Efetivando as mudanças pendentes na sessão e persistindo-as no banco de dados
    session.commit()

# Criando uma sessão para interagir com o banco de dados
with Session(engine) as session:
    # Usando o método get_by_id para obter um cliente específico pelo ID
    cliente = Cliente.get_by_id(session, 1)
    print(cliente)  # Imprime as informações do cliente com ID 1

    # Usando o método get_all para obter todos os clientes
    todos_os_clientes = Cliente.get_all(session)
    for cliente in todos_os_clientes:
        print(cliente)  # Imprime as informações de cada cliente

    # Usando o método get_contas para obter todas as contas de um cliente específico
    contas_do_cliente = cliente.get_contas(session)
    for conta in contas_do_cliente:
        print(conta)  # Imprime as informações de cada conta do cliente

    # Usando o método get_by_id para obter uma conta específica pelo ID
    conta = Conta.get_by_id(session, 1)
    print(conta)  # Imprime as informações da conta com ID 1

    # Usando o método get_all para obter todas as contas
    todas_as_contas = Conta.get_all(session)
    for conta in todas_as_contas:
        print(conta)  # Imprime as informações de cada conta

    # Usando o método get_cliente para obter o cliente de uma conta específica
    cliente_da_conta = conta.get_cliente(session)
    print(cliente_da_conta)  # Imprime as informações do cliente da conta
