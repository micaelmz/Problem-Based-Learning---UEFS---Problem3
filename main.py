# Autor: Micael Muniz de Oliveira Santos
# Componente Curricular: Algoritmos I
# Concluído em: 02/07/2022
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.


import sys
import os
from pickle import dump, load
import user_interface as ui
import file_management as fm

'''
Sys.argv: 0 - main.py, 1 - comando, 2 - instruções (caminho ou comando secundario), 3 - quando existe, caminho
Comandos: adicionar, ver, procurar, ajuda, remover tudo, remover palavra, remover diretorio
'''


# ADICIONAR: recebe um endereço, seja ARQUIVO (.txt) ou diretorio que contenha os arquivos, verifica se está tudo ok, se
# estiver, envia o endereço para a função "inverted_index" em "file_management.py" que descobre se é um endereço novo
# (caso de adição), ou um endeço que contém arquivos já fornecidos anteriormente (caso de atualização do índice).
if sys.argv[1].lower() == 'adicionar':
    if len(sys.argv) < 3:
        print('Por favor, digite um endereço para ser carregado, em caso de dúvidas utilize o comando ajuda.')
    else:
        # Todo caminho é lido como um caminho absoluto
        path = os.path.abspath(sys.argv[2])
        print('Carregando documentos, aguarde...')
        try:
            fm.inverted_index(path)
            print('Os documentos foram carregados com sucesso!')
        except FileNotFoundError:
            print('Erro! Caminho não encontrado. Verifique o comando digitado e tente novamente.')
        except PermissionError:
            print('Erro! Acesso negado. O programa não pode abrir esta pasta, pois a mesma está protegida pelo sistema.')
        except NotADirectoryError:
            print('Erro! O diretório é invalido, verifique a caminho digitado.')
        except Exception as erro:
            print(f'Os documentos NÃO foram carregados, devido a um erro!\n{erro}')
    # Salva o indice em ".cache.dat"
    fm.save()


# VER: função extra, exibe para o usuário o índice, de uma maneira mais intuitiva que apenas printar o dicionário.
elif sys.argv[1].lower() == 'ver':
    fm.show_files()


# PROCURAR: busca uma palavra e em qual arquivo se encontra, ordenando os arquivos por ordem de ocorrência da palavra.
elif sys.argv[1].lower() == 'procurar':
    try:
        fm.show_word(sys.argv[2].lower())
    except:
        # Em caso de qualquer erro, o programa simplesmente diz que a palavra não existe (único caso de erro conhecido)
        print('A palavra não existe em nenhum arquivo carregado!')


# REMOVER: remove uma palavra indicada, diretório, ou tudo, deletando o arquivo ".cache.dat" que contem o índice
elif sys.argv[1].lower() == 'remover':
    if len(sys.argv) < 3:
        print('Erro! Comando invalido')
        ui.help_remover()
    else:
        if sys.argv[2].lower() == 'palavra':
            fm.remove_word(sys.argv[3])
        elif sys.argv[2].lower() == 'diretorio':
            path = os.path.abspath(sys.argv[3])
            fm.remove_path(path)
        elif sys.argv[2].lower() == 'tudo':
            try:
                fm.clear_cache()
                print('Os dados do programa foram limpos!')
                exit()
            except OSError:
                print("Erro! Não foi possivel deletar o arquivo \'.cache.dat\'")
        else:
            print('Erro! Comando invalido')
            ui.help_remover()
    fm.save()


# AJUDA: printa um tutorial de como utilizar o programa, não é possível pedir ajuda para um comando especifico, pelo
# motivo de que caso o usuário erre o comando, a função que ele tentou utilizar por padrão já printa uma ajuda.
elif sys.argv[1].lower() == 'ajuda':
    ui.help()


# Não caiu em nenhum caso acima, nenhum comando foi digitado ou não foi reconhecido pelo programa.
else:
    print('Comando inexistente, use o comando ajuda para obter a lista de comandos')
