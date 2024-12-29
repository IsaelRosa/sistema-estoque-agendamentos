# Sistema de Controle de Estoque e Agendamentos

Este é um projeto desenvolvido em Python com interface gráfica utilizando `tkinter`, para gerenciamento de estoque, cadastro de clientes, agendamento de análises laboratoriais e geração de relatórios em PDF.

## Funcionalidades

- **Cadastro de clientes:** Adicionar clientes com informações como nome, email, telefone e endereço.
- **Controle de estoque:** Gerenciar itens, incluindo cadastro, edição e exclusão.
- **Agendamento de análises:** Agendar análises laboratoriais com cálculo automático do valor total e instruções específicas para coleta.
- **Listagem de agendamentos:** Visualizar os agendamentos realizados com status, cliente, data, análises e valores.
- **Geração de relatórios em PDF:** Criar relatórios detalhados dos agendamentos realizados.
- **Listagem de clientes:** Consultar clientes cadastrados no sistema.

## Tecnologias Utilizadas

- **Python 3.9+**
- **SQLite:** Banco de dados para armazenar informações.
- **tkinter:** Interface gráfica.
- **ReportLab:** Geração de relatórios em PDF.

## Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior instalado.
- Dependências adicionais podem ser instaladas com:
  ```bash
  pip install reportlab

