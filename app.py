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
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")


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
        # adicionando produto
        session.add(disputa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado a disputa entre os jogadores: '{disputa.nomeX}' e '{disputa.nomeO}'")
        return apresenta_disputa(disputa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{disputa.nomeX}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar a disputa :/"
        logger.warning(f"Erro ao criar uma nova disputa entre os jogadores: '{disputa.nomeX}' e '{disputa.nomeO}', {error_msg}")
        return {"message": error_msg}, 400

