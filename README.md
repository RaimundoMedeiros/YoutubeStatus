# Interface de visualização de dados de vídeos com Arquitetura MVC

Este projeto é uma aplicação Python desenvolvida com a arquitetura **MVC (Model-View-Controller)**, com interface gráfica, tratamento de dados e visualização em gráficos. 

##  Objetivo

A aplicação tem como objetivo demonstrar o funcionamento de um sistema com:
- Arquitetura MVC
- Interface gráfica interativa (GUI).
- Tratamento e exibição de gráficos.
- Separação clara entre modelo de dados, interface e controle.

##  Estrutura do Projeto

- `Model.py`: Responsável pela lógica e dados do sistema. Aqui estão funções tratamento de dados, armazenamento e manipulação.
- `View.py`: Define a interface gráfica com `tkinter`, contendo campos de entrada, botões e área de visualização.
- `projeto.py`: Arquivo principal, responsável por integrar o Model e a View (atuando como Controller).
- `DiagramaDeClasseProjeto.png`: Diagrama ilustrando a organização das classes no padrão MVC.

##  Bibliotecas Utilizadas

| Biblioteca | Uso |
|------------|------------|
| **tkinter** | Criação da interface gráfica (GUI) com botões, entradas, labels etc. |
| **tkinter.ttk** | Versão mais moderna dos widgets do `tkinter`, com melhor aparência. |
| **tkinter.messagebox** | Exibição de janelas de alerta e mensagens ao usuário. |
| **pandas** | Manipulação e estruturação dos dados recebidos em forma de tabelas. |
| **matplotlib.pyplot** | Geração de gráficos a partir dos dados simulados. |
| **seaborn** | Estilização dos gráficos com visual mais agradável e estatisticamente informativo. |
