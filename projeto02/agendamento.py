import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configurando o banco de dados
conn = sqlite3.connect("agendamentos.db")
cursor = conn.cursor()

# Criar a tabela de clientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT,
    endereco TEXT
)
''')

# Criar a tabela de agendamentos
cursor.execute('''
CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    analises TEXT NOT NULL,
    valor_total REAL NOT NULL,
    status TEXT DEFAULT 'Pendente',
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
''')

# Criar a tabela de estoque
cursor.execute('''
CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    quantidade INTEGER NOT NULL
)
''')

# Constantes e configurações
ANALISES = {
    "coliformes": 50.0,
    "ph": 20.0,
    "dureza": 30.0,
    "alcalinidade": 25.0
}

LIMITE_DIARIO = 10  # Limite de agendamentos diários


# Funções principais
def verificar_disponibilidade(data):
    cursor.execute("SELECT COUNT(*) FROM agendamentos WHERE data = ?", (data,))
    agendados = cursor.fetchone()[0]
    return agendados < LIMITE_DIARIO


def calcular_valor_total(analises):
    return sum(ANALISES[a] for a in analises)


def instrucoes(data, analises):
    dia_semana = datetime.strptime(data, "%Y-%m-%d").strftime("%A")
    if "coliformes" in analises and dia_semana not in ["Monday", "Tuesday"]:
        return "Análises de coliformes só podem ser entregues às segundas e terças-feiras."
    return "Amostras podem ser entregues no dia agendado das 8h às 17h."


def cadastrar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    cursor.execute(
        "INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?)",
        (nome, email, telefone, endereco)
    )
    conn.commit()
    messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado com sucesso!")


def agendar():
    cliente_id_str = entry_cliente_id.get()

    # Verificar se o campo de ID do cliente está vazio ou contém um valor inválido
    if not cliente_id_str.isdigit():
        messagebox.showerror("Erro", "Por favor, insira um ID válido do cliente.")
        return

    cliente_id = int(cliente_id_str)

    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()

    if not cliente:
        messagebox.showerror("Erro", "Cliente não encontrado!")
        return

    data = entry_data.get()

    if not verificar_disponibilidade(data):
        messagebox.showerror("Erro", "Não há mais vagas disponíveis para esta data.")
        return

    analises = entry_analises.get().split(",")
    analises = [a.strip() for a in analises if a.strip() in ANALISES]

    if not analises:
        messagebox.showerror("Erro", "Nenhuma análise válida selecionada.")
        return

    valor_total = calcular_valor_total(analises)
    instrucoes_agendamento = instrucoes(data, analises)

    messagebox.showinfo("Instruções", instrucoes_agendamento)
    confirmar = messagebox.askyesno("Confirmar Agendamento", f"Valor total: R${valor_total:.2f}\nDeseja confirmar o agendamento?")

    if confirmar:
        try:
            cursor.execute(
                "INSERT INTO agendamentos (cliente_id, data, analises, valor_total) VALUES (?, ?, ?, ?)",
                (cliente_id, data, ", ".join(analises), valor_total)
            )
            conn.commit()
            gerar_pdf_agendamento(cliente, data, analises, valor_total, instrucoes_agendamento)
            messagebox.showinfo("Sucesso", "Agendamento realizado com sucesso!")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao inserir no banco: {e}")
            messagebox.showerror("Erro de Banco de Dados", "Ocorreu um erro ao realizar o agendamento.")
    else:
        messagebox.showinfo("Cancelado", "Agendamento cancelado.")


def listar_agendamentos():
    cursor.execute('''
    SELECT agendamentos.id, clientes.nome, agendamentos.data, agendamentos.analises, agendamentos.valor_total, agendamentos.status
    FROM agendamentos
    JOIN clientes ON agendamentos.cliente_id = clientes.id
    ''')
    agendamentos = cursor.fetchall()

    if not agendamentos:
        messagebox.showinfo("Sem agendamentos", "Nenhum agendamento encontrado.")
        return

    agendamentos_str = "\n".join([f"ID: {agendamento[0]} | Cliente: {agendamento[1]} | Data: {agendamento[2]} | "
                                 f"Análises: {agendamento[3]} | Valor: R${agendamento[4]:.2f} | Status: {agendamento[5]}"
                                 for agendamento in agendamentos])
    messagebox.showinfo("Agendamentos", agendamentos_str)


def listar_clientes():
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    if not clientes:
        messagebox.showinfo("Sem clientes", "Nenhum cliente cadastrado.")
        return

    clientes_str = "\n".join([f"ID: {cliente[0]} | Nome: {cliente[1]} | E-mail: {cliente[2]}" for cliente in clientes])
    messagebox.showinfo("Clientes", clientes_str)


# Função para gerar o PDF com as instruções
def gerar_pdf_agendamento(cliente, data, analises, valor_total, instrucoes):
    c = canvas.Canvas(f"Agendamento_{cliente[1]}_{data}.pdf", pagesize=letter)
    c.drawString(100, 750, f"Cliente: {cliente[1]}")
    c.drawString(100, 730, f"E-mail: {cliente[2]}")
    c.drawString(100, 710, f"Telefone: {cliente[3]}")
    c.drawString(100, 690, f"Endereço: {cliente[4]}")
    c.drawString(100, 670, f"Data do Agendamento: {data}")
    c.drawString(100, 650, f"Análises: {', '.join(analises)}")
    c.drawString(100, 630, f"Valor Total: R${valor_total:.2f}")
    c.drawString(100, 610, f"Instruções: {instrucoes}")

    c.save()
    messagebox.showinfo("PDF Gerado", f"PDF do agendamento de {cliente[1]} gerado com sucesso!")


# Função para dar baixa no agendamento (concluir ou cancelar)
def dar_baixa_agendamento():
    agendamento_id_str = entry_agendamento_id.get()

    # Verificar se o campo de ID do agendamento está vazio ou contém um valor inválido
    if not agendamento_id_str.isdigit():
        messagebox.showerror("Erro", "Por favor, insira um ID válido do agendamento.")
        return

    agendamento_id = int(agendamento_id_str)

    cursor.execute("SELECT * FROM agendamentos WHERE id = ?", (agendamento_id,))
    agendamento = cursor.fetchone()

    if not agendamento:
        messagebox.showerror("Erro", "Agendamento não encontrado!")
        return

    novo_status = entry_status.get()

    if novo_status not in ["Concluído", "Cancelado"]:
        messagebox.showerror("Erro", "Status inválido! Escolha 'Concluído' ou 'Cancelado'.")
        return

    cursor.execute(
        "UPDATE agendamentos SET status = ? WHERE id = ?",
        (novo_status, agendamento_id)
    )
    conn.commit()

    messagebox.showinfo("Sucesso", f"Agendamento ID {agendamento_id} atualizado para {novo_status}!")


# Função para controlar o estoque (aumentar ou diminuir a quantidade)
def atualizar_estoque():
    item = entry_item.get()
    quantidade_str = entry_quantidade.get()

    # Verificar se a quantidade é um número válido
    if not quantidade_str.isdigit():
        messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
        return

    quantidade = int(quantidade_str)

    cursor.execute("SELECT * FROM estoque WHERE item = ?", (item,))
    estoque_item = cursor.fetchone()

    if not estoque_item:
        cursor.execute("INSERT INTO estoque (item, quantidade) VALUES (?, ?)", (item, quantidade))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Item {item} adicionado ao estoque com {quantidade} unidades.")
    else:
        nova_quantidade = estoque_item[2] + quantidade
        cursor.execute("UPDATE estoque SET quantidade = ? WHERE item = ?", (nova_quantidade, item))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Estoque do item {item} atualizado para {nova_quantidade} unidades.")


# Interface gráfica
root = Tk()
root.title("Sistema de Agendamento")

# Entrada de dados para cadastro de clientes
Label(root, text="Nome:").grid(row=0, column=0)
entry_nome = Entry(root)
entry_nome.grid(row=0, column=1)

Label(root, text="E-mail:").grid(row=1, column=0)
entry_email = Entry(root)
entry_email.grid(row=1, column=1)

Label(root, text="Telefone:").grid(row=2, column=0)
entry_telefone = Entry(root)
entry_telefone.grid(row=2, column=1)

Label(root, text="Endereço:").grid(row=3, column=0)
entry_endereco = Entry(root)
entry_endereco.grid(row=3, column=1)

Button(root, text="Cadastrar Cliente", command=cadastrar_cliente).grid(row=4, columnspan=2)

# Entrada de dados para agendamento
Label(root, text="ID Cliente:").grid(row=5, column=0)
entry_cliente_id = Entry(root)
entry_cliente_id.grid(row=5, column=1)

Label(root, text="Data (YYYY-MM-DD):").grid(row=6, column=0)
entry_data = Entry(root)
entry_data.grid(row=6, column=1)

Label(root, text="Análises (coliformes, ph, dureza, alcalinidade):").grid(row=7, column=0)
entry_analises = Entry(root)
entry_analises.grid(row=7, column=1)

Button(root, text="Agendar Análise", command=agendar).grid(row=8, columnspan=2)

# Entrada de dados para dar baixa no agendamento
Label(root, text="ID Agendamento:").grid(row=9, column=0)
entry_agendamento_id = Entry(root)
entry_agendamento_id.grid(row=9, column=1)

Label(root, text="Status (Concluído/Cancelado):").grid(row=10, column=0)
entry_status = Entry(root)
entry_status.grid(row=10, column=1)

Button(root, text="Dar Baixa no Agendamento", command=dar_baixa_agendamento).grid(row=11, columnspan=2)

# Entrada de dados para controle de estoque
Label(root, text="Item:").grid(row=12, column=0)
entry_item = Entry(root)
entry_item.grid(row=12, column=1)

Label(root, text="Quantidade:").grid(row=13, column=0)
entry_quantidade = Entry(root)
entry_quantidade.grid(row=13, column=1)

Button(root, text="Atualizar Estoque", command=atualizar_estoque).grid(row=14, columnspan=2)

# Botões para listar clientes e agendamentos
Button(root, text="Listar Clientes", command=listar_clientes).grid(row=15, column=0)
Button(root, text="Listar Agendamentos", command=listar_agendamentos).grid(row=15, column=1)

root.mainloop()
