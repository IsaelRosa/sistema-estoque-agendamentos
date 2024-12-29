import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

cliente_agendado = None
data_agendada = None
analises_agendadas = []
valor_total_agendado = 0.0
instrucoes_agendamento = ""

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('estoque_agendamentos.db')
cursor = conn.cursor()

# Função para validar a data
def validar_data(data):
    try:
        datetime.strptime(data, "%Y-%m-%d")
        return True
    except ValueError:
        return False
def listar_clientes():
    for i in tree_clientes.get_children():
        tree_clientes.delete(i)
    
    cursor.execute("SELECT id, nome FROM clientes")
    for row in cursor.fetchall():
        tree_clientes.insert('', 'end', values=row)    

# Criando as tabelas necessárias no banco de dados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        quantidade INTEGER,
        data_validade DATE,
        fornecedor TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT,
        endereco TEXT
    )
''')

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

# Constantes e configurações
ANALISES = {
    "coliformes": 50.0,
    "ph": 20.0,
    "dureza": 30.0,
    "alcalinidade": 25.0
}
# Função para atualizar as análises e valores
def atualizar_analises():
    for analise, valor in ANALISES.items():
        lista_analises.insert(tk.END, f"{analise.capitalize()}: R${valor:.2f}")

# Função para exibir a instrução e valores da análise selecionada
def exibir_valor_analise():
    analise_selecionada = combo_analises.get()
    if analise_selecionada in ANALISES:
        valor = ANALISES[analise_selecionada]
        messagebox.showinfo("Valor da Análise", f"O valor para análise de {analise_selecionada.capitalize()} é R${valor:.2f}")
    else:
        messagebox.showerror("Erro", "Selecione uma análise válida!")

# Função para atualizar as instruções
def atualizar_instrucoes():
    instrucoes = """
    **Instruções para Coleta de Amostra de Água para Análise**

    1. **Escolha do Local**: Coletar a amostra em um ponto representativo da fonte de água, como em rios, lagos ou poços, onde a água está em fluxo natural.

    2. **Equipamentos Necessários**: Utilize frascos limpos e esterilizados (vidro ou plástico) e material adequado para a coleta, como garra ou bomba, dependendo da profundidade.

    3. **Procedimento de Coleta**:
       - Para águas superficiais: Coletar a amostra a cerca de 50 cm abaixo da superfície.
       - Para poços: Coletar de um ponto representativo da coluna de água.
       - Evite tocar na parte interna do frasco ou tampa para prevenir contaminação.

    4. **Volume da Amostra**: Recolher de 1 a 2 litros de água, conforme orientação do laboratório.

    5. **Preservação da Amostra**: 
       - Para algumas análises, pode ser necessário adicionar conservantes.
       - Mantenha as amostras refrigeradas, especialmente para análises microbiológicas.

    6. **Etiquetagem**: Identifique claramente a amostra com:
       - Data e hora da coleta
       - Local de coleta
       - Nome do responsável pela coleta

    7. **Transporte**: Transporte a amostra em caixas térmicas, mantendo a temperatura adequada até a análise.

    **Observação**: Para garantir a precisão das análises, siga as instruções de forma cuidadosa e consulte o laboratório em caso de dúvidas.
    """
    
    text_instrucoes.delete(1.0, tk.END)  # Limpar o conteúdo atual
    text_instrucoes.insert(tk.END, instrucoes)  # Inserir as instruções no Text widget

LIMITE_DIARIO = 10  # Limite de agendamentos diários

# Funções de Estoque
def cadastrar_item():
    nome_item = entry_nome_item.get()
    quantidade = entry_quantidade_item.get()
    data_validade = entry_data_validade_item.get()
    fornecedor = entry_fornecedor_item.get()

    if not validar_data(data_validade):
        messagebox.showerror("Erro", "Data inválida. Use o formato YYYY-MM-DD.")
        return

    try:
        cursor.execute('''
            INSERT INTO estoque (item, quantidade, data_validade, fornecedor) 
            VALUES (?, ?, ?, ?)
        ''', (nome_item, quantidade, data_validade, fornecedor))
        conn.commit()
        messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
        atualizar_lista_estoque()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar item: {e}")

def atualizar_lista_estoque():
    for i in tree.get_children():
        tree.delete(i)
    
    cursor.execute("SELECT * FROM estoque")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

def editar_item():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showwarning("Seleção", "Selecione um item para editar.")
        return
    
    item_id = tree.item(item_selecionado)['values'][0]
    novo_nome_item = entry_nome_item.get()
    nova_quantidade = entry_quantidade_item.get()
    nova_data_validade = entry_data_validade_item.get()
    novo_fornecedor = entry_fornecedor_item.get()

    if not validar_data(nova_data_validade):
        messagebox.showerror("Erro", "Data inválida. Use o formato YYYY-MM-DD.")
        return

    try:
        cursor.execute('''
            UPDATE estoque SET item=?, quantidade=?, data_validade=?, fornecedor=? WHERE id=?
        ''', (novo_nome_item, nova_quantidade, nova_data_validade, novo_fornecedor, item_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Item editado com sucesso!")
        atualizar_lista_estoque()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao editar item: {e}")

def excluir_item():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showwarning("Seleção", "Selecione um item para excluir.")
        return
    
    item_id = tree.item(item_selecionado)['values'][0]
    
    try:
        cursor.execute('DELETE FROM estoque WHERE id=?', (item_id,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Item excluído com sucesso!")
        atualizar_lista_estoque()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao excluir item: {e}")

# Funções de Agendamento
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
    global cliente_agendado, data_agendada, analises_agendadas, valor_total_agendado, instrucoes_agendamento
    
    cliente_id_str = entry_cliente_id.get()

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

    # Atualizar variáveis globais
    cliente_agendado = cliente
    data_agendada = data
    analises_agendadas = analises
    valor_total_agendado = valor_total
    instrucoes_agendamento = instrucoes_agendamento

    messagebox.showinfo("Instruções", instrucoes_agendamento)
    confirmar = messagebox.askyesno("Confirmar Agendamento", f"Valor total: R${valor_total:.2f}\nDeseja confirmar o agendamento?")

    if confirmar:
        try:
            cursor.execute(
                "INSERT INTO agendamentos (cliente_id, data, analises, valor_total) VALUES (?, ?, ?, ?)",
                (cliente_id, data, ", ".join(analises), valor_total)
            )
            conn.commit()
            gerar_pdf_agendamento()
            messagebox.showinfo("Sucesso", "Agendamento realizado com sucesso!")
            
            # Ativar o botão de gerar PDF
            botao_gerar_pdf.config(state="normal")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao inserir no banco: {e}")
            messagebox.showerror("Erro", "Erro ao agendar. Tente novamente.")

def gerar_pdf_agendamento():
    global cliente_agendado, data_agendada, analises_agendadas, valor_total_agendado
    
        
    # Criar o PDF
    nome_arquivo_pdf = f"agendamento_{cliente_agendado}_{data_agendada}.pdf"
    c = canvas.Canvas(nome_arquivo_pdf, pagesize=letter)
    
    # Título do PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Agendamento de Análise de Água")
    
    # Detalhes do Agendamento
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Cliente: {cliente_agendado}")
    c.drawString(100, 710, f"Data do Agendamento: {data_agendada}")
    c.drawString(100, 690, f"Análises: {', '.join(analises_agendadas)}")
    c.drawString(100, 670, f"Valor Total: R${valor_total_agendado:.2f}")
    
    # Adicionar as instruções de coleta
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 650, "Instruções para Coleta de Amostra de Água para Análise")
    
    c.setFont("Helvetica", 10)
    c.drawString(100, 630, "1. Escolha do Local: Coletar a amostra em um ponto representativo da fonte de água.")
    c.drawString(100, 610, "2. Equipamentos Necessários: Utilize frascos limpos e esterilizados.")
    c.drawString(100, 590, "3. Procedimento de Coleta: Coletar a amostra a cerca de 50 cm abaixo da superfície.")
    c.drawString(100, 570, "4. Volume da Amostra: Recolher de 1 a 2 litros, conforme orientação do laboratório.")
    c.drawString(100, 550, "5. Preservação da Amostra: Mantenha as amostras refrigeradas.")
    c.drawString(100, 530, "6. Etiquetagem: Identifique claramente a amostra com data, hora e local.")
    c.drawString(100, 510, "7. Transporte: Transporte a amostra em caixas térmicas, mantendo a temperatura adequada.")
    c.drawString(100, 490, "Observação: Para garantir a precisão, siga as instruções cuidadosamente.")
    
    # Finalizar e salvar o PDF
    c.showPage()
    c.save()
    
    # Mostrar mensagem de sucesso
    messagebox.showinfo("PDF Gerado", f"PDF gerado com sucesso! Salvo como {nome_arquivo_pdf}")

    pdf = canvas.Canvas(f"agendamento_{cliente_agendado[1]}.pdf", pagesize=letter)
    pdf.drawString(100, 750, f"Agendamento de Análises - {cliente_agendado[1]}")
    y = 730
    pdf.drawString(100, y, f"Data: {data_agendada}")
    y -= 20
    pdf.drawString(100, y, f"Análises: {', '.join(analises_agendadas)}")
    y -= 20
    pdf.drawString(100, y, f"Valor Total: R${valor_total_agendado:.2f}")
    y -= 20
    pdf.drawString(100, y, f"Instruções: {instrucoes_agendamento}")
    pdf.save()


# Função para Listar Agendamentos
def listar_agendamentos():
    for i in tree_agendamentos.get_children():
        tree_agendamentos.delete(i)
    
    cursor.execute('''
        SELECT clientes.nome, agendamentos.data, agendamentos.analises, agendamentos.valor_total, agendamentos.status
        FROM agendamentos
        JOIN clientes ON agendamentos.cliente_id = clientes.id
    ''')
    registros = cursor.fetchall()
    if not registros:
        messagebox.showinfo("Sem Agendamentos", "Não há agendamentos para listar.")
    
    for row in registros:
        tree_agendamentos.insert('', 'end', values=row)
    for row in cursor.fetchall():
        tree_agendamentos.insert('', 'end', values=row)
# Iniciando a interface gráfica
root = tk.Tk()  # Aqui está a criação da janela principal
root.title("Sistema de Controle de Estoque e Agendamentos")        
root = tk.Tk()
root.title("Instruções de Coleta de Amostra de Água")
root.geometry("800x600")

# Abas principais
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Aba Instruções de Coleta
frame_instrucoes = ttk.Frame(notebook)
notebook.add(frame_instrucoes, text="Instruções de Coleta")

# Exibir instruções para coleta
text_instrucoes = tk.Text(frame_instrucoes, wrap=tk.WORD, width=80, height=15)
text_instrucoes.pack(padx=10, pady=10)
atualizar_instrucoes()  # Atualiza as instruções de coleta na interface

# Seção para adicionar as análises e seus valores
frame_analises = ttk.Frame(frame_instrucoes)
frame_analises.pack(padx=10, pady=10)

# Lista das análises
lista_analises = tk.Listbox(frame_analises, height=6, width=40)
lista_analises.pack(side=tk.LEFT, padx=10)
atualizar_analises()  # Atualiza a lista de análises com os valores

# Botão para exibir o valor da análise selecionada
botao_verificar_valor = ttk.Button(frame_analises, text="Verificar Valor", command=exibir_valor_analise)
botao_verificar_valor.pack(side=tk.LEFT, padx=10)

# Seção para selecionar análise no ComboBox
frame_selecionar_analise = ttk.Frame(frame_instrucoes)
frame_selecionar_analise.pack(padx=10, pady=10)

# ComboBox para seleção de análise
combo_analises = ttk.Combobox(frame_selecionar_analise, values=list(ANALISES.keys()), state="readonly", width=30)
combo_analises.set("Escolha uma análise")
combo_analises.pack(padx=10)

# Botão para exibir o valor da análise selecionada
botao_exibir_valor = ttk.Button(frame_selecionar_analise, text="Exibir Valor", command=exibir_valor_analise)
botao_exibir_valor.pack(padx=10)

# Rodapé com a versão do sistema
label_rodape = ttk.Label(root, text="Sistema de Coleta e Análises de Água - Versão 1.0", anchor="center")
label_rodape.pack(side="bottom", fill="x", pady=5)
# Aba de Estoque
tab_control = ttk.Notebook(root)
tab_estoque = ttk.Frame(tab_control)
tab_agendamento = ttk.Frame(tab_control)
tab_cliente = ttk.Frame(tab_control)
tab_lista_agendamentos = ttk.Frame(tab_control)
tab_instrucoes = ttk.Frame(tab_control)
tab_listar_clientes = ttk.Frame(tab_control)  # Nova aba para listar clientes

tab_control.add(tab_cliente, text="Cadastrar Cliente")
tab_control.add(tab_agendamento, text="Agendar Análise")
tab_control.add(tab_lista_agendamentos, text="Listar Agendamentos")
tab_control.add(tab_instrucoes, text="Instruções para Coleta")
tab_control.add(tab_estoque, text="Controle de Estoque")
tab_control.add(tab_listar_clientes, text="Listar Clientes")  # Adicionando aba de listar clientes
tab_control.pack(expand=1, fill="both")

# ------------------------------ Listar Clientes ------------------------------
tree_clientes = ttk.Treeview(tab_listar_clientes, columns=("ID", "Nome"), show="headings")
tree_clientes.heading("ID", text="ID")
tree_clientes.heading("Nome", text="Nome")
tree_clientes.pack(fill="both", expand=True)

botao_listar_clientes = tk.Button(tab_listar_clientes, text="Listar Clientes", command=listar_clientes)
botao_listar_clientes.pack()

# ------------------------------ Cadastro de Cliente ------------------------------
label_nome = tk.Label(tab_cliente, text="Nome do Cliente")
label_nome.grid(row=0, column=0)
entry_nome = tk.Entry(tab_cliente)
entry_nome.grid(row=0, column=1)

label_email = tk.Label(tab_cliente, text="Email")
label_email.grid(row=1, column=0)
entry_email = tk.Entry(tab_cliente)
entry_email.grid(row=1, column=1)

label_telefone = tk.Label(tab_cliente, text="Telefone")
label_telefone.grid(row=2, column=0)
entry_telefone = tk.Entry(tab_cliente)
entry_telefone.grid(row=2, column=1)

label_endereco = tk.Label(tab_cliente, text="Endereço")
label_endereco.grid(row=3, column=0)
entry_endereco = tk.Entry(tab_cliente)
entry_endereco.grid(row=3, column=1)

botao_cadastrar_cliente = tk.Button(tab_cliente, text="Cadastrar Cliente", command=cadastrar_cliente)
botao_cadastrar_cliente.grid(row=4, column=0, columnspan=2)

# ------------------------------ Agendamento --------------------------------------

label_cliente_id = tk.Label(tab_agendamento, text="ID Cliente")
label_cliente_id.grid(row=0, column=0)
entry_cliente_id = tk.Entry(tab_agendamento)
entry_cliente_id.grid(row=0, column=1)

label_data = tk.Label(tab_agendamento, text="Data (YYYY-MM-DD)")
label_data.grid(row=1, column=0)
entry_data = tk.Entry(tab_agendamento)
entry_data.grid(row=1, column=1)

label_analises = tk.Label(tab_agendamento, text="Análises (coliformes, ph, dureza, alcalinidade)")
label_analises.grid(row=2, column=0)
entry_analises = tk.Entry(tab_agendamento)
entry_analises.grid(row=2, column=1)

botao_agendar = tk.Button(tab_agendamento, text="Agendar", command=agendar)
botao_agendar.grid(row=3, column=0, columnspan=2)

# Criar o botão de gerar PDF
botao_gerar_pdf = tk.Button(tab_agendamento, text="Gerar PDF do Agendamento", state="disabled", command=gerar_pdf_agendamento)
botao_gerar_pdf.grid(row=4, column=0, columnspan=2)


# ------------------------------ Listar Agendamentos ------------------------------
tree_agendamentos = ttk.Treeview(tab_lista_agendamentos, columns=("Nome", "Data", "Análises", "Valor Total", "Status"), show="headings")
tree_agendamentos.heading("Nome", text="Nome")
tree_agendamentos.heading("Data", text="Data")
tree_agendamentos.heading("Análises", text="Análises")
tree_agendamentos.heading("Valor Total", text="Valor Total")
tree_agendamentos.heading("Status", text="Status")
tree_agendamentos.pack(fill="both", expand=True)

botao_listar_agendamentos = tk.Button(tab_lista_agendamentos, text="Listar Agendamentos", command=listar_agendamentos)
botao_listar_agendamentos.pack()

# ------------------------------ Instruções para Coleta -------------------------

label_instrucao = tk.Label(tab_instrucoes, text="Instruções para Coleta")
label_instrucao.pack(pady=10)

botao_mostrar_instrucoes = tk.Button(tab_instrucoes, text="Mostrar Instruções", command=lambda: messagebox.showinfo("Instruções", instrucoes(entry_data.get(), entry_analises.get().split(","))))
botao_mostrar_instrucoes.pack(pady=10)

# ------------------------------ Controle de Estoque --------------------------

label_nome_item = tk.Label(tab_estoque, text="Nome do Item")
label_nome_item.grid(row=0, column=0)
entry_nome_item = tk.Entry(tab_estoque)
entry_nome_item.grid(row=0, column=1)

label_quantidade_item = tk.Label(tab_estoque, text="Quantidade")
label_quantidade_item.grid(row=1, column=0)
entry_quantidade_item = tk.Entry(tab_estoque)
entry_quantidade_item.grid(row=1, column=1)

label_data_validade_item = tk.Label(tab_estoque, text="Data de Validade (YYYY-MM-DD)")
label_data_validade_item.grid(row=2, column=0)
entry_data_validade_item = tk.Entry(tab_estoque)
entry_data_validade_item.grid(row=2, column=1)

label_fornecedor_item = tk.Label(tab_estoque, text="Fornecedor")
label_fornecedor_item.grid(row=3, column=0)
entry_fornecedor_item = tk.Entry(tab_estoque)
entry_fornecedor_item.grid(row=3, column=1)

botao_cadastrar_item = tk.Button(tab_estoque, text="Cadastrar Item", command=cadastrar_item)
botao_cadastrar_item.grid(row=4, column=0)

botao_editar_item = tk.Button(tab_estoque, text="Editar Item", command=editar_item)
botao_editar_item.grid(row=4, column=1)

botao_excluir_item = tk.Button(tab_estoque, text="Excluir Item", command=excluir_item)
botao_excluir_item.grid(row=4, column=2)

tree = ttk.Treeview(tab_estoque, columns=("ID", "Item", "Quantidade", "Data Validade", "Fornecedor"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Item", text="Item")
tree.heading("Quantidade", text="Quantidade")
tree.heading("Data Validade", text="Data Validade")
tree.heading("Fornecedor", text="Fornecedor")
tree.grid(row=5, column=0, columnspan=3)

# Atualiza a lista de itens ao iniciar
atualizar_lista_estoque()

root.mainloop()
