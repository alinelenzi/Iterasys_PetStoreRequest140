# 1.bibliotecas
import json      # leitor e escritor de arquivos json
import pytest    # enginer/ framework de teste de unidade
import requests  # framework de teste API
from utils.utils import read_csv

# 2.classe (opcional no python, em muitos casos)
# 2.1.atributos ou variáveis
# consulta e resultado esperado
pet_id = 173092001
pet_name = "Princess"
pet_category_id = 1
pet_category_name = "dog"
pet_tag_id = 1
pet_tag_name = "vacinado"

# informações em comum

url= 'https://petstore.swagger.io/v2/pet'   #endereço
headers= {'Content-Type': 'application/json'} #formato dos dados trafegados

# 2.2.funções e métodos

def test_post_pet():
    #configura
    #dados de entrada estão no arquivo json
    pet = open("./fixtures/json/pet1.json")    # abre o conteudo json
    data = json.loads(pet.read())              # ler o conteúdo e carrega com json em uma variável data
    #dados de saída/ resultado esperado estão nos atibutos acima das funções
    
    #executa
    response = requests.post(     #executa o método post com as informações a seguir
        url = url,                #endereço
        headers = headers,        #cabeçalho, formato da mensagem
        data = json.dumps(data),  #a mensagem = json
        timeout = 5               #tempo limite da transmissão, em segundos
    )

    #valida
    response_body = response.json()  #cria uma variável e carrega a resposta em formato json

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name

def test_get_pet():
    #configura
    #executa
    response = requests.get(
        url= f'{url}/{pet_id}',
        headers=headers
    )

    #valida
    response_body = response.json()
    
    assert response.status_code == 200
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['status'] == 'available'


def test_put_pet():
    #dados de entrada estão no arquivo json
    pet = open("./fixtures/json/pet2.json")    # abre o conteudo json
    data = json.loads(pet.read())              # ler o conteúdo e carrega com json em uma variável data

    #executa
    response = requests.put(
        url= url,
        headers=headers,
        data= json.dumps(data),
        timeout=5
    )

    #valida
    response_body = response.json()
    
    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['tags'][0]['name'] == pet_tag_name
    assert response_body['status'] == 'sold'

def test_delete_pet():
    #Arrange - Organiza dados
    
    #Act - afirma
    response = requests.delete(
        url= f'{url}/{pet_id}',
        headers=headers,
        timeout=5
    )

    #Assert - Executa
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)

@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                        read_csv('./fixtures/csv/pets.csv')
                        )

def test_post_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):
    #arrange
    #criando a estrutura de json, criando vários
    pet={}
    pet['id'] = int(pet_id)
    pet['category'] = {}
    pet['category']['id'] = int(category_id)
    pet['category']['name'] = category_name
    pet['name'] = pet_name
    pet['photoUrls'] = []
    pet['photoUrls'].append('')
    pet['tags'] = []
    
    tags_splited = tags.split(';')
    for tag in tags_splited:
        tag = tag.split('-')
        tag_formatada = {}
        tag_formatada['id'] = int(tag[0])
        tag_formatada['name'] = tag[1]
        pet['tags'].append(tag_formatada)

    pet['status'] = status

    #act
    pet = json.dumps(obj=pet, indent=4)
    print('\n' + pet)

    #assert
    response = requests.post(
        url=url,
        headers=headers,
        data=pet,
        timeout=5
    )

    #Compara
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == int(pet_id)
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == int(category_id)
    assert response_body['category']['name'] == category_name
    assert response_body['status'] == status
    for x in range(len(tags_splited)):
        tag = tags_splited[x]
        tag = tag.split("-")
        assert response_body['tags'][x]['id'] == int(tag[0])
        assert response_body['tags'][x]['name'] == tag[1]


