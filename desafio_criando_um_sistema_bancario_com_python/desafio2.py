menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar Conta
[u] Criar Usuário
[a] Saldo
[q] Sair

=> """

usuarios = {}
contas_correntes = {}
numero_conta = 1  # Contador global para gerar números de conta únicos
LIMITE_SAQUES = 3  # Adicionando a definição da constante

class Usuario:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco

class ContaCorrente:
    def __init__(self, usuario):
        global numero_conta
        self.numero_conta = numero_conta
        numero_conta += 1
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.saques = 0
        self.usuario = usuario

def depositar(conta):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        conta.saldo += valor
        conta.extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito realizado com sucesso na conta {conta.numero_conta} de {conta.usuario.nome}.")
        print(f"Saldo atual da conta {conta.numero_conta}: R$ {conta.saldo:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar(conta):
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > conta.saldo
    excedeu_limite = valor > conta.limite
    excedeu_saques = conta.saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        conta.saldo -= valor
        conta.extrato += f"Saque: R$ {valor:.2f}\n"
        conta.saques += 1
        print(f"Saque realizado com sucesso na conta {conta.numero_conta} de {conta.usuario.nome}.")
        print(f"Saldo atual da conta {conta.numero_conta}: R$ {conta.saldo:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta.extrato else conta.extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

def criar_conta():
    nome = input("Informe o nome do usuário: ")
    cpf = input("Informe o CPF do usuário: ")
    endereco = input("Informe o endereço do usuário: ")

    if cpf in usuarios:
        print("Usuário já existe.")
        return

    usuario = Usuario(nome, cpf, endereco)
    usuarios[cpf] = usuario
    conta = ContaCorrente(usuario)
    contas_correntes[conta.numero_conta] = conta

    print(f"Conta corrente criada para o usuário {usuario.nome} com CPF {cpf} e número de conta {conta.numero_conta}.")
    print(f"Saldo atual da conta {conta.numero_conta}: R$ {conta.saldo:.2f}")

def criar_usuario():
    nome = input("Informe o nome do usuário: ")
    cpf = input("Informe o CPF do usuário: ")
    endereco = input("Informe o endereço do usuário: ")

    if cpf in usuarios:
        print("Usuário já existe.")
        return

    usuario = Usuario(nome, cpf, endereco)
    usuarios[cpf] = usuario
    conta = ContaCorrente(usuario)
    contas_correntes[conta.numero_conta] = conta

    print(f"Usuário criado com sucesso: {usuario.nome} com CPF {cpf} e número de conta {conta.numero_conta}.")
    print(f"Saldo atual da conta {conta.numero_conta}: R$ {conta.saldo:.2f}")

def verificar_saldo():
    numero_conta = int(input("Informe o número da conta: "))
    if numero_conta in contas_correntes:
        conta = contas_correntes[numero_conta]
        print(f"\nSaldo atual da conta {numero_conta} de {conta.usuario.nome}: R$ {conta.saldo:.2f}")
    else:
        print("Conta não encontrada.")

while True:
    opcao = input(menu)

    if opcao == "d":
        numero_conta = int(input("Informe o número da conta: "))
        if numero_conta in contas_correntes:
            depositar(contas_correntes[numero_conta])
        else:
            print("Conta não encontrada.")
    elif opcao == "s":
        numero_conta = int(input("Informe o número da conta: "))
        if numero_conta in contas_correntes:
            sacar(contas_correntes[numero_conta])
        else:
            print("Conta não encontrada.")
    elif opcao == "e":
        numero_conta = int(input("Informe o número da conta: "))
        if numero_conta in contas_correntes:
            exibir_extrato(contas_correntes[numero_conta])
        else:
            print("Conta não encontrada.")
    elif opcao == "c":
        criar_conta()
    elif opcao == "u":
        criar_usuario()
    elif opcao == "a":
        verificar_saldo()
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

