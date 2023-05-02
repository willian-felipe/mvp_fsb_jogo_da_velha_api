from pydantic import BaseModel
from typing import Any, Optional, List
from schemas.disputa import DisputaViewSchema



class ChecaResultadoRequestSchema(BaseModel):
    """ Define como se encontra a partida e se houve algum vencedor.
    """
    jogo: List[str | None]
    disputa_id: int

class ChecaResultadoResponseSchema(BaseModel):
    """ Verifica se houve algum vencedor e informa o resultado atualizado.
    """
    jogo: List[str | None]
    # partida: Any
    partida: DisputaViewSchema | None
    vencedor: str | None
    finalizado: bool

def apresenta_resultado(result: ChecaResultadoResponseSchema):
    """ Retorna uma representação da result seguindo o schema definido em
        resultViewSchema.
    """
    return {
        "finalizado": result.finalizado,
        "jogo": result.jogo,
        "partida": {
            "id": result.partida.id,
            "nomeX": result.partida.nomeX,
            "pontosX": result.partida.pontosX,
            "nomeO": result.partida.nomeO,
            "pontosO": result.partida.pontosO,
            "velha": result.partida.velha,
            "data_criacao": result.partida.data_criacao,
            "ultima_alteracao": result.partida.ultima_alteracao
        },
        "vencedor": result.vencedor
    }