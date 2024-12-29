# Sistema de Agendamentos Análises de Água e  Controle de Estoque de Reagentes

Este é um projeto desenvolvido em Python com interface gráfica utilizando tkinter, criado para facilitar o gerenciamento de estoque, cadastro de clientes, agendamento de análises laboratoriais e a geração de relatórios em PDF. Ele foi pensado para laboratórios ou empresas que buscam uma solução simples e eficiente para organizar suas atividades.

## Funcionalidades Principais

- **Cadastro de clientes:** 
    - Adicione clientes com informações detalhadas como:
        - Nome
        - Email
        - Telefone
EndereçoAdicionar clientes com informações como nome, email, telefone e endereço.
- **Controle de estoque:** 
    - Gerencie itens do estoque:
      - Cadastro de novos itens
      - Edição de informações dos itens
      - Exclusão de itens obsoletos ou fora de uso
- **Agendamento de análises:** 
    - Realize agendamentos laboratoriais com:
      - Cálculo automático do valor total
      - Instruções específicas para coleta
      - Associação a clientes cadastrados
- **Listagem de agendamentos:**
    - Consulte os agendamentos realizados, exibindo informações como:
      - Cliente
      - Data do agendamento
      - Análises solicitadas
      - Valores calculados
      - Status do agendamento
- **Geração de relatórios em PDF:** 
    - Crie relatórios detalhados com todas as informações relevantes dos agendamentos, facilitando o compartilhamento e o armazenamento de dados.
- **Listagem de clientes:** 
    - Consulte os clientes cadastrados, possibilitando rápida visualização e acesso às informações.

## Tecnologias Utilizadas

- **Python 3.9+**
- **SQLite:** Banco de dados para armazenar informações.
- **tkinter:** Interface gráfica.
- **ReportLab:** Geração de relatórios em PDF.

## Instalação e Configuração
### Tecnologias Utilizadas

- Python 3.9+: Linguagem principal utilizada no desenvolvimento.
- SQLite: Banco de dados embutido para armazenamento de informações.
- tkinter: Ferramenta para criação da interface gráfica.
- ReportLab: Biblioteca para geração de relatórios em formato PDF.

### Instalação e Configuração
#### Pré-requisitos

##### Certifique-se de ter instalado em seu ambiente:
    - Python 3.9 ou superior.
    - Gerenciador de pacotes pip configurado.

### Pré-requisitos

- Python 3.9 ou superior instalado.
- Dependências adicionais podem ser instaladas com:
  ```bash
  pip install reportlab

