import hashlib
import json
import sys


def catalogo_paciente():
    print("-------Lista de Pacinetes-------\n\n")
    catalog = []

    def carregar_paciente():
        try:
            with open("lista_paciente.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Erro ao carregar o arquivo JSON. O conteúdo pode estar corrompido.")
            return []
    # salvar pacientes na lista


    def salvar_catalogo(catalog):
        with open("lista_paciente.json", 'w') as file:
            json.dump(catalog, file)
            
# Adicionar pacientes na lista

    def adicionar_paciente(nome, periodo, curso, dataDaUltimaConsulta,
                        email, telefone, observacoes, links):
        paciente = {
            'nome': nome,
            'periodo': periodo,
            'curso': curso,
            'dataDaUltimaConsulta': dataDaUltimaConsulta,
            'email': email,
            'telefone': telefone,
            'observacoes': observacoes,
            'links': links
        }
        catalog.append(paciente)
        salvar_catalogo(catalog)
        print('A lista de pacientes está vazia.')
    #listar os pacientes    
    def listar_paciente():
        if not catalog:
            print('A lista de pacientes está vazia')
        else:
            for i, paciente in enumerate(catalog, start=1):
                print(f"Paciente {i}:")
                print(f"Nome: {paciente['nome']}")
                print(f"Período: {paciente['periodo']}")
                print(f"Curso: {paciente['curso']}")
                print(f"Data da Última Consulta: {paciente['dataDaUltimaConsulta']}")
                print(f"Email: {paciente['email']}")
                print(f"Telefone: {paciente['telefone']}")
                print(f"Observações: {paciente['observacoes']}")
                print(f"Links: {paciente['links']}\n")
                
    #excluir paciente da lista            
    def excluir_paciente(indice):
        if 0 < indice <= len(catalog):
            catalog.pop(indice - 1)
            salvar_catalogo(catalog)
            print("Paciente removido com sucesso.")
        else:
            print("Índice inválido. Nenhum paciente foi removido.")
    
    #main
    catalog = carregar_paciente()
    
    while True:
        print("1. Mostrar paciente")
        print("2. Adicionar pacinete")
        print("3. Atualizar paciente")
        print("4. Excluir paciente")
        print("0. Voltar para o menu")
        
        opcao = input ('Escolha uma opção: ')

        if opcao == '1':
            listar_paciente()
        if opcao == '2':
            nome = input("Nome: ")
            periodo = input("Período: ")
            curso = input("Curso: ")
            dataDaUltimaconsulta = input("Data da Ultima Consulta: ")
            email = input("Email: ")
            telefone = input('Telefone: ')
            observacoes = input('Observações: ')
            links = input('Links: ')
            adicionar_paciente(nome, periodo, curso, dataDaUltimaconsulta, email, telefone, observacoes, links)
        if opcao == '3':
            listar_paciente()
            indice = int(input("Digite o indice do paciente a ser editado: "))
            nome = input("Nome: ")
            periodo = input("Período: ")
            curso = input("Curso: ")
            dataDaUltimaconsulta = input("Data da Ultima Consulta: ")
            email = input("Email: ")
            telefone = input('Telefone: ')
            observacoes = input('Observações: ')
            links = input('Links: ')
        if opcao == '4':
            listar_paciente()
            indice = int(input("Digite o indice do animal a ser removido: "))
            excluir_paciente(indice)
        else:
            print("Opção inválida. Tente novamente.")
            

            
catalogo_paciente()

#teste commit