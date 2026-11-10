import requests
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()


def consultar_cotacao(moeda:str = "USD-BRL") -> str:
    """Consulta a cotação atual de uma moeda em relação ao Real (BRL).
    
    Args:
        moeda: O par de moedas a ser consultado, 
        por exemplo 'USD-BRL', 'EUR-BRL' ou 'BTC-BRL'.
    """
    print(f"\n⚙️ [AGENTE EM AÇÃO] A IA decidiu executar consultar_cotacao('{moeda}')...")

    try:
        url = os.getenv('API_BASE_URL')
        resposta = requests.get(f"{url}/{moeda}",timeout=5)
        dados = resposta.json()
        chave = moeda.replace('-',"")
        info = dados[chave]
        valor = info['bid']
        return (f"A cotação atual de {moeda} é R${float(valor):.2f}")
    except (KeyError,requests.RequestException) as error:
        print(f"Erro ao consultar cotação: {error}")
        return None
    
def consultar_endereco(cep:str) -> str:
    """Consulta o endereço completo brasileiro 
    (rua, bairro e cidade) a partir de um CEP.
    
    Args:
        cep: O código postal brasileiro 
        com 8 dígitos (ex: '01001000' ou '01001-000').
    """
    print(f"\n⚙️ [AGENTE EM AÇÃO] Consultando CEP {cep}...")

    try:
        url = os.getenv("URL_CEP")
        resposta = requests.get(f"{url}{cep}/json/",timeout=5)
        dados = resposta.json()
        rua=dados['logradouro']
        bairro=dados['bairro']
        cidade=dados['localidade']
        return (f'Endereço encontrado: {rua}, {bairro} e {cidade}')
    except (KeyError,requests.RequestException) as error:
        print(f"Falha ao consultar endereço: {error}")
        return None

def main():
    
    client = genai.Client()

    config = types.GenerateContentConfig(tools=[consultar_cotacao,consultar_endereco],temperature=0.0)

    chat = client.chats.create( model="gemini-3.5-flash",
        config=config
        )
    

    while True:

        pergunta = input("Digite sua dúvida: ").lower().strip()

        if pergunta in ["sair","exit"]:
            print("Saindo do programa!")
            break

        resposta = chat.send_message(pergunta)
        print(f'Resposta:{resposta.text}')
        
if __name__ == "__main__":
    main()