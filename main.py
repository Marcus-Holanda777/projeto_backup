import os
from datetime import datetime
from modelo import engine, Projetos, Arquivos
from sqlalchemy.orm import sessionmaker
import shutil

Session = sessionmaker(bind=engine)
session = Session()

root = os.path.join('..')

lista_projetos = ['lista de projetos']
pasta_bk = r'D:\Bk_projetos_novo'

for projeto in lista_projetos:
    cam = os.path.join(root, projeto)
    dt_criacao = datetime.fromtimestamp(os.path.getmtime(cam))

    ins = Projetos(nome=projeto, data_modificacao=dt_criacao)
    session.add(ins)
    session.commit()

    for pasta, sub, arq in os.walk(cam):
        for a in arq:
            comp_arq = os.path.join(pasta, a)

            print(comp_arq)

            ins_arq = Arquivos(
                id_projeto=ins.id_projeto, nome=a, caminho=comp_arq, data_modificacao=datetime.fromtimestamp(
                    os.path.getmtime(comp_arq))
            )

            session.add(ins_arq)
            session.commit()


query = session.query(Projetos)

for row in query:
    print(f'Copiando: {row.nome}')
    origem = os.path.join(root, row.nome)
    novo_projeto = os.path.join(pasta_bk, row.nome)

    shutil.copytree(origem, novo_projeto, dirs_exist_ok=True)

saida_banco = 'db_{0}_.sqlite3'.format(
    str(datetime.fromtimestamp(os.path.getmtime('db.sqlite3'))).replace(':', '.'))
shutil.copy('db.sqlite3', os.path.join(pasta_bk, saida_banco))

print('')
print('=*' * 50)
print(saida_banco)
print('*=' * 50)
