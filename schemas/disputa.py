from pydantic import BaseModel
from typing import Optional, List
from model.disputa import Disputa

class DisputaInitSchema(BaseModel):
    """ Define como uma nova disputa deve ser iniciada 
    """
    nomeX: str = "Felipe"
    nomeO: str = "Willian"




class DisputaSchema(BaseModel):
    """ Define como um modelo base da tabela de disputa será representada
    """
    id: int = 1
    nomeX: str = "Felipe"
    pontosX: int = 3
    nomeO: str = "Willian"
    pontosO: int = 5
    velha: int = 2

class DisputaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da disputa.
    """
    id: int = 0


class ListagemDisputasSchema(BaseModel):
    """ Define como uma listagem de disputas será retornada.
    """
    disputas:List[DisputaSchema]


def apresenta_disputas(disputas: List[Disputa]):
    """ Retorna uma lista de representação seguindo o schema definido em
        DisputaViewSchema.
    """
    result = []
    for item in disputas:
        result.append({
            "id": item.id,
            "nomeX": item.nomeX,
            "pontosX": item.pontosX,
            "nomeO": item.nomeO,
            "pontosO": item.pontosO,
            "velha": item.velha
        })

    return {"disputas": result}


class DisputaViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    nomeX: str = "Felipe"
    pontosX: int = 3
    nomeO: str = "Willian"
    pontosO: int = 5
    velha: int = 2
    # data_criacao: disputa.data_criacao,
    # ultima_alteracao: disputa.ultima_alteracao


class DisputaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    id: int

def apresenta_disputa(disputa: Disputa):
    """ Retorna uma representação da disputa seguindo o schema definido em
        DisputaViewSchema.
    """
    return {
        "id": disputa.id,
        "nomeX": disputa.nomeX,
        "pontosX": disputa.pontosX,
        "nomeO": disputa.nomeO,
        "pontosO": disputa.pontosO,
        "velha": disputa.velha,
        "data_criacao": disputa.data_criacao,
        "ultima_alteracao": disputa.ultima_alteracao
    }
