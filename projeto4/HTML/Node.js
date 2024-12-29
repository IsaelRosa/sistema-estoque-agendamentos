const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('estoque_agendamentos.db');

// Criação das tabelas no banco de dados, caso ainda não existam
db.serialize(() => {
    // Criando a tabela de clientes
    db.run("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, telefone TEXT, endereco TEXT)");

    // Criando a tabela de agendamentos
    db.run("CREATE TABLE IF NOT EXISTS agendamentos (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER, data TEXT, analises TEXT, valor_total INTEGER, status TEXT, FOREIGN KEY (cliente_id) REFERENCES clientes(id))");
});

// Rota para cadastrar cliente
app.post('/api/cadastrar-cliente', (req, res) => {
    const { nome, email, telefone, endereco } = req.body;
    db.run("INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?)", [nome, email, telefone, endereco], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.status(200).json({ id: this.lastID });
    });
});

// Rota para listar clientes
app.get('/api/clientes', (req, res) => {
    db.all("SELECT id, nome FROM clientes", [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

// Rota para agendar análise
app.post('/api/agendar', (req, res) => {
    const { clienteId, data, analises } = req.body;
    const analisesStr = analises.join(", ");
    const valorTotal = analises.length * 50; // Exemplo de cálculo de valor total

    db.run("INSERT INTO agendamentos (cliente_id, data, analises, valor_total) VALUES (?, ?, ?, ?)", [clienteId, data, analisesStr, valorTotal], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.status(200).json({ id: this.lastID });
    });
});

// Rota para listar agendamentos
app.get('/api/agendamentos', (req, res) => {
    db.all("SELECT clientes.nome, agendamentos.data, agendamentos.analises, agendamentos.valor_total, agendamentos.status FROM agendamentos JOIN clientes ON agendamentos.cliente_id = clientes.id", [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

// O banco de dados só será fechado quando o servidor for encerrado
process.on('SIGINT', () => {
    db.close((err) => {
        if (err) {
            console.error('Erro ao fechar o banco de dados:', err);
        }
        console.log('Banco de dados fechado.');
        process.exit(0);
    });
});
