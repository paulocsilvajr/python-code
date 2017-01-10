#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import popen, path
from subprocess import call

# variáveis de backup automático
nome_particao_backup = '/dev/sda5'
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

# testando formato das variáveis nome_particao_backup e lista_arquivos
# testando se existe os arquivos/pastas informadas
assert isinstance(nome_particao_backup, str), 'Formato do nome da partição inválido, requer uma string.'
assert isinstance(pasta_backup, str), 'Formato do nome da pasta de backup inválido, requer uma string.'
assert isinstance(lista_arquivos, (list, tuple)), 'Formato da lista de arquivos inválida, requer uma list ou tuple'
for i in lista_arquivos:
    assert isinstance(i, str), '{}, Formato do item da lista inválido'.format(i)

    assert path.exists(i), '{} não existe'.format(i)

print('Lista de arquivos/pastas para backup:', *lista_arquivos, sep='\n')
confirmacao_backup = True if input('Fazer backup dos arquivos e pastas apresentados[S/n]: ')[0] \
                             in ('y', 'Y', 's', 'S') else False
if confirmacao_backup:
    # testando existencia da partição informada
    verif_particao = popen('df|grep %s' % nome_particao_backup).readlines()
    if verif_particao:
        ponto_montagem = str(verif_particao[0]).split(' ')[-1][:-1]

        # verificando existência de pasta de backup, caso for informada
        diretorio_backup = '%s/%s' % (ponto_montagem, pasta_backup)
        assert path.exists(diretorio_backup), '%s não existe' % diretorio_backup

        for arquivo in lista_arquivos:
            # executando a cópia dos arquivos/pastas informados em lista_arquivos
            if ' ' in arquivo:
                arquivo = arquivo.replace(' ', '\ ')

            comando = 'sudo cp -vr {} {}'.format(arquivo, diretorio_backup)
            a = input('{}: '.format(comando))
            call(comando, shell=True)

        print('\n\n')
        for arquivo in lista_arquivos:
            destino = '{}/{}'.format(diretorio_backup, arquivo.split('/')[-1])
            print('{}: {}'.format(destino, 'OK' if path.exists(destino) else 'X'))

    else:
        print('NÃO encontrou partição', 'Monte a partição {} ou'.format(nome_particao_backup),
              'Modifique a variável interna nome_particao_backup', sep='\n')
