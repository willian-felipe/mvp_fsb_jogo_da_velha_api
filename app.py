from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Disputa
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="MVP FSB - Jogo da Velha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
disputa_tag = Tag(name="Disputa", description="Inicia (Adição), visualização e remoção de disputas à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi/swagger')


@app.post('/disputa', tags=[disputa_tag],
          responses={"200": DisputaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_disputa(form: DisputaInitSchema):
    """Cria uma nova disputa na base de dados

    Retorna uma representação da partida iniciada.
    """
    disputa = Disputa(nomeX=form.nomeX, nomeO=form.nomeO)
    logger.debug(f"Adicionando uma disputa entre os jogadores: '{disputa.nomeX}' e '{disputa.nomeO}'")

    try:
        # criando conexão com a base
        session = Session()
        # adicionando disputa
        session.add(disputa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado a disputa entre os jogadores: '{disputa.nomeX}' e '{disputa.nomeO}'")
        return apresenta_disputa(disputa), 200

    except IntegrityError as e:
        # TODO - MELHORAR INTEGRIDADE NESTE PONTO
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "disputa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar disputa '{disputa.nomeX}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar a disputa :/"
        logger.warning(f"Erro ao criar uma nova disputa entre os jogadores: '{disputa.nomeX}' e '{disputa.nomeO}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/disputas', tags=[disputa_tag],
         responses={"200": ListagemDisputasSchema, "404": ErrorSchema})
def get_disputas():
    """Faz a busca por todas as Disputas realizadas no jogo

    Retorna uma representação da listagem de disputas.
    """
    logger.debug(f"Coletando histórico de Disputas")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    disputas = session.query(Disputa).all()

    if not disputas:
        # se não há disputas cadastradas
        return {"disputas": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(disputas))
        # retorna a representação de disputa
        print(disputas)
        return apresenta_disputas(disputas), 200

@app.delete('/disputa', tags=[disputa_tag],
            responses={"200": DisputaDelSchema, "404": ErrorSchema})
def del_disputa(query: DisputaBuscaSchema):
    """Deleta uma Disputa a partir do id da disputa informada

    Retorna uma mensagem de confirmação da remoção.
    """
    disputa_id = int(unquote(unquote(str(query.id))))
    print(disputa_id)
    logger.debug(f"Deletando disputa do id: #{disputa_id}")

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Disputa).filter(Disputa.id == disputa_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada a disputa #{disputa_id}")
        return {"message": "Disputa removida", "id": disputa_id}
    else:
        # se o disputa não foi encontrado
        error_msg = "Disputa não encontrada na base :/"
        logger.warning(f"Erro ao deletar a disputa #'{disputa_id}', {error_msg}")
        return {"message": error_msg}, 404


@app.put('/disputa/checaresultado', tags=[disputa_tag],
          responses={"200": ChecaResultadoResponseSchema, "409": ErrorSchema, "400": ErrorSchema})
def checaresultado(form: ChecaResultadoRequestSchema):
    """Cria uma nova disputa na base de dados

    Retorna uma representação da partida iniciada.
    """

    # TODO Faz a verificação do vencedor

    try:
        response = ChecaResultadoResponseSchema(
            jogo=form.jogo,
            partida=None,
            vencedor=None,
            finalizado=False
        )

        disputa_id = form.disputa_id

        print(disputa_id)

        if len(form.jogo) != 9:
            error_msg = "Jogo informado não corresponde a um jogo da velha válido :/"
            logger.warning(f"Falha no processamento da disputa '{disputa_id}', {error_msg}")
            return {"message": error_msg}, 400

        # criando conexão com a base
        session = Session()

        # Pega a disputa atual
        disputaAtual = session.query(Disputa).filter(Disputa.id == disputa_id).first()

        # Verifica se o jogador X venceu
        if(form.jogo[0] == 'X' and form.jogo[1] == 'X' and form.jogo[2] == 'X' or 
           form.jogo[3] == 'X' and form.jogo[4] == 'X' and form.jogo[5] == 'X' or
           form.jogo[6] == 'X' and form.jogo[7] == 'X' and form.jogo[8] == 'X' or
           form.jogo[0] == 'X' and form.jogo[3] == 'X' and form.jogo[6] == 'X' or 
           form.jogo[1] == 'X' and form.jogo[4] == 'X' and form.jogo[7] == 'X' or 
           form.jogo[2] == 'X' and form.jogo[5] == 'X' and form.jogo[8] == 'X' or
           form.jogo[0] == 'X' and form.jogo[4] == 'X' and form.jogo[8] == 'X' or
           form.jogo[2] == 'X' and form.jogo[4] == 'X' and form.jogo[6] == 'X'):
            response.vencedor = 'X'
            response.finalizado = True
            
            # atualizando disputa
            session.query(Disputa).filter(Disputa.id == disputa_id).update({'pontosX': disputaAtual.pontosX + 1})

        if(form.jogo[0] == 'O' and form.jogo[1] == 'O' and form.jogo[2] == 'O' or 
           form.jogo[3] == 'O' and form.jogo[4] == 'O' and form.jogo[5] == 'O' or
           form.jogo[6] == 'O' and form.jogo[7] == 'O' and form.jogo[8] == 'O' or
           form.jogo[0] == 'O' and form.jogo[3] == 'O' and form.jogo[6] == 'O' or 
           form.jogo[1] == 'O' and form.jogo[4] == 'O' and form.jogo[7] == 'O' or 
           form.jogo[2] == 'O' and form.jogo[5] == 'O' and form.jogo[8] == 'O' or
           form.jogo[0] == 'O' and form.jogo[4] == 'O' and form.jogo[8] == 'O' or
           form.jogo[2] == 'O' and form.jogo[4] == 'O' and form.jogo[6] == 'O'):
            response.vencedor = 'O'
            response.finalizado = True

            # atualizando disputa
            session.query(Disputa).filter(Disputa.id == disputa_id).update({'pontosO': disputaAtual.pontosO + 1})
        
        if not response.finalizado:
            isVelha: bool = True

            for x in form.jogo:
                print(x)
                if x == '':
                    response.vencedor = None
                    response.finalizado = False
                    isVelha = False
                    break
            
            if isVelha:
                response.vencedor = "VELHA"
                response.finalizado = True

                # atualizando disputa
                session.query(Disputa).filter(Disputa.id == disputa_id).update({'velha': disputaAtual.velha + 1})


        # efetivando o camando de atualização do item na tabela
        session.commit()

        disputa = session.query(Disputa).filter(Disputa.id == disputa_id).first()

        if not disputa:
            # Se a disputa não foi encontrado
            error_msg = "Disputa não encontrado na base :/"
            logger.warning(f"Erro ao buscar disputa '{disputa_id}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            response.partida = disputa
            return apresenta_resultado(response), 200
    except IntegrityError as e:
        # TODO - MELHORAR INTEGRIDADE NESTE PONTO
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "disputa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar disputa '{disputa.nomeX}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar a disputa :/"
        # logger.warning(f"Erro ao criar uma nova disputa entre os jogadores: '{disputa.nomeX}' e '{disputa.nomeO}', {error_msg}")
        logger.warning(f"Erro: '{str(e)}', {error_msg}")
        return {"message": error_msg}, 400