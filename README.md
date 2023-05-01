# mvp_fsb_jogo_da_velha_api
MVP do curso de Desenvolvimento Full Stack (Sprint 1) - Jogo da Velha (API)

## Processo de Instalação
Para realizar o processo de instalação, basta seguir os passos-a-passos abaixo:
    1. Validar se o pip está atualizado
        >>> python3 -m pip install --upgrade pip
    
    2. Instalar o virtualenv
        >>> python3 -m pip install --user virtualenv
    
    3. No diretório raiz do projeto, rodar o comando para criar o ambiente virtual
        >>> python3 -m venv env
    
    4. Ativar o ambiente virtual
        >>> .\env\Scripts\activate
    
    5. Instalar as bibliotecas do projeto dentro do ambiente virtual (Certificar-se que o ambiente virtual tenha sido iniciado >> (env) no início da linha)
        >>> python3 -m pip install -r requirements.txt
    
    6. Rodar a aplicação via flask (Certificar-se que o ambiente virtual tenha sido iniciado >> (env) no início da linha)
        a. Modo normal
            >>> flask run --host 0.0.0.0 --port 5500
        b. Modo desenvolvimento
            >>> flask run --host 0.0.0.0 --port 5500 --reload
    
    7. Abra o endereço [http://localhost:5000/] no navegador para validar a sua execução.
        

Para finalizar/desativar o ambiente virtual, basta executar o seguinte comando:
    >>> deactivate