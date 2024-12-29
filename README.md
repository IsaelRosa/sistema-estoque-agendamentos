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

#### Passos para Instalação
- 1° Clone o repositório do projeto:
    - git clone https://github.com/seu-usuario/sistema-controle-estoque.git
    - cd sistema-controle-estoque
- 2° Instale as dependências necessárias:
    - pip install reportlab
- 3° Execute o arquivo principal para iniciar a aplicação:
    - C:\Users\user\Documents\LOCALDOPROJETO>'C:\Program Files (x86)\Python312-32\python.exe' -m PyInstaller --onefile --hidden-import=reportlab "NOMEDOARQUIVO.py"                               

## Como Usar
- 1° Inicie o sistema: Após executar o comando acima, a interface gráfica será exibida. 
- 2° Cadastre clientes: Clique na opção de cadastro e insira as informações necessárias.
- 3° Gerencie o estoque: Adicione, edite ou remova itens do estoque conforme necessário.
- 4° Realize agendamentos: Selecione um cliente, escolha as análises e finalize o agendamento.
- 5° Visualize relatórios: Gere PDFs dos agendamentos para impressão ou armazenamento.


