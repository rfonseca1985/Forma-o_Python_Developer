Sistema Bancário - README
Este é um projeto de um Sistema Bancário implementado em Python, utilizando o paradigma de orientação a objetos. O sistema modela diversas entidades relacionadas a operações bancárias, proporcionando uma estrutura robusta e extensível.

Classes Principais
Transacao
Classe abstrata que define um contrato para transações bancárias.
Implementada pelas classes concretas Saque e Deposito, que encapsulam a lógica associada a saques e depósitos.
PessoaFisica
Representa uma pessoa física com atributos como nome, CPF e data de nascimento.
Cliente
Herda de PessoaFisica e representa um cliente bancário.
Contém uma lista de contas associadas ao cliente.
Permite realizar transações por meio do método realizar_transacao.
Historico
Armazena o histórico de transações de uma conta.
Conta
Representa uma conta bancária comum, com atributos como número, agência, cliente e saldo.
Possui um histórico de transações.
ContaCorrente
Herda de Conta e representa uma conta corrente.
Adiciona características específicas de contas correntes, como limite de saque e limite diário de saques.
Funcionalidades Principais
Depositar: Realiza depósitos na conta.
Sacar: Realiza saques, respeitando limites de saque diário e limite da conta corrente.
Extrato: Exibe o histórico de transações da conta.
Saldo: Exibe o saldo atual da conta.
Uso do Sistema
Ao iniciar o programa, é possível acessar uma conta existente informando agência e conta separados por espaço.
Para criar uma nova conta, digite 'c' no início e siga as instruções para fornecer dados do cliente.
O sistema oferece um menu com opções para depositar, sacar, ver extrato, verificar saldo, voltar à tela inicial ou sair.
Este projeto adota os princípios da orientação a objetos, proporcionando um código modular, extensível e de fácil compreensão. As classes fornecem uma estrutura clara e hierárquica, permitindo a expansão do sistema com facilidade.
