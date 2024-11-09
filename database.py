from tinydb import TinyDB, Query
import datetime

# Set up TinyDB and create a database file named "estoque.json"
db = TinyDB('estoque.json')
produtos = db.table('produtos')  # Define a table within the TinyDB database

def print_produto(produto):
    print(f"ID: {produto.doc_id} | Nome: {produto['nome']} | Categoria: {produto['categoria']} | Estoque: {produto['quantidade']} | Preço: {produto['preco']:.2f} | Localização: {produto['localizacao']} | Estoque ideal: {produto['estoque_ideal']}")

def check_name(name):
    produto = Query()
    resultado = produtos.search(produto.nome.test(lambda x: name.lower() in x.lower()))
    if resultado:
        return True
    return False

def registrar_produto():
    nome = input("Nome do produto: ")

    if check_name(nome):
        print("Produto com este nome já registrado!")
        print("Deseja registrar outro produto? (s/n)")
        opcao = input("Escolha uma opção: ")
        while (opcao != 's' and opcao != 'n'):
            print("Opção inválida!")
            opcao = input("Escolha uma opção: ")
        if opcao == 's':
            registrar_produto()
        return

    categoria = input("Categoria: ")
    quantidade = int(input("Quantidade: "))
    estoque_ideal = int(input("Estoque ideal: "))
    preco = float(input("Preço: ").replace(",", "."))
    localizacao = input("Localização: ")
    movimentacoes = []

    # Insert product into TinyDB
    produto = {
        "nome": nome,
        "categoria": categoria,
        "quantidade": quantidade,
        "estoque_ideal": estoque_ideal,
        "preco": preco,
        "localizacao": localizacao,
        "movimentacoes": movimentacoes
    }
    produtos.insert(produto)
    print("Produto registrado com sucesso!")

def atualizar_estoque():
    id = int(input("ID do produto a ser atualizado: "))

    produto = produtos.get(doc_id=id)
    if not produto:
        print("Produto não encontrado.")
        return

    print("--------------------------------- PRODUTO ---------------------------------")
    print_produto(produto)
    print("---------------------------------------------------------------------------")

    print("\nVocê deseja:")
    print("1. Adicionar ao estoque")
    print("2. Subtrair do estoque")
    opcao = int(input("Escolha uma opção: "))

    while (opcao != 1 and opcao != 2):
        print("Opção inválida!")
        print("1. Adicionar ao estoque")
        print("2. Subtrair do estoque")
        opcao = int(input("Escolha uma opção: "))

    nova_quantidade = int(input("Quantidade: "))

    # Adjust quantity based on option
    if opcao == 2:
        nova_quantidade = -nova_quantidade
        if produto["quantidade"] + nova_quantidade < 0:
            print("Estoque insuficiente!")
            return


    # Get the current date and time
    data_hora_movimentacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the movement record
    movimentacao = {
        "data_hora": data_hora_movimentacao,
        "quantidade_anterior": produto["quantidade"],
        "quantidade_alterada": nova_quantidade,
        "quantidade_final": produto["quantidade"] + nova_quantidade
    }

    # Update product quantity and add movement record
    produtos.update(lambda doc: doc.update({
        "quantidade": doc["quantidade"] + nova_quantidade,
        "movimentacoes": doc["movimentacoes"] + [movimentacao]
    }), doc_ids=[id])

    produto = produtos.get(doc_id=id)

    print("--------------------------------- PRODUTO ---------------------------------")
    print_produto(produto)
    print("Estoque atualizado com sucesso!")
    print("---------------------------------------------------------------------------")


def listar_produtos():
    produtos_ordenados = produtos.all()
    print("--------------------------------- PRODUTOS ---------------------------------")
    for produto in produtos_ordenados:
        print_produto(produto)
    print("----------------------------------------------------------------------------")


def buscar_produto():
    print("\nVocê deseja:")
    print("1. Buscar por ID")
    print("2. Buscar por Nome")
    opcao = int(input("Escolha uma opção: "))

    while (opcao != 1 and opcao != 2):
        print("Opção inválida!")
        print("1. Buscar por ID")
        print("2. Buscar por Nome")
        opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        id = int(input("ID do produto: "))
        while (id < 0):
            print("ID inválido!")
            id = int(input("ID do produto: "))
        produto = produtos.get(doc_id=id)
        print("--------------------------------- PRODUTO ---------------------------------")
        print_produto(produto)
        print("---------------------------------------------------------------------------")
    else:
        nome = input("Nome do produto: ")
        produto = Query()
        resultado = produtos.search(produto.nome.test(lambda x: nome.lower() in x.lower()))
        
        if resultado:
            print("--------------------------------- PRODUTOS ENCONTRADOS ---------------------------------")
            for produto in resultado:
                print_produto(produto)
            print("----------------------------------------------------------------------------------------")
        else:
            print("Produto não encontrado.")    

def editar_produto_prompt():
    id = int(input("ID do produto a ser editado: "))
    produto = produtos.get(doc_id=id)
    if not produto:
        print("Produto não encontrado.")
        return

    editar_produto(produto)

def editar_produto(produto):
    id = produto.doc_id

    def print_options():
        print("1. Nome")
        print("2. Categoria")
        print("4. Estoque ideal")
        print("5. Preço")
        print("6. Localização")

    def change_name():
        novo_nome = input("Novo nome: ")

        while check_name(novo_nome):
            print("Produto com este nome já registrado!")
            novo_nome = input("Escolha outro nome: ")

        produtos.update({"nome": novo_nome}, doc_ids=[id])

    def change_category():
        nova_categoria = input("Nova categoria: ")
        produtos.update({"categoria": nova_categoria}, doc_ids=[id])

    def change_estoque_ideal():
        novo_estoque_ideal = int(input("Novo estoque ideal: "))
        produtos.update({"estoque_ideal": novo_estoque_ideal}, doc_ids=[id])

    def change_preco():
        novo_preco = float(input("Novo preço: ").replace(",", "."))
        produtos.update({"preco": novo_preco}, doc_ids=[id])

    def change_localizacao():
        nova_localizacao = input("Nova localização: ")
        produtos.update({"localizacao": nova_localizacao}, doc_ids=[id])

    options = {
        1: change_name,
        2: change_category,
        4: change_estoque_ideal,
        5: change_preco,
        6: change_localizacao
    }

    produto = produtos.get(doc_id=id)
    print("--------------------------------- PRODUTO ---------------------------------")
    print_produto(produto)
    print("---------------------------------------------------------------------------")
    print("\nSelecione o campo que deseja editar:")
    print_options()
    opcao = int(input("Escolha uma opção: "))

    while (opcao < 1 or opcao > 6):
        print("Opção inválida!")
        print_options()
        opcao = int(input("Escolha uma opção: "))

    
    options[opcao]()
    print("Produto editado com sucesso!")
    print("Deseja editar outro campo? (s/n)")
    opcao = input("Escolha uma opção: ")
    while (opcao != 's' and opcao != 'n'):
        print("Opção inválida!")
        opcao = input("Escolha uma opção: ")
    if opcao == 's':
        editar_produto(produto)
    else:
        print("Deseja editar outro produto? (s/n)")
        opcao = input("Escolha uma opção: ")
        while (opcao != 's' and opcao != 'n'):
            print("Opção inválida!")
            opcao = input("Escolha uma opção: ")
        if opcao == 's':
            editar_produto_prompt()
        else:
            return

def remover_produto():
    id = int(input("ID do produto a ser atualizado: "))

    produto = produtos.get(doc_id=id)
    if not produto:
        print("Produto não encontrado.")
        return

    print(f'Tem certeza que quer excluir "{produto['nome']}"? (s/n)')
    opcao = input("Escolha uma opção: ")
    while (opcao != 's' and opcao != 'n'):
        print("Opção inválida!")
        opcao = input("Escolha uma opção: ")
    if opcao == 's':
        produtos.remove(doc_ids=[id])
        print("Produto removido com sucesso!")
    else:
        return

def check_stock(product):
    if product['estoque_ideal'] == 0:
        return 0

    difference = ((product['quantidade'] - product['estoque_ideal']) / product['estoque_ideal']) * 100

    if abs(difference) >= 30:
        if difference < 0 : args = 'abaixo'
        else : args = 'acima'
        print(f'\nO estoque de "{product['nome']}" está {abs(difference):.2f}% {args} do valor ideal.')
    else:
        print(f'\nO estoque de "{product['nome']}" está dentro do valor ideal.')

def report_manifest(product):
    print(f"\n------------------------------ MOVIMENTAÇÕES DE {product['nome'].upper()} ------------------------------\n")
    if len(product['movimentacoes']) > 0:
        for i, mov in enumerate(product['movimentacoes']):
            print(f"Movimentação {i+1}:")
            print(f"  Data e Hora: {mov['data_hora']}")
            print(f"  Quantidade Inicial: {mov['quantidade_anterior']}")
            print(f"  Quantidade Alterada: {mov['quantidade_alterada']}")
            print(f"  Quantidade Final: {mov['quantidade_final']}")
            print("----------------------------------------------------")
    else:
        print(f"Nenhuma movimentação registrada para {product['nome']}.\n") 
    
def gerar_relatorio():
    def relatorio_produto(id=None):
        flag = False
        if not id:
            id = int(input("ID do produto a ser reportado: "))
            flag = True
        produto = produtos.get(doc_id=id)
        if not produto:
            print("Produto não encontrado.")
            relatorio_produto()

        print(f"\n------------------------------ RELATÓRIO DE {produto['nome'].upper()} ------------------------------\n")
        print_produto(produto)
        check_stock(produto)
        report_manifest(produto)
        print("----------------------------------------------------------------------------------------")
            
    def relatorio_categoria():
        categoria_desejada = input("Digite a categoria a ser reportada: ")
        categoria_query = Query()
        produtos_categoria = produtos.search(categoria_query.categoria.test(lambda x: x.lower() == categoria_desejada.lower()))
        if produtos_categoria:
            print(f"\n--------------------------------- RELATÓRIO DA CATEGORIA: {categoria_desejada.upper()} ---------------------------------\n")
            for produto in produtos_categoria:
                relatorio_produto(produto.doc_id)
        else:
            print(f"Nenhum produto encontrado na categoria '{categoria_desejada}'.")
        

    def relatorio_estoque():
        print("\n--------------------------------- RELATÓRIO DE TODO O ESTOQUE ---------------------------------\n")
        for produto in produtos.all():
            relatorio_produto(produto.doc_id)

    relatorios = {
        1: relatorio_produto,
        2: relatorio_categoria,
        3: relatorio_estoque
    }

    print("Escolha o tipo de relatório desejado:")
    print("1. Relatório de um Produto")
    print("2. Relatório de uma Categoria")
    print("3. Relatório de todo o estoque")
    opcao = int(input("Escolha uma opção: "))
    while (opcao < 1 or opcao > 3):
        print("Opção inválida!")
        opcao = int(input("Escolha uma opção: "))

    relatorios[opcao]()

    print("Deseja gerar outro relatório? (s/n)")
    opcao = input("Escolha uma opção: ")
    while (opcao != 's' and opcao != 'n'):
        print("Opção inválida!")
        opcao = input("Escolha uma opção: ")
    if opcao == 's':
        gerar_relatorio()
    else:
        return
