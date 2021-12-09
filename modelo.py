from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, DateTime, Integer, Column, create_engine, ForeignKey
from sqlalchemy.orm import relationship, backref
import os

Base = declarative_base()


class Projetos(Base):
    __tablename__ = 'projetos'

    id_projeto = Column(Integer(), primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    data_modificacao = Column(DateTime(), nullable=False)

    def __repr__(self) -> str:
        return f'''Projetos(nome={self.nome}, data_criacao={self.data_criacao})'''


class Arquivos(Base):
    __tablename__ = 'arquivos'

    id_arquivo = Column(Integer(), primary_key=True)
    id_projeto = Column(Integer(), ForeignKey(
        'projetos.id_projeto'), nullable=False)
    nome = Column(String(100), nullable=False, index=True)
    caminho = Column(String(), nullable=False, index=True)
    data_modificacao = Column(DateTime(), nullable=False)

    projetos = relationship('Projetos', backref=backref(
        'arquivos', order_by=id_arquivo))

    def __repr__(self) -> str:
        return f'''Arquivos(id_projeto={self.id_projeto},nome={self.nome},caminho={self.caminho},data_modificacao={self.data_modificacao})'''


if os.path.isfile('db.sqlite3'):
    os.unlink('db.sqlite3')

engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(engine)
