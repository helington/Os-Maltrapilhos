# Rambinho: O Último Soldado

Relátorio de Desenvolvimento do jogo **Rambinho: O Último Soldado**, feito para a cadeira de Introdução a Programação do curso de Sistemas de Informação do CIn-UFPE no semestre 2025-01.

## Equipe

<table>
    <tr>
        <td align="center"><a href="https://github.com/helington"><img src="https://avatars.githubusercontent.com/u/78865806?v=4" width="100px"/><br /><sub><b>Helington Willamy</b></sub></a><br/</td>
        <td align="center"><a href="https://github.com/GabrielNSB007"><img src="https://avatars.githubusercontent.com/u/154392376?v=4" width="100px"/><br /><sub><b>Gabriel Nóbrega</b></sub></a><br/></td>
        <td align="center"><a href="https://github.com/luismiguuel"><img src="https://avatars.githubusercontent.com/u/224866738?v=4" width="100px"/><br /><sub><b>Luis Miguel</b></sub></a><br/></td>
        <td align="center"><a href="https://github.com/vitorlins0"><img src="https://avatars.githubusercontent.com/u/224650528?v=4" width="100px"/><br /><sub><b>João Vitor</b></sub></a><br/></td>
        <td align="center"><a href="https://github.com/Igor-a-Soares"><img src="https://avatars.githubusercontent.com/u/223944470?v=4" width="100px"/><br /><sub><b>Igor Soares</b></sub></a><br/></td>
        <td align="center"><a href="https://github.com/AldusD"><img src="https://avatars.githubusercontent.com/u/98439753?v=4" width="100px"/><br /><sub><b>Aldus Daniel</b></sub></a><br/></td>
    </tr>
</table>

## Estrutura do projeto

O projeto segue uma arquitetura modular, separando responsabilidades em diferentes pacotes:

```
Rambinho/
├── assets/                # Recursos do jogo
│ ├── graphics/            # Imagens dos sprites e do mapa
│ └── levels/              # Arquivos de nível
├── src/                   # Código-fonte do jogo
│ ├── config/              # Arquivos de configuração
│ ├── core/                # Lógica central do jogo
│ ├── entities/            # Entidades e personagens do jogo
│ │ ├── bullet/            # Representação das balas
│ │ ├── character/         # Representação dos personagens (Inimigos e o jogador)
│ │ ├── collectable/       # Representação dos coletáveis
│ │ └── world/             # Representação do mundo de gameplay e seus elementos (Obstáculos, Background e etc)
│ ├── off_game_screens/    # Telas de menu, game over, etc.
│ ├── __init__.py          # Módulo de inicialização
│ └── entities_enum.py     # Enumeração de entidades
├── .gitignore             # Arquivos e diretórios a serem ignorados pelo Git
├── README.md              # Relatório do projeto
├── main.py                # Arquivo principal que inicia o jogo
└── requirements.txt       # Dependências do projeto (bibliotecas usadas)
```

## Bibliotecas e ferramentas utilizadas
- [PyGame](https://www.pygame.org/news): Biblioteca principal para o desenvolvimento do jogo.
- [OS](https://docs.python.org/3/library/os.html): Biblioteca usada para acessar as sprites e artes do jogo.
- [Pathlib](https://docs.python.org/3/library/pathlib.html): Biblioteca usada como auxiliar para encontrar o diretório das sprites e artes do jogo.
- [Enum](https://docs.python.org/3/library/enum.html): Biblioteca usada para criar grupos de classes, facilitando a legibilidade e interpretação do código, evitando a criação de números mágicos.
- [CSV](https://docs.python.org/3/library/csv.html): Biblioteca usada para leitura do arquivo da fase atual.
- [Math](https://docs.python.org/3/library/math.html): Biblioteca usada para criação do movimento de flutuação dos itens coletáveis.
- [Random](https://docs.python.org/3/library/random.html): Biblioteca usada para definir a movimentação dos inimigos.
- [Piskel](https://www.piskelapp.com/): Ferramenta usada para criação das sprites do jogo.
- [Itch.io](https://itch.io/): Ferramenta usada para arte do background do jogo.

## Conceitos utilizados

## Desafios e erros

## Capturas de tela

<table>
    <tr>
        <td align="center"><img src="https://snipboard.io/YuPDxO.jpg" width="1200px"/><br /><sub><b>Tela de Início</b></sub></a><br/</td>
        <td align="center"><img src="https://snipboard.io/iZA83F.jpg" width="1200px"/><br /><sub><b>Tela do Jogo em Andamento (Um Jogador)</b></sub></a><br/></td></tr>
    <tr>
        <td align="center"><img src="https://snipboard.io/h0RAzd.jpg" width="1200px"/><br /><sub><b>Tela do Jogo em Andamento (Quatro Jogadores)</b></sub></a><br/></td>
        <td align="center"><img src="https://snipboard.io/QNPYO4.jpg" width="1200px"/><br /><sub><b>Tela do Jogo em Andamento (Jogador Nadando)</b></sub></a><br/></td>
    </tr>
</table>

## Como instalar e rodar o jogo

### 1. Clone o repositório e entre no mesmo

```bash
git clone https://github.com/helington/Projeto-IP.git
cd Projeto-IP
```

### 2. Crie o ambiente virtual

```bash
python3 -m venv venv
```

### 3. Ative o ambiente virtual

#### No MacOS/Linux
```bash
source venv/bin/activate
```
#### No Windows
```bash
venv\Scripts\activate.bat
```

### 4. Instale as dependências
```bash
pip3 install -r requirements.txt
```

### 5. Execute o jogo
```bash
python3 main.py
```
