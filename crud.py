
#CRUD
import psycopg2

class AppBD:
    def __init__(self):
        print('Método Construtor')

    def abrirconexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                               password="1234",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="postgres")
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)

    # todos os produtos
    @property
    def selecionarDados(self):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            print("Selecionando todos os produtos")
            sql_select_query = """select * from public.PRODUTO """
            cursor.execute(sql_select_query)
            registros = cursor.fetchall()
            print(registros)
        except (Exception, psycopg2.Error) as error:
            print("Error in select operation", error)
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("conexão com PostgreSQL finalizada.")
        return registros


    # Inserir Produto

    def inserirDados(self, codigo, nome, preco, precovenda):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO PRODUTO 
          (codigo, NOME, PRECO, precovenda) VALUES (%s,%s,%s,%s)"""
            record_to_insert = (codigo, nome, preco, precovenda)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com successo na tabela PRODUTO")
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print("Falha ao inserir registro na tabela PRODUTO", error)
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("conexão com PostgreSQL finalizada.")

    # atualizar prod

    def atualizarDados(self, codigo, nome, preco, precovenda):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            print("Registro antes da atualização ")
            sql_select_query = """select * from public.PRODUTO 
            where CODIGO = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)
            #atualizar reg
            sql_update_query = """Update public.PRODUTO set NOME = %s, 
            PRECO = %s
             where CODIGO = %s"""
            cursor.execute(sql_update_query, (nome, preco, codigo))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "O registro foi atualizado.")
            print("Registro após atualização ")
            sql_select_query = """select * from public.PRODUTO 
            where CODIGO = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)
        except (Exception, psycopg2.Error) as error:
            print("Erro de atualização.", error)
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com PostgreSQL foi finalizada.")

    #excluir produto
    def excluirDados(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            #atualizar reg

            sql_delete_query = """Delete from public.PRODUTO 
            where CODIGO = %s"""
            cursor.execute(sql_delete_query, (codigo,))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "O registro foi excluído.")
        except (Exception, psycopg2.Error) as error:
            print("Erro de exclusão", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi finalizada.")

