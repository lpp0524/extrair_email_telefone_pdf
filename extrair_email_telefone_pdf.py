import PyPDF2
import re
import mysql.connector
from mysql.connector import Error

# Tentar conectar ao banco de dados
try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sua_senha",
        database="db_contatos"
    )

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão", db_info)
        cursor = con.cursor()
        cursor.execute("SELECT DATABASE();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados", linha)

        # Ler o arquivo PDF
        pdf_file = r"Caminho/Para/Seu/dados.pdf"

        try:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            page = read_pdf.getPage(0)
            dados = page.extractText()
        except Exception as e:
            print("Erro ao ler o arquivo PDF:", e)
            con.close()
            exit()

        # Extrair email e telefone usando regex
        email_match = re.findall(r'[\w\.-]+@[\w\.-]+', dados)
        email = str(email_match[0]) if email_match else None

        telefone_match = re.findall(r'\(\d+\)[ ]?\d+[-. ]?\d+', dados)
        telefone = str(telefone_match[0]) if telefone_match else None

        # Inserir dados no banco de dados
        if email and telefone:
            try:
                cursor.execute(f"INSERT INTO db_contatos.tbl_contatos (tbl_telefone, tbl_email) VALUES ('{telefone}', '{email}')")
                con.commit()
                print("Dados inseridos com sucesso!")
            except Error as e:
                print("Erro ao inserir dados no banco de dados:", e)
        else:
            print("Dados de email ou telefone não encontrados no PDF.")

        # Fechar a conexão com o banco de dados
        cursor.close()
        con.close()
        print("Conexão encerrada.")

except Error as e:
    print("Erro ao conectar ao MySQL:", e)
