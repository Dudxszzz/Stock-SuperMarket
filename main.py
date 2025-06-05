import pandas as pd
import sqlite3
import os

db = 'estoque.db'

def create_database(db):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estoque(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    codigo INTEGER UNIQUE,
                    preco REAL,
                    quantidade INTEGER,
                    categoria TEXT
                )
            """)
            conn.commit()
            print(f"Tabela {db} criada com sucesso!")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e} (verifique se o banco e a tabela existem)")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")

def insert_database(nome, codigo, preco, quantidade, categoria):
    try:
        with sqlite3.connect(db)as conn:
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO estoque(nome, codigo, preco, quantidade, categoria)
            VALUES(?,?,?,?,?)
            """, (nome, codigo, preco, quantidade, categoria))
            conn.commit()
    except sqlite3.IntegrityError:
        print("Erro: Código do produto já existe no banco de dados.")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")

def interface():
    print()
    print("="*60)
    print(" "*10,"Modelagem de estoque supermarket")
    print("="*60)

    return 0

def cadastro_produto():
    while True:    
        print("\n===== Cadastro de Produto =====\n")
        print("-"*23)
        print("1. Adicionar produto\n2. Voltar ao Menu")
        print("-"*23)

        opcao = input("Escolha uma opção: ")

        if opcao.isdigit():
            opcao = int(opcao)

            if opcao == 1:
                nome_produto = input("Qual é o nome do produto: ").strip().lower()
                try:
                    code_produto = int(input("Qual é o código do produto: "))
                    preco_produto = float(input("Qual é o preço: "))
                    quantidade_produto = int(input("Qual é a quantidade no estoque: "))
                    categoria_produto = input("Em qual categoria: ").lower()

                    insert_database(nome_produto, code_produto, preco_produto, quantidade_produto, categoria_produto)

                except ValueError:
                    print("Erro: Código e quantidade devem ser inteiros, e preço deve ser um número decimal.")
                print(f"Produto {nome_produto} cadastrado com sucesso!\n")
            elif opcao == 2:
                break
            else:
                print("Entrada inválida, Tente novamente.")
        else:
            print("Entrada inválida! Digite um número.")
    return None

def atualiza_estoque():
    while True:
        print("\n====== Atualização de Estoque Produto ======\n")
        print("-"*23)
        print("1. Digite o código do produto\n2. Voltar")
        print("-"*23)
        opcao = int(input("Escolha uma opção: "))
        
        if opcao == 1:
            codigo_produto = input("Digite o código do produto: ")
            nova_quantidade = int(input(f"Qual é a nova quantidade em estoque? "))
            try:
                with sqlite3.connect(db) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE estoque SET quantidade = ? WHERE codigo = ?", (nova_quantidade, codigo_produto))
                    conn.commit()

                    cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (codigo_produto,))
                    produto = cursor.fetchone() #fetchone serve para apenas um resultado

                if produto:
                    print("=== Produto Atualizado! ===")
                    print(f"Nome: {produto[1]}, código: {produto[2]}, Preço: {produto[3]}, Quantidade: {produto[4]}, Categoria: {produto[5]}")
                else:
                    print("Produto não encontrado.")
            except sqlite3.OperationalError as e:
                print(f"Erro operacional: {e} (verifique se o banco e a tabela existem)")
            except sqlite3.Error as e:
                print(f"Erro no banco de dados: {e}")
        elif opcao == 2:
            print("Voltando ao menu principal...\n")
            return
        else:
            print("Entrada inválida! Tente novamente.")

def consulta_produto():
    while True:
        print("\n====== Busca de Produtos ======\n")
        print("-"*23)
        print("1. Consulta por Nome\n2. Consulta por Código\n3. Categoria\n4. Voltar")
        print("-"*23)
        opcao = input("Escolha uma opção: ")

        if opcao.isdigit():
            opcao = int(opcao)

            if opcao == 1:
                nome_produto = input("Digite o nome do produto: ").strip().lower

                with sqlite3.connect(db) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM estoque WHERE nome = ?", (nome_produto,))
                    produtos = cursor.fetchall()

                if produtos:
                    print("===== Produtos Encontrados =====")
                    for produto in produtos:
                        print(f"Nome: {produto[1]}, Código: {produto[2]}, Preço: {produto[3]}, Quantidade: {produto[4]}, Categoria: {produto[5]}")
                else:
                    print("Produto não encontrado.")

            elif opcao == 2:
                codigo_poduto = input("Digite o código do produto: ")

                with sqlite3.connect(db) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (codigo_poduto,))
                    produtos = cursor.fetchall()

                if produtos:
                    print("===== Produtos Encontrados =====")
                    for produto in produtos:
                        print(f"Nome: {produto[1]}, Código: {produto[2]}, Preço: {produto[3]}, Quantidade: {produto[4]}, Categoria: {produto[5]}")
                else:
                    print("Produtos não encontrado.")

            elif opcao == 3:
                categoria_produto = input("Qual é a categoria do produto: ").lower()

                with sqlite3.connect(db) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM estoque WHERE categoria = ?", (categoria_produto,))
                    produtos = cursor.fetchall()

                if produtos:
                    print("===== Produtos Encontrados =====")
                    for produto in produtos:
                        print(f"Nome: {produto[1]}, Código: {produto[2]}, Preço: {produto[3]}, Quantidade: {produto[4]}, Categoria: {produto[5]}")
                else:
                    print("Produtos não encontrados.")

            elif opcao == 4:
                print("Voltando ao menu principal...\n")
                return

            else:
                print("Entrada inválida! Tente novamente.")
        else:
            print("Entrada inválida! Digite um número.")
            
def produtos():
    print()
    print("="*60)
    print(" "*10, "ESTOQUE SUPERMARKET")
    print("="*60,"\n")
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM estoque")
            produtos = cursor.fetchall()

        if produtos:
            for produto in produtos:
                print(f"ID: {produto[0]}, Nome: {produto[1]}, Codigo: {produto[2]}, Preço: {produto[3]}, Quantidade: {produto[4]}, Categoria: {produto[5]}")
        else:
            print("\nNenhum produto cadastrado ainda!")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e} (verifique se o banco e a tabela existem)")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")

def planilha(estoque):
    print("Criando planilha...")
    try:
        with sqlite3.connect(db) as conn:
            sql = "SELECT * FROM estoque"
            df = pd.read_sql(sql, conn)

            df.rename(columns={
                "id": "ID",
                "nome": "Nome",
                "codigo": "Código",
                "preco": "Preço",
                "quantidade": "Quantidade",
                "categoria": "Categoria"
            }, inplace=True)

            df.to_excel(estoque, index=False)

    except sqlite3.OperationalError as e:
        print(f"Erro operacional : {e} (Verificar se tabela existe)")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")


def main():
    estoque = 'estoque.xlsx'
    create_database(db)

    while True:
        interface()
        print("")
        print("-"*23)
        print("1. Cadastrar Produto\n2. Atualizar Estoque\n3. Consulta de produtos\n4. Produtos\n5. Criar Planilha\n6. Sair")
        print("-"*23)

        opcao = input("Escolha uma opção: ")
        
        if opcao.isdigit():
            opcao = int(opcao)

            if opcao == 1:
                cadastro_produto()
            elif opcao == 2:
                atualiza_estoque()
            elif opcao == 3:
                consulta_produto()
            elif opcao == 4:
                produtos()
            elif opcao == 5:
                planilha(estoque)
            elif opcao == 6:
                print("Fechando supermarket...")
                break
            else:
                print("Entrada inválida, Tente novamente.")
        else:
            print("Entrada inválida! Digite um número.")
    
if __name__ == "__main__":
    main()