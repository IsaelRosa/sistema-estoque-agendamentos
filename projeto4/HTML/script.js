// Cadastro de Cliente
document.getElementById('form-cadastrar-cliente').addEventListener('submit', function(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const telefone = document.getElementById('telefone').value;
    const endereco = document.getElementById('endereco').value;

    const cliente = {
        nome,
        email,
        telefone,
        endereco
    };

    fetch('/api/cadastrar-cliente', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(cliente)
    })
    .then(response => response.json())
    .then(data => {
        alert('Cliente cadastrado com sucesso!');
        document.getElementById('form-cadastrar-cliente').reset();
    })
    .catch(error => {
        console.error('Erro ao cadastrar cliente:', error);
        alert('Erro ao cadastrar cliente.');
    });
});

// Agendamento de Análises
document.getElementById('form-agendamento').addEventListener('submit', function(event) {
    event.preventDefault();

    const clienteId = document.getElementById('cliente-id').value;
    const data = document.getElementById('data').value;
    const analises = document.getElementById('analises').value.split(',').map(a => a.trim());

    const agendamento = {
        clienteId,
        data,
        analises
    };

    fetch('/api/agendar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(agendamento)
    })
    .then(response => response.json())
    .then(data => {
        alert('Agendamento realizado com sucesso!');
        document.getElementById('form-agendamento').reset();
    })
    .catch(error => {
        console.error('Erro ao agendar:', error);
        alert('Erro ao agendar.');
    });
});

// Listar Clientes
document.getElementById('listar-clientes-btn').addEventListener('click', function() {
    fetch('/api/clientes')
    .then(response => response.json())
    .then(clientes => {
        const tbody = document.querySelector('#tabela-clientes tbody');
        tbody.innerHTML = '';
        clientes.forEach(cliente => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${cliente.id}</td><td>${cliente.nome}</td>`;
            tbody.appendChild(row);
        });
    })
    .catch(error => console.error('Erro ao listar clientes:', error));
});

// Listar Agendamentos
document.getElementById('listar-agendamentos-btn').addEventListener('click', function() {
    fetch('/api/agendamentos')
    .then(response => response.json())
    .then(agendamentos => {
        const tbody = document.querySelector('#tabela-agendamentos tbody');
        tbody.innerHTML = '';
        agendamentos.forEach(agendamento => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${agendamento.nome}</td><td>${agendamento.data}</td><td>${agendamento.analises}</td><td>${agendamento.valor_total}</td><td>${agendamento.status}</td>`;
            tbody.appendChild(row);
        });
    })
    .catch(error => console.error('Erro ao listar agendamentos:', error));
});
