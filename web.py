import requests
import json

# Consumindo WebAPI

while True:
    cep = input('Digite o CEP para ter informações sobre o local: ')
    
    #URL
    url_cep = "http://viacep.com.br/ws/{}/json/".format(cep)

    #Buscando o URL do WebAPI
    req = requests.get(url_cep)

    #Tentativa de acesso
    try:

        #Leitura da WebAPI
        adress_data = req.json()
        break

    except json.decoder.JSONDecodeError:
        print("CEP inválido, digite novamente.")
        continue

#Exibição dos dados
print('CEP: {}'.format(adress_data['cep']))
print('CIDADE: {}'.format(adress_data['localidade']))
print('BAIRRO: {}'.format(adress_data['bairro']))
print('ESTADO: {}'.format(adress_data['uf']))