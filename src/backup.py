#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import popen, path
from subprocess import call

nome_particao_backup = '/dev/sda5'
pasta_backup = ''
lista_arquivos = ('/home/paulo/.vimrc',
                  '/home/paulo/backup_vim',
                  '/home/paulo/Calibre Library',
                  '/home/paulo/Documents',
                  '/home/paulo/Downloads',
                  '/home/paulo/faculdade',
                  '/home/paulo/NetBeansProjects',
                  '/home/paulo/pc',
                  '/home/paulo/backup_vim',
                  '/home/paulo/Pictures')

# testando formato das variáveis nome_particao_backup e lista_arquivos
# testando se existe os arquivos/pastas informadas
assert isinstance(nome_particao_backup, str), 'Formato do nome da partição inválido, requer uma str.'
assert isinstance(nome_particao_backup, str), 'Formato do nome da pasta de backup inválido, requer uma str.'
assert isinstance(lista_arquivos, (list, tuple)), 'Formato da lista de arquivos inválida, requer uma list ou tuple'
for i in lista_arquivos:
    assert isinstance(i, str), 'Formato do item da lista inválido'

    assert path.exists(i), '%s não existe' % i


verif_particao = popen('df|grep %s' % nome_particao_backup).readlines()
if verif_particao:
    ponto_montagem = str(verif_particao[0]).split(' ')[-1][:-1]

    diretorio_backup = '%s/%s' % (ponto_montagem, pasta_backup)
    assert path.exists(diretorio_backup), '%s não existe' % diretorio_backup

    for arquivo in lista_arquivos:
        call('sudo cp -vr %s %s' % (arquivo, diretorio_backup), shell=True)

else:
    print('NÃO encontrou partição', 'Monte a partição %s ou' % nome_particao_backup,
          'Modifique a variável interna nome_particao_backup', sep='\n')