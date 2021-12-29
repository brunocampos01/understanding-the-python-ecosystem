## Tutorias em Python
***

Todo conteúdo aqui inserido é para fins de estudo e consulta, não tendo fins lucrativos, foi retirado de N fontes da internet incluindo video aulas do Youtube até conteúdo de cursos realizados e livros.

***
#### Instalação
***

Para instalar o notebook jupyter primeiro devemos ter o python3 instalado e o pip3, com o pip3 instalado execute o comando:

```sh
sudo apt-get install python3-pip python3-jupyter python3-numpy python3-scipy python3-matplotlib
```

* Se precisar use o sudo na frente

* **Referências**:

    - [Jupyter](http://jupyter.org/)
    - [Como funciona o jupyter notebook](https://www.youtube.com/watch?v=xuahp9g3Dic)
    - [Documentação](http://jupyter-notebook.readthedocs.io/en/latest/)

* Com o jupyter instalado rode ele na pasta que você desejar:

    ```sh
    jupyter notebook
    ```

* Roda qualquer comando no python pelo terminal:

    ```sh
    pip3 install ipython
    python3
    ```

***
#### O que é o notebook jupyter
***

O notebook amplia a abordagem baseada em console para a computação interativa em uma direção qualitativamente nova, fornecendo uma aplicação
baseada na web adequada para capturar todo o processo de computação: desenvolver, documentar e executar o código, bem como comunicar os
resultados. O notebook Jupyter combina dois componentes:

* **Um aplicativo web**: uma ferramenta baseada em navegador para criação interativa de documentos que combinam texto explicativo, matemática,
  cálculos e sua saída de midia rica.

* **Documentos Notebooks**: uma representação de todos os conteúdos visíveis no aplicativo da Web, incluindo entradas e saídas dos cálculos, texto
  explicativo, matemática, imagens e representações de objetos em midia rica.

Os documentos notebooks contém as entradas e saídas de uma sessão interativa, bem como texto adicional que acompanha o código, mas não é para
execução. Desta forma, os arquivos de caderno podem servir como um registro computacional completo de uma sessão, intercalando o código
executável com texto explicativo, matemática e ricas representações de objetos resultantes. Esses documentos são internamente arquivos JSON e são
salvos com a extensão .ipynb. Como o JSON é um formato de texto simples, eles podem ser controlados por versão e compartilhados com colegas.

***
#### Modo de comandos (ESC)
***

|Comando|Descrição|
|:-----:|:--------|
|ENTER|Move para o modo de edição|
|Shift + Enter|Executa cada uma das celulas/linhas do notebook e passa para a linha abaixo|
|Ctrl + Enter|Executa a celula/linha atual|
|Alt + Enter|Executa a celular/linha e cria uma nova abaixo|
|F|Encontrar e modificar/trocar|
|Y|Para codificar|
|M|Para markdown|
|R|Para texto normal|
|A|Inserir celula acima|
|B|Inserir celula abaixo|
|X|Corta celula|
|C|Copiar celula|
|V|Colar celula|
|DD|Deletar celula|
|1|cabeçalho de tamanho gigante, **1**,2,3,4,5,6|
|6|cabeçalho de tamanho pequeno, 1,2,3,4,5,**6**|
|Shift + UP|Selecionar a celula acima|
|Shift + DOWN|Selecionar a celula abaixo|
|Shift + M|Mesclar celulas selecionadas|
|Ctrl + S|Salvar|

***
#### Modo de edição (ENTER)
***

|Comando|Descrição|
|:-----:|:--------|
|ESC|Move para o modo de comandos|
|TAB|Identar ou autocompletar código|
|Ctrl + A|Selecionar todos|
|Ctrl + UP|Ir para a primeira celula|
|Ctrl + DOWN|Ir para a ultima celula|

***
#### Simbolos matematicos ($$)
***

![math1](https://cloud.githubusercontent.com/assets/14116020/26659341/62d9d082-4646-11e7-9c9e-19c352112968.png)

![math2](https://cloud.githubusercontent.com/assets/14116020/26659348/6db51ef8-4646-11e7-8617-07f6df4312e6.png)

![math3](https://cloud.githubusercontent.com/assets/14116020/26659349/70272fdc-4646-11e7-9965-64664aa4225b.png)

![math4](https://cloud.githubusercontent.com/assets/14116020/26659352/727f73fc-4646-11e7-9586-b6187c9d83dd.png)

![math5](https://cloud.githubusercontent.com/assets/14116020/26659354/74fb7ffe-4646-11e7-90aa-f72245ca4494.png)

![math6](https://cloud.githubusercontent.com/assets/14116020/26659356/7698fc2e-4646-11e7-86f2-1b08c2dba0fb.png)

***
#### Referências
***

* **Python**: Video aulas do Udemy e do canal do Youtube (ignorância zero)

* **Métodos Númericos**: https://github.com/fabiommendes/numericos-pub
