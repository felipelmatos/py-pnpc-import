import base64
import requests
import json

"""------------------------------"""
"""       EDITAR CONSTANTES      """
"""------------------------------"""

LOGIN = "login_recebido_pela_pnpc"
SENHA = "senha_recebida_pela_pnpc"
ARQUIVO_JSON = "Json_caminho_unidades_a_importar"
CNPJ = "cnpj_da_unidade_raiz_a_receber_dados"

"""------------------------------"""
"""     METODOS DA APLICACAO     """
"""------------------------------"""

def getToken():
    my_headers = {
        'Content-Type': 'application/json'
    }
    dados = {"login":LOGIN,"senha":SENHA}
    resposta = requests.post('https://treina.pncp.gov.br/api/pncp/v1/usuarios/login', headers=my_headers, json=dados)
    return resposta.headers['authorization']

def setDados(codigoIbge, codigoUnidade, nomeUnidade):
    token = getToken().strip()
    url = "https://treina.pncp.gov.br/api/pncp/v1/orgaos/"+CNPJ+"/unidades"
    my_headers = {
        "Authorization": token
    }
    unidades = {"codigoIBGE": codigoIbge,"codigoUnidade":codigoUnidade,"nomeUnidade":nomeUnidade}
    resposta = requests.post(url, headers=my_headers, json=unidades)
    return resposta.status_code

def abreArquivoJson(caminho):
    arquivo = open(caminho)
    dados = json.load(arquivo)
    arquivo.close()
    return dados['items']

"""------------------------------"""
"""REGRA DE NEGOCIO DA IMPORTACAO"""
"""------------------------------"""

dadosJson = abreArquivoJson(ARQUIVO_JSON);
for i in dadosJson:
    print("INSERINDO -> "+i['codigoibge']+"|"+i['codigounidade']+"|"+i['nomeunidade'])
    retorno = setDados(i['codigoibge'],i['codigounidade'],i['nomeunidade'])
    if retorno == 200 or retorno == 201:
        print("INSERIDO!!!")
        print("")
    else:
        print("ERRO AO INSERIR! VERIFICAR SE JÁ EXISTE NO PORTAL.")
        print("")

print("------------------")        
print("Fim da importação.")
