#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import popen, path
from subprocess import call
from datetime import datetime
from argparse import ArgumentParser

NOW = datetime.now()
SIM = ('y', 'Y', 's', 'S')

# variáveis padrão de backup automático
nome_particao_backup = '/dev/sda5'
ponto_montagem = ''
pasta_backup = 'backup'
lista_arquivos = ('/home/paulo/.vimrc',
                  '/home/paulo/backup_vim',
                  '/home/paulo/Calibre Library',
                  '/home/paulo/Documents',
                  '/home/paulo/Downloads',
                  '/home/paulo/faculdade',
                  '/home/paulo/NetBeansProjects',
                  '/home/paulo/pc',
                  '/home/paulo/Pictures')


def remover_caracter_final(texto, caracter='/'):
    if texto.endswith(caracter):
        texto = texto.rstrip(caracter)
    return texto


def capturar_argumentos(nome_particao_backup, pasta_backup, lista_arquivos, ponto_montagem):
    parser = ArgumentParser(description='Automatização de backup de arquivos.'
                                        'Será necessário permissão de administrador para efetuar o backup.')
    parser.add_argument('-n',
                        action='store',
                        type=str,
                        dest='nome_particao_backup',
                        default='',
                        help='Nome do dispositivo referente a partição para backup(ex: -n /dev/sda1), '
                             'padrão: {}. OBS: Captura o ponto de montagem automaticamente, ignorando o parâmetro -m.'.format(nome_particao_backup))
    parser.add_argument('-m',
                        action='store',
                        type=str,
                        dest='ponto_montagem',
                        default='',
                        help='Nome do ponto de montagem referente a partição para backup(ex: -m /media/paulo/bk), '
                             'padrão: {}'.format(ponto_montagem))
    parser.add_argument('-p',
                        action='store',
                        type=str,
                        dest='pasta_backup',
                        default='',
                        help='Nome da pasta destino para o backup(ex: -p backup), '
                             'padrão: {}'.format(pasta_backup))
    parser.add_argument('-a',
                        action='store',
                        type=str,
                        dest='lista_arquivos',
                        default='',
                        help='Lista de arquivos para backup(ex: -a unix.txt,linux.sh,darwin.c), '
                             'padrão: {}'.format(lista_arquivos))

    args = parser.parse_args()

    if args.ponto_montagem:
        temp = remover_caracter_final(args.ponto_montagem)
        ponto_montagem = temp

    if args.nome_particao_backup:
        temp = remover_caracter_final(args.nome_particao_backup)
        nome_particao_backup = temp
        ponto_montagem = ''

    if args.pasta_backup:
        temp = args.pasta_backup
        if temp.startswith('/'):
            temp = temp.lstrip('/')
        pasta_backup = temp

    if args.lista_arquivos:
        temp = args.lista_arquivos.split(',')
        lista_arquivos = temp


def testar_variaveis_backup(nome_particao_backup: str, pasta_backup: str, lista_arquivos: tuple):
    # testando formato das variáveis nome_particao_backup e lista_arquivos
    # testando se existe os arquivos/pastas informadas
    assert isinstance(nome_particao_backup, str), 'Formato do nome da partição inválido, requer uma string.'
    assert isinstance(pasta_backup, str), 'Formato do nome da pasta de backup inválido, requer uma string.'
    assert isinstance(lista_arquivos, (list, tuple)), 'Formato da lista de arquivos inválida, requer uma list ou tuple'
    for i in lista_arquivos:
        assert isinstance(i, str), '{}, Formato do item da lista inválido'.format(i)

        assert path.exists(i), '{} não existe'.format(i)


def confirmar_mensagem(mensagem: str, caracteres_sim):
    return True if input(mensagem)[0] in caracteres_sim else False


def confirmar_backup(lista_arquivos: tuple, caracteres_sim):
    print('Lista de arquivos/pastas para backup:', *lista_arquivos, sep='\n')
    return confirmar_mensagem('Fazer backup dos arquivos e pastas apresentados [S/n]? ', caracteres_sim)


def efetuar_backup(diretorio_backup: str, lista_arquivos: tuple):
    for arquivo in lista_arquivos:
        # executando a cópia dos arquivos/pastas informados em lista_arquivos
        if ' ' in arquivo:
            arquivo = arquivo.replace(' ', '\ ')

        comando = 'sudo cp -vr {} {}'.format(arquivo, diretorio_backup)
        call(comando, shell=True)


def verificar_particao(nome_particao_backup: str):
    # testando existencia da partição informada
    if ponto_montagem:
        return popen('df|grep {}'.format(ponto_montagem)).readlines()
    else:
        return popen('df|grep {}'.format(nome_particao_backup)).readlines()


def extrair_ponto_montagem(verif_particao: list):
    if ponto_montagem:
        return ponto_montagem
    else:
        return str(verif_particao[0]).split(' ')[-1][:-1]


def verificar_diretorio_backup(ponto_montagem: str, pasta_backup: str, horario_atual, caracteres_sim):
    # verificando existência de pasta de backup, caso for informada
    diretorio_backup = '{0}/{2:%Y}{2:%m}{2:%d}_{1}'.format(ponto_montagem, pasta_backup, horario_atual)
    if path.exists(diretorio_backup):
        return diretorio_backup
    else:
        if confirmar_mensagem('Criar a pasta de backup {} [S/n]? '.format(diretorio_backup), caracteres_sim):
            call('sudo mkdir {}'.format(diretorio_backup), shell=True)
            return diretorio_backup
        else:
            raise ValueError('%s não existe' % diretorio_backup)


def verificar_backup_efetuado(diretorio_backup: str, lista_arquivos: tuple, confirmacao: str='OK', negacao: str='X'):
    print('\nVerificando arquivos/diretórios copiados:')
    for arquivo in lista_arquivos:
        arquivo = remover_caracter_final(arquivo)
        destino = '{}/{}'.format(diretorio_backup, arquivo.split('/')[-1])
        print('{}: {}'.format(destino, confirmacao if path.exists(destino) else negacao))

if __name__ == '__main__':
    capturar_argumentos(nome_particao_backup, pasta_backup, lista_arquivos, ponto_montagem)

    testar_variaveis_backup(nome_particao_backup, pasta_backup, lista_arquivos)

    if confirmar_backup(lista_arquivos, SIM):
        verif_particao = verificar_particao(nome_particao_backup)
        if verif_particao:
            ponto_montagem = extrair_ponto_montagem(verif_particao)

            diretorio_backup = verificar_diretorio_backup(ponto_montagem, pasta_backup, NOW, SIM)

            efetuar_backup(diretorio_backup, lista_arquivos)

            verificar_backup_efetuado(diretorio_backup, lista_arquivos)

        else:
            temp = nome_particao_backup if not ponto_montagem else ponto_montagem
            print('NÃO encontrou partição',
                  'Monte a partição {} ou'.format(temp),
                  'Modifique a variável interna nome_particao_backup ou',
                  'Informe outro dispositivo/partição no parâmetro -n ou -m', sep='\n')
