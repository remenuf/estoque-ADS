import sqlite3
import database

functions = {
    1: database.registrar_produto,
    2: database.atualizar_estoque,
    3: database.listar_produtos,
    4: database.buscar_produto,
    5: database.editar_produto_prompt,
    6: database.remover_produto,
    7: database.gerar_relatorio,
}


def mostrar_menu():
    print("\n--- Bem-Vindo ---")
    print("Escolha a sua operação:")
    print("1. Registrar produto")
    print("2. Atualizar estoque de um produto")
    print("3. Listar produtos")
    print("4. Buscar produto")
    print("5. Editar produto")
    print("6. Remover produto")
    print("7. Gerar relatório de produtos")
    print("0. Sair")

while True:
    mostrar_menu()
    opcao = int(input("Escolha uma opção: "))
    if opcao in (1, 2, 3, 4, 5, 6, 7):  # Check if opcao is within the valid range
        functions[opcao]()
    elif opcao == 0:
        break
    else:
        print("Opção inválida!") 
