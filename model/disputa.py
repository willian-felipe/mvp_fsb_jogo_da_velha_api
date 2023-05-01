from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Disputa(Base):
    __tablename__ = 'disputa'

    id = Column(Integer, primary_key=True)
    nomeX = Column(String(50))
    pontosX = Column(Integer, default=0)
    nomeO = Column(String(50))
    pontosO = Column(Integer, default=0)
    velha = Column(Integer, default=0)
    data_criacao = Column(DateTime, default=datetime.now())
    ultima_alteracao = Column(DateTime, default=datetime.now())

    def __init__(self, nomeX:str, nomeO:str, pontosX:int = 0, pontosO: int = 0, velha:int = 0, 
                 data_criacao:Union[DateTime, None] = None, ultima_alteracao:Union[DateTime, None] = None):
        """
        Cria um disputa

        Arguments:
            nomeX: nomeX do jogador de 'X'
            pontosX: pontosX do jogador de 'X'
            nomeO: nomeO do jogador de 'O'
            pontosO: pontosO do jogador de 'O'
            velha: pontos da velha
            data_criacao: data de quando o disputa foi iniciada
            ultima_alteracao: data da ultima alteração que ocorreu na disputa
        """
        self.nomeX = nomeX
        self.pontosX = pontosX
        self.nomeO = nomeO
        self.pontosO = pontosO
        self.velha = velha

        if data_criacao:
            self.data_criacao = data_criacao
        if ultima_alteracao:
            self.ultima_alteracao = ultima_alteracao

