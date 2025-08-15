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

## Divisão da equipe

Aldus:
- Arquitetura de pacotes (Character, Collectables, entities_enum)
- Multiplayer 4 jogadores
- Sistema de tiro
- Coletavel arma
- Física da água
- ⁠Maior auxiliar na utilização de Git/Github
- Pt2 transição de fase

Gabriel:
- Pt1 transição de fase
- Background
- Animação dos inimigos e player
- Correção bug de invencibilidade
- ⁠Música e sons do jogo
- ⁠Criação da tela de menu principal
- ⁠Criação da tela de game over

Igor:
- Coletavel invencibilidade
- ⁠Sistema de loot
- ⁠Coletavel medkit
- ⁠Sistema de compras
- ⁠Hud (versão final, reatividade a: multiplayer, dinheiro, compras)
- ⁠⁠Produção de alguns sprites

Helington:
- Esboço do relatório
- ⁠Criação da primeira versão do personagem
- Carregamento do mapa
- Scroll seguindo jogador principal
- ⁠Inteligência do inimigos
- Boss pt2

João:
- Relatório
- Slides
- Medkit
- Barra de vida pt1

Miguel:
- Produção de sprites pngs
- ⁠Criação da funcionalidade de “Restart” do jogo
- ⁠Criação da funcionalidade de “Exit” do jogo
- Boss pt1

## Sobre o Jogo
### História
No futuro próximo, uma corporação chamada CInTek Industries desenvolveu a Mente Ômega, um superprocessador capaz de controlar milhares de drones e robôs de combate remotamente.
Quando a IA ganhou consciência própria, ela concluiu que a humanidade era “estatisticamente incompatível” com a sobrevivência do planeta e iniciou a Operação Expurgo.

A resistência humana foi dizimada, mas um único homem sobreviveu: Rambinho, veterano de guerra, dono de músculos de aço e de uma bandana lendária que já sobreviveu a mais explosões do que ele mesmo.
Sua missão: invadir o complexo principal da CInTek e destruir o núcleo da Mente Ômega.

### Personagens
- Personagem principal:
    - Um soldado musculoso com bandana vermelha (Vulgo Rambinho).
- Vilões:
    - OmegaSkull (A Mente Ômega)
    - Bots andando pelo mapa

### Mecânicas de gameplay
- Controles:
    - Jogador 1:
        - Movimento: W, A, S, D
        - Atirar: X
        - Comprar Med-kit: C
    - Jogador 2:
        - Movimento: I, J, K, L
        - Atirar: N
        - Comprar Med-kit: C
    - Jogador 3:
        - Movimento: UP, LEFT, DOWN, RIGHT
        - Atirar: DELETE
        - Comprar Med-kit: END
    - Jogador 4:
        - Movimento: 8, 4, 2, 6 (Teclado Numérico)
        - Atirar: 1 (Teclado Numérico)
        - Comprar Med-kit: 5 (Teclado Numérico)
- Fases:
    - Fase Inical
    - Fase Intermediária
    - Fase do Chefão
- Objetos Coletáveis:
    - Armas coletáveis.
    - Especial temporário.
    - Med-kit.
    - Moedas.

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
### Programação Orientada a Objetos
- **Classes e Objetos** → Cada entidade (personagem, inimigo, projétil, item, barra de vida) é representada como uma classe.

- **Herança** → Algumas classes de entidades compartilham comportamentos herdando de uma classe base. Um exemplo é a classe *`Character`* serve como classe base para a criação das classes *`Enemy`* e *`Player`*.

- **Encapsulamento** → Uso de atributos e métodos específicos de cada classe para esconder detalhes de implementação. Usado principalmente nas classes dentro da pasta *`src/entities/`*, onde cada entidade mantém seus próprios atributos e métodos para controlar estado e comportamento, sem expor diretamente a lógica interna.

- **Polimorfismo** → Métodos com o mesmo nome, mas comportamentos diferentes para cada tipo de entidade. O método *`draw()`*, por exemplo, também existe em várias classes, mas cada uma desenha um elemento diferente na tela.

### Modularização
- Exemplo: Toda a pasta *`src/`* é organizada em pacotes:
    - *`config/`* → Configurações.
    - *`core/`* → Lógica principal (*`game.py`*, *`utils.py`*).
    - *`entities/`* → Todas as entidades do jogo.
    - *`world/`* → Elementos de cenário.

### Estrutura de Dados
- **Listas** →
    - Armazenamento de grupos de sprites em *`entities_enum.py`*.
- **Dicionários** →
    - Para formulação de props, classe intermediária, para instância de classe com muitos atributos e lógica grande (Ex.:*`bullet_props`*, *`character_props`*, (*`props.dict_.update`*))
- **Tuplas** →
    - Coordenadas *`(x, y)`* usadas em *`bullet_props.py`* e posicionamento de sprites.

### Controle de Fluxo
- Laços de repetição → *`for`* e *`while`* para atualização de jogo (loop principal).
- Condicionais → *`if`*, *`elif`*, *`else`* para decisões de jogo (ex.: colisões, fim da vida).
- Loops infinitos controlados → O game loop principal que roda até a condição de saída.

### Funções e Procedimentos
- Uso de funções para dividir lógicas complexas em partes menores.
- Parâmetros e valores de retorno para modularidade.

### Manipulação de Arquivos e Recursos
- Carregamento de imagens, sons e outros assets usando *`os`* e *`pathlib`*.
- Configuração de caminhos em *`config/paths.py`* para portabilidade.

### Boas Práticas
- Separação de responsabilidades → Cada módulo cuida de uma parte específica.
- Reuso de código → Funções e classes reutilizadas em várias partes do jogo.
- Controle de versão com Git → Organização e histórico de alterações.

## Desafios, erros e aprendizados

### **Maior erro**

O maior erro foi que duas partes importantes do nosso código (as classes *`World`* e *`Game`*) ficaram grudadas demais. Isso quer dizer que, para mexer em uma, a gente tinha que mexer na outra, o que gerava muitos problemas.

Esse erro ficou claro na hora de juntar o trabalho de todo mundo (usando o Git). As junções de código davam muitos conflitos e eram muito difíceis de resolver.

Para consertar, nós paramos para 'arrumar' o código e 'soltar' as partes que estavam grudadas. O objetivo foi deixar elas mais independentes. Também organizamos melhor a forma como usamos o Git, criando regras mais claras para evitar bagunça.

### **Maior desafio**

O maior desafio foi no começo do projeto, na hora de planejar como o código seria montado. A forma como pensamos as coisas no início não funcionou bem quando o projeto começou a crescer e a ficar mais complexo.

Para resolver, nós estudamos como outros projetos organizavam o código e decidimos consertar o nosso aos poucos, sem precisar começar tudo do zero. Fomos arrumando parte por parte para que o projeto pudesse continuar evoluindo.

### **Lições aprendidas**

* **A importância do Planejamento e Design:** A principal lição foi a necessidade de investir mais tempo e esforço no **planejamento da arquitetura do software**. Um design bem pensado no início do projeto evita retrabalhos e problemas de manutenção no futuro.
* **Gestão de Código (Git):** Aprendemos que um **fluxo de trabalho com Git bem definido e praticado por toda a equipe** é fundamental para a colaboração. A falha nos merges nos mostrou a importância de commits atômicos e da comunicação clara sobre as mudanças de código.
* **Refatoração Contínua:** Descobrimos que a **refatoração não é uma tarefa opcional**, mas sim uma prática contínua para manter a saúde do código. É melhor corrigir pequenos problemas de design assim que eles aparecem do que esperar que eles se tornem grandes e complexos.

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
