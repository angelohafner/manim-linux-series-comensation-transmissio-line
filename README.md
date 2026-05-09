# Banco de Capacitor Serie em Linhas de Transmissao

Projeto em Python/Manim para gerar uma animacao didatica sobre compensacao serie em sistemas de potencia. O video explica, de forma visual, como um banco de capacitor serie reduz a reatancia equivalente da linha e aumenta a potencia transferivel.

## Objetivo

O projeto foi organizado para que usuarios tecnicos possam alterar dados de entrada, textos, cores, geometria e configuracoes de renderizacao sem precisar mexer na logica interna das cenas.

## Como alterar os dados de entrada

Edite apenas o arquivo `config.py`.

Ele centraliza:

- resolucao, FPS e cena padrao;
- textos exibidos nos slides;
- cores e estilo visual;
- simbolos eletricos em LaTeX;
- valores numericos das barras comparativas;
- geometria da linha de transmissao;
- dimensoes do capacitor, indutor e demais simbolos;
- espacamentos, escalas e tempos de animacao.

## Como executar

Para renderizar com a configuracao padrao:

```powershell
python main.py
```

Para renderizar em 1080p:

```powershell
python main.py --resolution 1920,1080 --fps 30
```

Para renderizar uma cena especifica:

```powershell
python main.py --scene FirstFourSlidesScene --resolution 426,240 --fps 15
```

Os nomes antigos das cenas continuam disponiveis em `banco_capacitor_serie.py` para compatibilidade com comandos Manim usados anteriormente.

## Estrutura do projeto

```text
main.py
config.py
banco_capacitor_serie.py
models/
calculators/
plotters/
exporters/
utils/
assets/
```

## Papel de cada pasta

- `main.py`: coordena o fluxo principal de renderizacao.
- `config.py`: contem todos os parametros editaveis pelo usuario.
- `banco_capacitor_serie.py`: expoe as cenas para o Manim e preserva nomes antigos.
- `models/`: dataclasses tipadas para configuracao e simbolos eletricos.
- `calculators/`: funcoes matematicas e algoritmos, como a catenaria.
- `plotters/`: componentes visuais e cenas Manim.
- `exporters/`: chamada ao Manim e controle de exportacao.
- `utils/`: validacoes e funcoes auxiliares reutilizaveis.
- `assets/`: arquivos externos, imagens e templates futuros.

## Como expandir

Para adicionar novos calculos, crie modulos em `calculators/`.

Para adicionar novos elementos visuais reutilizaveis, edite ou crie arquivos em `plotters/`.

Para adicionar novos parametros editaveis, comece por `config.py` e propague o valor pela estrutura tipada em `models/`.

Essa organizacao facilita futuras integracoes com notebooks Jupyter, GUI ou uma interface web.
