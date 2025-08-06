# Os Maltrapilhos

Relátorio de Desenvolvimento do jogo Os Maltrapilhos, feito para a cadeira de Introdução a Programação do curso de Sistemas de Informação do CIn-UFPE no semestre 2025-01.

## Equipe

<table>
    <tr>
        <td align="center"><a href="https://github.com/helington"><img src="https://avatars.githubusercontent.com/u/78865806?v=4" width="100px"/><br /><sub><b>Helington Willamy</b></sub></a><br/</td>
        <td align="center"><a href="https://github.com/JeanValjeanRD"><img src="https://avatars.githubusercontent.com/u/154392376?v=4" width="100px"/><br /><sub><b>Gabriel Nóbrega</b></sub></a><br/></td>
        <td align="center"><a href="https://github.com/luismiguuel"><img src="https://avatars.githubusercontent.com/u/224866738?v=4" width="100px"/><br /><sub><b>Luis Miguel</b></sub></a><br/></td>
        <td align="center"><a><br /><sub><b>João Vitor</b></sub></a><br/></td>
        <td align="center"><a href="https://github.com/Igor-a-Soares"><img src="https://avatars.githubusercontent.com/u/223944470?v=4" width="100px"/><br /><sub><b>Igor Soares</b></sub></a><br/></td>
        <td align="center"><a href="https://github.com/AldusD"><img src="https://avatars.githubusercontent.com/u/98439753?v=4" width="100px"/><br /><sub><b>Aldus Daniel</b></sub></a><br/></td>
    </tr>
</table>

## Estrutura do projeto

```
Projeto-IP/
├── main.py                  # Arquivo principal que inicia o jogo
├── settings.py              # Configurações globais (tamanho da tela, FPS, cores, etc.)
├── core/                    # Lógica central do jogo
│   ├── game.py              # Classe principal que gerencia o loop do jogo
│   └── utils.py             # Funções auxiliares
├── scenes/                  # Cenas do jogo (tutorial, menu, gameplay, game over, etc.)
├── entities/                # Entidades e personagens do jogo
├── assets/                  # Recursos gráficos, sonoros e tipográficos
│   ├── fonts/               # Fontes
│   ├── graphics/            # Imagens dos Sprites e do mapa
│   └── sounds/              # Efeitos sonoros
├── requirements.txt         # Dependências do projeto (bibliotecas usadas)
└── README.md                # Documentação e instruções do projeto
```

## Bibliotecas e ferramentas utilizadas
- [ PyGame ]( https://www.pygame.org/news ): Biblioteca principal para o desenvolvimento do jogo.

## Conceitos utilizados

## Desafios e erros

## Capturas de tela

## Como instalar e rodar o jogo

### 1. Clone o repositório

```bash
git clone https://github.com/helington/Projeto-IP.git
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
