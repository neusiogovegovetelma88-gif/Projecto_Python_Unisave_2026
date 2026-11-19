# Ciber Seguro - Quiz de Segurança Informática

- O Ciber Seguro é uma aplicação desktop em Python que ensina cibersegurança de forma interativa. O utilizador escolhe um tema, responde a perguntas e recebe explicação e recomendações. Resolve o problema da falta de conhecimento sobre phishing, burlas de prémios, roubo de PIN e Wi-Fi falso, muito comuns em Moçambique.

## Elementos do Grupo

- Clara Pinto Covane (claracovane1)
- Dionisío João Rungo (dionisiorungo8-max)
- Neusio da Telma Gove (neusiogovegovetelma88-gif)
- Frédio Vasco Utui (frediovascoutui8)

## Funcionalidades

- 4 temas com 20 perguntas: Cibersegurança básica, Vírus e fraudes, Wi-Fi e Protecção de contas
- Perguntas e respostas baralhadas com `random`
- Feedback imediato com explicação da resposta certa
- Resultado em percentagem + recomendações personalizadas das perguntas erradas
- Histórico persistente em JSON: melhor nota, tentativas e datas
- Interface gráfica com Tkinter, botões coloridos e popups

## Stack Técnica

- Linguagem: Python 3.x
- Paradigma: Programação Orientada a Objetos (POO)
- Armazenamento: JSON
- Dependências: Só biblioteca padrão - tkinter, json, os, random, datetime, dataclasses

## Arquitetura

- O código está organizado em 3 camadas: Modelo de Dados (`Pergunta`, `Tema`), Persistência (`GestorHistorico` - carrega/guarda JSON com try/except) e Interface (`App` - Tkinter). A função `main()` inicia a aplicação. As perguntas são objetos, o histórico é um dicionário JSON e a interface só mostra o que o modelo fornece.

## Requisitos

- Python 3.8 ou superior instalado no computador.

## Instalação e Execução

Bash
```bash
git clone https://github.com/neusiogovegovetelma88-gif/Projecto_Python_Unisave_2026.git
cd Projecto_Python_Unisave_2026
python main.py