# Autor: Micael Muniz de Oliveira Santos
# Componente Curricular: Algoritmos I
# Concluído em: 02/07/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.


import os
import user_interface as ui
from pickle import dump, load

'''
file_management.py é um módulo que realiza as operações CRUD requisitadas pelo usuário no main.py, em caso de ser
necessário printar algo mais complexo, coleta as informações necessárias e a passa para o módulo user_interface.py
'''

# O dicionário onde são armazenados os dados na forma de ÍNDICE INVERTIDO: a variável "inverted".
inverted = {}


'''
FOLDER: O programa utiliza objetos da classe DirEntry da biblioteca os, objetos gerado a partir do fornecimento de um 
diretorio à função os.scandir, que retorna uma lista de objetos com tudo que contêm na pasta, com atributos como path e 
name, porém essa função não aceita caminhos diretos para arquivos, então a classe Folder possui os mesmos atributos de 
name e path, sendo utilizada para esses casos especiais, permitindo o re-uso das funções que já trabalham com o DirEntry.
'''

class Folder(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path


# ======= FUNÇÕES AUXILIARES =======

# Função extra da funcionalidade "remover tudo".
def clear_cache():
    os.remove('.cache.dat')


# A primeira operação realizada, carregar os dados do índice invertido, caso existam, chamados cache.
if os.path.exists(".cache.dat"):
    with open(".cache.dat", "rb") as cache:
        inverted = load(cache)


# Tenta abrir o arquivo de maneira segura, caso não seja possível, ou esteja corrompido, ignora o arquivo.
def open_file(path):
    try:
        temp_file = open(path, encoding="utf8")
    except:
        pass
    else:
        with temp_file:
            return temp_file.read().lower()


# Verifica se tem uma palavra na string txt, se tiver, diz quantas vezes, se não tiver, diz que tem 0 vezes.
def count_word(value, txt):
    if value in txt:
        return txt.count(value)
    else:
        return 0


# Salva o índice invertido como arquivo binário, chamado de ".cache.dat" na pasta raiz do programa.
def save(dict=inverted):
    with open(".cache.dat", "wb") as cache:
        dump(dict, cache)


# Chama o "user_interface" para mostrar o índice invertido, caso tenha algo no índice, (comando VER).
def show_files():
    if len(inverted) > 0:
        #print(inverted)
        ui.word_index(inverted.keys(), inverted)
    else:
        print('Não existem arquivos carregados!')


# Chama o "user_interface" para mostrar em quais arquivos ocorre uma determinada palavra, (comando PROCURAR).
def show_word(word):
    # Sorted + key=lambda envia os itens ordenados por OCORRÊNCIA, assim, a função "word_spreadsheet" já lê ordenado.
    ui.word_spreadsheet(sorted(inverted[word], key=lambda occurrences: occurrences[1], reverse=True), word)


# Cria uma lista de objetos do tipo DirEntry, com o conteúdo de uma pasta, passada como caminho.
def generate_direntry(path, special_case=None):
    # Path = caminho da pasta
    # special_case = situações que não quero uma lista de objetos, mas sim uma lista de nomes ou caminhos de arquivos.
    folders = os.scandir(path)
    files = []
    for folder in folders:
        if folder.is_file() and os.path.splitext(folder.path)[1] == '.txt' and not special_case:
            files.append(folder)
        elif special_case == 'path':
            files.append(folder.path)
        elif special_case == 'name':
            files.append(folder.name)
    return files


# ======= FUNÇÕES PRINCIPAIS =======

# Cria o índice invertido ou atualiza ele (update=True), no caso de atualização, nada mais é do que reCRIAR o índice.
def inverted_index(path, update=False):
    # Caso 1: atualização, como já é conhecido pelo programa o que atualizar, ele trabalha com uma lista de caminhos e
    # simula uma lista de objetos da classe DirEntry com esses caminhos, usando a classe Folder.
    if update:
        files = []
        for item in path:
            file = Folder(os.path.split(item)[1], item)
            files.append(file)
    else:
        name = os.path.split(path)[1]
        format = os.path.splitext(path)[1]
        # Caso 2: criação, foi fornecido o caminho de um txt, é necessario simular uma lista DirEntry de UM elemento.
        if format == '.txt':
            file = Folder(name, path)
            files = [file]
        # Caso 3: foi fornecido de fato um diretório desconhecido, é gerado uma lista de objetos DirEntry deste caminho.
        else:
            files = generate_direntry(path)

    # Na criação do indice invertido ele vai verificar palavra por palavra, se uma palavra já existir, ele verifica se
    # o arquivo que ela veio também é o mesmo, se for, é um caso de atualização, fica guardao nesta lista para o final.
    files_to_update = []

    # Criação do índice invertido
    for file in files:
        new_file = True
        text = open_file(file.path)
        # Filtros do que significa uma nova palavra, virgulas, espaços e quebras de linha.
        text = text.replace(',', ' ')
        text = text.replace('\n', ' ')
        text = text.split(' ')
        for word in text:
            if word != '':
                name = file.name
                occurrences = count_word(word, text)
                absolute_path = os.path.abspath(file.path)
                file_size = os.path.getsize(file.path)
                folder = os.path.split(os.path.split(file.path)[0])[1]
                # Caso 1: palavra nova, cria ela.
                if word not in inverted.keys():
                    inverted[word] = [[name, occurrences, file_size, absolute_path, folder]]
                    new_file = False
                # Caso 2: palavra já conhecida, porém referência (arquivo onde está) nova, adiciona à palavra já existente.
                elif not file.path in [i[3] for i in inverted[word]]:
                    inverted[word].append([name, occurrences, file_size, absolute_path, folder])
                    new_file = False
                # Caso 3: palavra já conhecida na mesma referência, é necessário remover e adicionar novamente (atualizar).
                elif not update and new_file:    # SOMENTE caso já não esteja atualizando, se não vira um loop infinito.
                    if absolute_path not in files_to_update:
                        files_to_update.append(absolute_path)

    # Se existir algo na lista de atualizações, inicia a atualização, que se trata de chamar a função de remover,
    # passando a lista de repetidos, e chamando novamente a função de criar o índice, passando a lista de repetidos
    if len(files_to_update) > 0:
        #print(files_to_update)
        # Print customizado
        amount = len(files_to_update)
        label = ui.get_label('update', amount)
        print(f'Verificando mudanças em {amount} {label[0]} previamente {label[1]}.')
        # Chama as funções que já existem, porém atributos pré definidos como None ou False, viram True e passam valor
        # caindo nos "casos especiais" dessas funções
        remove_path(path=None, files_list_already_defined=files_to_update)  # files_list... de None, passa a lista, no caso especial.
        inverted_index(files_to_update, update=True)    # Update, de False, por padrão, vira True no caso especial.


# Função extra de remover uma palavra: deleta ela do dicionário. (Comando REMOVER PALAVRA)
def remove_word(word):
    if word in inverted.keys():
        inverted.pop(word)
        print('Palavra removida com sucesso!')
        save()
    else:
        print('Erro! A palavra não existe nos dados carregados.')


# Remove todas as referências á uma palavra de um arquivo, ou pasta de arquivos.
# A função remove_path, por padrão, gera uma lista de caminhos para remover, porém, no caso especial, essa lista já foi
# gerada por alguma outra função, então recebe essa lista e reaproveita a mesma.
def remove_path(path, files_list_already_defined=None):
    # Backup do indice feito para evitar o erro "RuntimeError: dictionary changed size during iteration"
    # Como ".copy" não funciona muito bem aqui, já que recria o dicionaro, mas os elementos dele são os mesmos ponteiros
    # i.e., as listas da matriz no dicionário, apontando para o mesmo endereço na memória, precisa recriar totalmente.
    backup_index = {key: value[:] for key, value in inverted.items()}

    # Caso 1: caminho passado é direto para um .txt, cria uma lista com UM elemento, o proprio endereço.
    if not files_list_already_defined and os.path.splitext(path)[1] == '.txt':
        files_to_del = [path]
    # Caso 2: caminho passado é um diretorio, é necessario obter uma lista de todos os caminhos de todos os arquivos dele.
    elif not files_list_already_defined:
        files_to_del = generate_direntry(path, special_case='path')
    # Caso especial: files_list_already_defined != None, a lista já foi gerada por outra função, reutiza ela.
    else:
        files_to_del = files_list_already_defined

    # Remover palavras do índice invertido
    for word in backup_index.keys():                  # verifica cada palavra do índice
        for file_in_index in backup_index[word]:      # verifica cada elemento da palavra (cada lista da matriz)
            if file_in_index[3] in files_to_del:      # verifica se o endereço, na lista do arquivo, está na lista negra
                inverted[word].remove(file_in_index)  # remove a lista que representa o arquvio da matriz no indice REAL
        if len(inverted[word]) < 1:                   # caso tudo seja removido da matriz, deleta a key do dicionário
            inverted.pop(word)
    if not files_list_already_defined:                # a mensagem de remoção não é mostrada pro usuário no caso especial
        print('O diretório foi removido!')            # já que é uma função conversando com outra, por baixo dos panos.
