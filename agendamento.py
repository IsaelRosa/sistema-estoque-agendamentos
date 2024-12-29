import sqlite3
from datetime import datetime

# Configurando o banco de dados
conn = sqlite3.connect("agendamentos.db")
cursor = conn.cursor()

# Criar tabela de agendamentos
cursor.execute('''
CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    data TEXT NOT NULL,
    analises TEXT NOT NULL,
    valor_total REAL NOT NULL
)
''')

ANALISES = {
    "coliformes": 50.0,
    "ph": 20.0,
    "dureza": 30.0,
    "alcalinidade": 25.0
}

LIMITE_DIARIO = 10

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

def agendar():
    cliente = input("Nome do cliente: ")
    data = input("Data do agendamento (YYYY-MM-DD): ")

    if not verificar_disponibilidade(data):
        print("Não há mais vagas disponíveis para esta data.")
        return

    print("Opções de análises disponíveis:")
    for analise, preco in ANALISES.items():
        print(f"- {analise}: R${preco:.2f}")

    analises = input("Digite as análises desejadas separadas por vírgula: ").split(",")
    analises = [a.strip() for a in analises if a.strip() in ANALISES]

    if not analises:
        print("Nenhuma análise válida selecionada.")
        return

    valor_total = calcular_valor_total(analises)
    print(f"Valor total: R${valor_total:.2f}")
    
    instrucoes_agendamento = instrucoes(data, analises)
    print("Instruções:")
    print(instrucoes_agendamento)

    # Confirmar e salvar
    confirmar = input("Confirmar agendamento? (s/n): ").lower()
    if confirmar == "s":
        cursor.execute(
            "INSERT INTO agendamentos (cliente, data, analises, valor_total) VALUES (?, ?, ?, ?)",
            (cliente, data, ", ".join(analises), valor_total)
        )
        conn.commit()
        print("Agendamento realizado com sucesso!")
    else:
        print("Agendamento cancelado.")

def listar_agendamentos():
    cursor.execute("SELECT * FROM agendamentos")
    agendamentos = cursor.fetchall()
    if not agendamentos:
        print("Nenhum agendamento encontrado.")
        return

    print("Agendamentos:")
    for agendamento in agendamentos:
        print(f"ID: {agendamento[0]} | Cliente: {agendamento[1]} | Data: {agendamento[2]} | Analises: {agendamento[3]} | Valor: R${agendamento[4]:.2f}")

def main():
    while True:
        print("\nMenu:")
        print("1. Agendar análise")
        print("2. Listar agendamentos")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            agendar()
        elif opcao == "2":
            listar_agendamentos()
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

# Fechar conexão com o banco de dados
conn.close()
