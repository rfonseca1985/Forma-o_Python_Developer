from abc import ABC, abstractmethod
from datetime import datetime

# Interface Transacao
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Classes Saque e Deposito que implementam a interface Transacao
class Saque(Transacao):
    def registrar(self, conta, valor):
        # Lógica para registrar saque na conta
        pass

class Deposito(Transacao):
    def registrar(self, conta, valor):
        # Lógica para registrar depósito na conta
        pass

# Classe PessoaFisica
class PessoaFisica:
    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# Classe Cliente que estende PessoaFisica
class Cliente(PessoaFisica):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(nome, cpf, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, transacao, conta, valor):
        transacao.registrar(conta, valor)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Classe Conta
class Conta:
    def __init__(self, numero, agencia, cliente, saldo=0):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.saldo = saldo
        self.historico = Historico()

# Classe ContaCorrente que estende Conta
class ContaCorrente(Conta):
    numero_agencia_global = 1
    numero_conta_global = 1

    def __init__(self, cliente, saldo=0):
        super().__init__(ContaCorrente.numero_conta_global, ContaCorrente.numero_agencia_global, cliente, saldo)
        ContaCorrente.numero_conta_global += 1
        ContaCorrente.numero_agencia_global += 1
        self.limite = 500
        self.limite_saque_diario = 3

    def nova_conta(self, cliente):
        nova_conta_corrente = ContaCorrente(cliente)
        cliente.adicionar_conta(nova_conta_corrente)
        print(f"Conta criada com sucesso na agência {nova_conta_corrente.agencia}, conta número {nova_conta_corrente.numero}.")
        return nova_conta_corrente

    def sacar(self, valor):
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return

        if self.limite_saque_diario <= 0:
            print("Operação falhou! Número máximo de saques diários excedido.")
        elif valor > self.limite:
            print(f"Operação falhou! O valor do saque não pode exceder {self.limite}.")
        else:
            self.saldo -= valor
            self.historico.adicionar_transacao(f"Saque: R$ {valor:.2f}")
            self.limite_saque_diario -= 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            self.exibir_saldo()

    def depositar(self, valor):
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return

        self.saldo += valor
        self.historico.adicionar_transacao(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        self.exibir_saldo()

    def exibir_saldo(self):
        print(f"Saldo atual: R$ {self.saldo:.2f}")

    def exibir_extrato(self):
        print("Extrato:")
        for transacao in self.historico.transacoes:
            print("========================================")
            print(transacao)


def main():
    clientes = {}

    while True:
        menu_inicial = """
        Bem-vindo ao Sistema Bancário!
        Digite o número da agência e o número da conta separados por espaço para acessar sua conta ou c para criar uma nova conta:
        """
        agencia_e_conta_digitada = input(menu_inicial)

        if agencia_e_conta_digitada == "c":
            # Criação de um novo cliente
            nome = input("Informe o nome do cliente: ")
            cpf = input("Informe o CPF do cliente: ")

            data_nascimento_str = input("Informe a data de nascimento do cliente (formato: dd/MM/yyyy): ")

            while True:
                try:
                    data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Formato de data inválido. Tente novamente.")
                    data_nascimento_str = input("Informe a data de nascimento do cliente (formato: dd/MM/yyyy): ")

            endereco = input("Informe o endereço do cliente: ")
            cliente = Cliente(nome, cpf, data_nascimento, endereco)
            conta = ContaCorrente(cliente)
            cliente.adicionar_conta(conta)

            # Adicionar o novo cliente à lista de clientes
            clientes[(conta.agencia, conta.numero)] = cliente

            print(f"Cliente criado com sucesso: {nome} com CPF {cpf}.")
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
            print(f"Agência: {conta.agencia}, Conta: {conta.numero}")

        elif " " in agencia_e_conta_digitada:
            # Tentar localizar o cliente existente pela agência e número da conta
            numeros_agencia_conta = agencia_e_conta_digitada.split()
            if len(numeros_agencia_conta) == 2 and numeros_agencia_conta[0].isdigit() and numeros_agencia_conta[1].isdigit():
                numero_agencia = int(numeros_agencia_conta[0])
                numero_conta = int(numeros_agencia_conta[1])

                if (numero_agencia, numero_conta) in clientes:
                    cliente_atual = clientes[(numero_agencia, numero_conta)]
                    print(f"Bem-vindo de volta, {cliente_atual.nome}!")

                    # Adicione o código para abrir o menu aqui, ou chame a função do menu
                    abrir_menu(cliente_atual)

                else:
                    print("Cliente não encontrado. Tente novamente ou digite c para criar uma nova conta.")
            else:
                print("Entrada inválida. Certifique-se de fornecer agência e conta separados por espaço.")

        else:
            # Adicionar índice ao menu inicial
            indice_cliente = input("Digite o índice do cliente para acessar (ou c para criar uma nova conta): ")

            if indice_cliente == "c":
                continue
            elif indice_cliente.isdigit() and int(indice_cliente) < len(clientes):
                agencia, conta = list(clientes.keys())[int(indice_cliente)]
                cliente_atual = clientes[(agencia, conta)]
                print(f"Bem-vindo de volta, {cliente_atual.nome}!")


                abrir_menu(cliente_atual)

            else:
                print("Agência e Conta Corrente invalidas . Tente novamente ou digite c para criar uma nova conta.")

def abrir_menu(cliente_atual):
    # Coloque aqui o código do menu
    menu = """
       ========================================
       [d] Depositar
       [s] Sacar
       [e] Extrato
       [a] Saldo
       [v] Voltar à tela inicial
       [q] Sair
       ========================================
    """

    while True:
        opcao = input(menu)

        if opcao == "d" or opcao == "s":
            valor = float(input("Informe o valor da transação: "))
            if opcao == "d":
                cliente_atual.contas[0].depositar(valor)
            elif opcao == "s":
                cliente_atual.contas[0].sacar(valor)

        elif opcao == "e":
            # Exibir extrato
            cliente_atual.contas[0].exibir_extrato()

        elif opcao == "a":
            if cliente_atual and cliente_atual.contas:
                cliente_atual.contas[0].exibir_saldo()
            else:
                print("Nenhum cliente logado ou nenhuma conta associada. Faça login e crie uma conta antes de verificar o saldo.")

        elif opcao == "v":
            # Voltar à tela inicial
            break

        elif opcao == "q":
            print("Saindo do programa. Até logo!")
            break

if __name__ == "__main__":
    main()


