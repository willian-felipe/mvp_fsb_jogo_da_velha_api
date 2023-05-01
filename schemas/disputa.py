from pydantic import BaseModel
from typing import Optional, List
from model.disputa import Disputa

class DisputaInitSchema(BaseModel):
    """ Define como uma nova disputa deve ser iniciada 
    """
    nomeX: str = "Felipe"
    nomeO: str = "Willian"




class DisputaSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50


class DisputaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"


class ListagemDisputasSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[DisputaSchema]


# def apresenta_produtos(produtos: List[Produto]):
#     """ Retorna uma representação do produto seguindo o schema definido em
#         ProdutoViewSchema.
#     """
#     result = []
#     for produto in produtos:
#         result.append({
#             "nome": produto.nome,
#             "quantidade": produto.quantidade,
#             "valor": produto.valor,
#         })

#     return {"produtos": result}


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


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_disputa(disputa: Disputa):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
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
