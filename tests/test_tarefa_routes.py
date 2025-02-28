import pytest
from app import create_app
from datetime import datetime

# Fixture do pytest para criar o client
@pytest.fixture
def client():
    app = create_app()  # Cria a aplicação Flask
    with app.test_client() as client:  # Cria o client de teste
        yield client  # Retorna o client para ser usado no teste

# Fixture que cria uma tarefa para testes e depois exclui
# Obs.: Como essa fixture cria, deleta e verifica se a a tarefa não está mais no banco de dados, para evitar redundância, as funções de teste para criação e deleção serão apenas para testes de erros.
@pytest.fixture
def tarefaTeste(client):

    tarefa = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"2025-02-21"}
    response = client.post('/tarefas',json=tarefa)

    # Verificando se a tarefa foi criada corretamente, ou seja, se o status da resposta é 201
    assert response.status_code == 201
    
    response = response.get_json()

    # Retornando o json da tarefa teste
    yield response

    # Deletendo tarefa teste do banco de dados
    response = client.delete(f"/tarefas/{response.get('id')}")

    # Verifica se a deleção funcionou
    assert response.status_code == 200

    response = response.get_json()

    # Verificando se a tarefa realmente não está no banco de dados
    response = client.get(f"/tarefas/{response.get("id")}")
    assert response.status_code == 404


def test_get_tarefas(client):
    # Faz uma requisição GET para a rota "/tarefas"
    response = client.get('/tarefas')
    
    # Verifica se a resposta tem o status 200 (sucesso)
    assert response.status_code == 200

    # Verifica se a resposta é um json
    assert response.is_json

    # Pegando a lista de dicionários retornada pela resposta
    tarefas = response.get_json()

    # Verifica se cada dicionário possui as chaves corretas
    for tarefa in tarefas:
        assert set(tarefa.keys()) == {"id","concluida","titulo", "descricao", "data"}

def test_get_tarefa(client,tarefaTeste):

    # Guardando a tarefa teste criada
    tarefa_teste = tarefaTeste

    # Guardando id da tarefa teste
    tarefa_teste_id = tarefa_teste.get("id")

    # Faz uma requisição GET para a rota "/tarefas/<int:id>"
    response = client.get(f'/tarefas/{tarefa_teste_id}')
    
    # Verifica se a resposta tem o status 200 (sucesso)
    assert response.status_code == 200

    # Verifica se a resposta é um json
    assert response.is_json

    # Pegando o dicionário retornado pela resposta
    tarefa = response.get_json()

    # Verifica se o dicionário possui as chaves corretas
    assert set(tarefa.keys()) == {"id","concluida","titulo", "descricao", "data"}

    # Acrescentando CONCLUIDA e ID ao dicionário da tarefa teste, para comparar com o json completo que vem como resposta da requisição GET
    tarefa_teste.update({"concluida":False , "id":int(tarefa_teste_id)})

    # Verifica se o dicionário possui os valores corretos
    assert set(tarefa.values()) == set(tarefa_teste.values())


def test_create_tarefa(client):

    # Criando tarefa com campos faltando
    tarefa = {"titulo":"tarefa teste", "data":"2025-02-21"}
    response = client.post('/tarefas',json=tarefa)
    assert response.status_code == 400

    # Criando tarefa com data em formato inesperado
    tarefa = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"21/02/2025"}
    response = client.post('/tarefas',json=tarefa)
    assert response.status_code == 400

    # Criando tarefa com campo vazio
    tarefa = {"titulo":"tarefa teste","descricao":"","data":"21/02/2025"}
    response = client.post('/tarefas',json=tarefa)
    assert response.status_code == 400

    # Criando tarefa com campos a mais
    tarefa = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"21/02/2025", "obs":"observacao sobre tarefa"}
    response = client.post('/tarefas',json=tarefa)
    assert response.status_code == 400

def test_update_tarefa(client,tarefaTeste):

    # Guardando a tarefa teste criada
    tarefa_teste = tarefaTeste

    # Guardando id da tarefa teste
    tarefa_teste_id = tarefa_teste.get("id")

    # Criando tarefa com os dados a serem trocados na tarefa teste
    tarefa_teste_edicao = {"titulo":"tarefa teste edicao","descricao":"desc. da tarefa teste edicao","data":"2025-02-21"}

    # Fazendo requisição PUT em tarefas/<int:id>
    response = client.put(f"/tarefas/{tarefa_teste_id}", json=tarefa_teste_edicao)

    # Testando se a requisição funcionou
    assert response.status_code == 200

    # Verifica se a resposta é um json
    assert response.is_json

    # Pegando o dicionário retornado pela resposta
    tarefa = response.get_json()

    # Verifica se o dicionário possui as chaves corretas
    assert set(tarefa.keys()) == {"id","concluida","titulo", "descricao", "data"}

    # Acrescentando CONCLUIDA e ID ao dicionário da tarefa teste, para comparar com o json completo que vem como resposta da requisição GET
    tarefa_teste_edicao.update({"concluida":False , "id":int(tarefa_teste_id)})

    # Formatando data da tarefa para ficar no mesmo formato que a data do dicionário da tarefa teste
    tarefa.update({"data": datetime.strptime(tarefa.get("data"),"%d/%m/%Y").strftime("%Y-%m-%d")})

    # Verifica se o dicionário possui os valores corretos
    assert set(tarefa.values()) == set(tarefa_teste_edicao.values())


def test_delete_tarefa(client):

    # Deletando uma tarefa inexistente
    response = client.get(f'/tarefas')
    tarefas = response.get_json()

    maior_id = 0
    for tarefa in tarefas:
        if tarefa["id"] > maior_id:
            maior_id = tarefa["id"]

    tarefa_id = maior_id + 1

    # Deletendo tarefa do banco de dados
    response = client.delete(f"/tarefas/{tarefa_id}")
    
    # Verifica que a deleção não funcionou
    assert response.status_code == 404

def test_concluir_tarefa(client, tarefaTeste):

    # Guardando a tarefa teste criada
    tarefa_teste = tarefaTeste

    # Guardando id da tarefa teste
    tarefa_teste_id = tarefa_teste.get("id")

    # Guardando o estado da tarefa teste criada
    tarefa_teste_concluida = client.get(f'/tarefas/{tarefa_teste_id}').get_json().get("concluida")

    # Testando requisição PATCH em tarefas/<int:id>/concluir
    response = client.patch(f"/tarefas/{tarefa_teste_id}/concluir")

    # Verifica se a requisição funcionou
    assert response.status_code == 200

    # Verifica se o estado da resposta é diferente do estado antes da requisição
    assert response.is_json
    assert response.get_json().get("concluida") != tarefa_teste_concluida   