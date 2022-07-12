# Autor: Micael Muniz de Oliveira Santos
# Componente Curricular: Algoritmos I
# Concluído em: 02/07/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.


'''
user_interface.py é um módulo que realiza as impressões de mensagems mais complexas, geralmente em ASCII, também resolve
problemas relacionados a string dando-lhes uma label, com a função get_label.
'''


# Mensagem de ajuda ao utilizar o comando AJUDA
def help():
    print(f'┌───────────────────────────────────────────────────────────┐\n'
          f'│{f"Lista de comandos para navegação e gerenciamento da busca":^59}│\n'
          f'├───────────────────┬───────────────────────────────────────┤\n'
          f'│      COMANDO      │               O QUE FAZ               │\n'
          f'├───────────────────┼───────────────────────────────────────┤\n'
          f'│     adicionar     │ Carrega todos .txt daquele diretório  │\n'
          f'│        ver        │ Exibe todas palavras e às suas origens│\n'
          f'│       ajuda       │ Exibe uma tabela com todos os comandos│\n'
          f'│   remover tudo    │ Limpa todos os dados já carregados    │\n'
          f'│  remover palavra  │ Remove uma palavra e suas referências │\n'
          f'│ remover diretorio │ Remove da busca todos txt do diretório│\n'
          f'└───────────────────┴───────────────────────────────────────┘')


# Monta um ASCII de pastas, porém só foi utilizado para mostrar as palavras do índice e quais informações carregam
def word_index(words, inverted_index):
    if len(words) == 1:
        print(f' └─{inverted_index}')
    else:
        for index, item in enumerate(words):
            elbow = ' └─'
            tee = ' ├─'
            inside_elbow = ' │   └─'
            inside_tee = ' │   ├─'
            last_inside_elbow = '     └─'
            last_inside_tee = '     ├─'
            if index == len(words) - 1:
                fitting = elbow
            else:
                fitting = tee
            print(f'{fitting}{item}')
            for inside_index, inside_item in enumerate(inverted_index[item]):
                if inside_index == len(inverted_index[item]) - 1:
                    if index == len(words) - 1:
                        fitting = last_inside_elbow
                    else:
                        fitting = inside_elbow
                else:
                    if index == len(words) - 1:
                        fitting = last_inside_tee
                    else:
                        fitting = inside_tee
                print(f'{fitting}{inside_item}')


# Elementos onde o texto muda dependendo da situação, utilizam dessa função para obter uma label / string para cada caso
def get_label(what_for, value):
    # Label do tamanho dos arquivos, se for muito grande vai de bytes para kilobytes, depois megabytes...
    if what_for == 'size':
        size_string_len = len(str(value))
        if size_string_len > 6:
            size_label = '+ de 1mb'
        elif size_string_len > 5:
            value = value / 1000
            size_label = f'{round(value, 2)}kb'
        elif size_string_len > 4:
            value = value / 1000
            size_label = f'{round(value, 2)} kb'
        elif size_string_len > 3:
            value = value / 1000
            size_label = f'{round(value, 3)} kb'
        else:
            size_label = f'{value} b'
        return size_label

    # Label do nome da pasta / arquivo, se for muito grande o nome, a ponto de quebrar o ASCII da tabela, reduz o nome
    if what_for == 'folder':
        folder_string_len = len(value)
        if folder_string_len > 36:
            folder_label = '...' + value[:33]
        else:
            folder_label = value
        return folder_label

    # Label para as ocorrências de uma palavra, caso seja mais de 1 vez, é chamado vezes, se for maior que 99, por exemplo:
    # algo como "9999283732167361236216", poluindo a UI, então nesses casos de números grandes só mostra como +99
    if what_for == 'occurrences':
        file_string_len = len(str(value))
        if file_string_len > 2:
            file_label = '+99vezes'
        elif value > 1:
            file_label = f'{value} vezes'
        else:
            file_label = f'{value} vez'
        return file_label

    # Se o mesmo arquivo tiver em 2 pastas diferentes, além do nome do arquivo é mostrado a pasta em que se encontra
    if what_for == 'duplicate':
        file = get_label("folder", value[0])
        folder = value[1]
        return f'/{folder}/{file}'

    # Label para plural e singular
    if what_for == 'update':
        if value > 1:
            return ('arquivos', 'carregados')
        else:
            return ('arquivo', 'carregado')


# Monta a tabela onde é mostrado quantas vezes a palavra aparece nos arquivos, em quais arquivos... (comando PROCURAR)
def word_spreadsheet(folders, word):
    print()
    print()
    print(f'┌───────────────────────────────────────────────────────────┐')
    print(f"│{f'OCORRÊNCIAS DA PALAVRA':^59}│")
    print(f"│{f'{word.upper()}':^59}│")
    # Sempre vai ter ao menos uma pasta, por isso ele por padrao ja imprime o primeiro desenho com os elementos 0
    occurrences = get_label('occurrences', folders[0][1])
    size_label = get_label('size', folders[0][2])
    # Se o mesmo arquivo tiver em 2 pastas diferentes, além do nome do arquivo é mostrado a pasta em que se encontra
    if [i[0] for i in folders].count(folders[0][0]) > 1:
        file_label = get_label('folder', get_label('duplicate', (folders[0][0], folders[0][4])))
    else:
        file_label = get_label('folder', folders[0][0])
    print(f'├────┬────────────────────────────────────┬────────┬────────┤')
    print(f'│Rank│ Nome do arquivo                    │Tamanho │ Vezes  │')
    print(f'├────┼────────────────────────────────────┼────────┼────────┤')
    print(f'│ 1  │{file_label:<36}│{size_label:>8}│{occurrences:>8}│')
    # Se tiver mais de um arquivo, roda um for para buscar quais tem, se nao tiver, imprime a parte final da caixa
    # ja que o unico arquivo que tem, foi impresso na linha acima.
    if len(folders) != 1:
        for index, folder in enumerate(folders):
            # Pula o elemento 0 (primeiro arquivo), já que foi impresso lá em cima.
            if index > 0:
                occurrences = get_label('occurrences', folder[1])
                size_label = get_label('size', folder[2])
                # Se o mesmo arquivo tiver em 2 pastas diferentes, além do nome do arquivo é mostrado a pasta em que se encontra
                if [i[0] for i in folders].count(folder[0]) > 1:
                    file_label = get_label('folder', get_label('duplicate', (folder[0], folder[4])))
                else:
                    file_label = get_label('folder', folder[0])
                print(f'├────┼────────────────────────────────────┼────────┼────────┤')
                print(f'│{index + 1:^4}│{file_label:<36}│{size_label:>8}│{occurrences:>8}│')
    # Ao final do loop, fecha a tabela ASCII
    print('└────┴────────────────────────────────────┴────────┴────────┘')


# O comando remover possui 3 "subcomandos" por isso, caso a pessoa não entenda muito bem como utilizar e erre, imprime
# essa mensagem com ASCII
def help_remover():
    print(f'┌───────────────────────────────────────────────────────────┐\n'
          f'│{f"Como remover um arquivo, diretório ou palavra da busca":^59}│\n'
          f'├───────────────────────────────────────────────────────────┤\n'
          f'│{f" .─────._________       É possivel remover da busca uma  ":^59}│\n'
          f'│{f" |               |      palavra, um diretório ou arquivo.":^59}│\n'
          f'│{f" |    ───────────┴───   Para remover uma palavra use:    ":^59}│\n'
          f'│{f" |   /              /   >   remover palavra  *palavra*   ":^59}│\n'
          f'│{f" |  /              /    Para remover pasta / arquivo use:":^59}│\n'
          f'│{f" | /              /     >   remover diretório *caminho*  ":^59}│\n'
          f'│{f" |/______________/      Para remover tudo do cache use:  ":^59}│\n'
          f'│{f"                        >   remover tudo                 ":^59}│\n'
          f'└───────────────────────────────────────────────────────────┘\n')