import pytest
from app import create_app
from datetime import datetime
from routes.tarefa_routes import get_tarefas,get_tarefa,create_tarefa,update_tarefa,delete_tarefa,concluir_tarefa

# Fixture do pytest para criar o client
@pytest.fixture
def client():
    app = create_app()  # Cria a aplicação Flask
    with app.test_client() as client:  # Cria o client de teste
        yield client  # Retorna o client para ser usado no teste

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

def test_get_tarefa(client):

    # Primeiro, devemos criar uma tarefa para fazer o teste de buscá-la
    tarefa_teste = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"2025-02-21"}
    response = client.post('/tarefas',json=tarefa_teste)

    # Verificando se a tarefa foi criada corretamente, ou seja, se o status da resposta é 201
    assert response.status_code == 201

    # Guardando o id da tarefa teste criada
    tarefa_teste_id = response.get_json().get("id")

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

    # Formatando data da tarefa para ficar no mesmo formato que a data do dicionário da tarefa teste
    tarefa.update({
        "data":   
        (tarefa.get("data").split("/")[2]+"-"+tarefa.get("data").split("/")[1]+"-"+tarefa.get("data").split("/")[0])
    })

    # Verifica se o dicionário possui os valores corretos
    assert set(tarefa.values()) == set(tarefa_teste.values())

    # Deletendo tarefa teste do banco de dados
    response = client.delete(f"/tarefas/{tarefa_teste_id}")
    
    # Verifica se a deleção funcionou
    assert response.status_code == 200

    # Verificando se a tarefa realmente não está no banco de dados
    response = client.get(f"tarefas/{tarefa_teste_id}")

    assert response.status_code == 404


def test_create_tarefa(client):

    # Primeiro, devemos criar uma tarefa para fazer o teste de buscá-la
    tarefa_teste = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"2025-02-21"}
    response = client.post('/tarefas',json=tarefa_teste)

    # Verificando se a tarefa foi criada corretamente, ou seja, se o status da resposta é 201
    assert response.status_code == 201

    # Guardando o id da tarefa teste criada
    tarefa_teste_id = response.get_json().get("id")

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

    # Formatando data da tarefa para ficar no mesmo formato que a data do dicionário da tarefa teste
    tarefa.update({
        "data":   
        (tarefa.get("data").split("/")[2]+"-"+tarefa.get("data").split("/")[1]+"-"+tarefa.get("data").split("/")[0])
    })

    # Verifica se o dicionário possui os valores corretos
    assert set(tarefa.values()) == set(tarefa_teste.values())

    # Deletendo tarefa teste do banco de dados
    response = client.delete(f"/tarefas/{tarefa_teste_id}")
    
    # Verifica se a deleção funcionou
    assert response.status_code == 200

    # Verificando se a tarefa realmente não está no banco de dados
    response = client.get(f"tarefas/{tarefa_teste_id}")

    assert response.status_code == 404

def test_update_tarefa(client):

    # Crindo tarefa
    tarefa_teste = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"2025-02-21"}
    response = client.post('/tarefas',json=tarefa_teste)

    # Verificando se a tarefa foi criada corretamente, ou seja, se o status da resposta é 201
    assert response.status_code == 201

    # Guardando o id da tarefa teste criada
    tarefa_teste_id = response.get_json().get("id")

    # Criando tarefa com os dados a serem trocados na tarefa teste
    tarefa_teste_edicao = {"titulo":"tarefa teste edicao","descricao":"desc. da tarefa teste edicao","data":"2025-02-21"}

    # Fazendo requisição PUT em tarefas/<int:id>
    response = client.put(f"tarefas/{tarefa_teste_id}", json=tarefa_teste_edicao)

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
    tarefa.update({
        "data":   
        (tarefa.get("data").split("/")[2]+"-"+tarefa.get("data").split("/")[1]+"-"+tarefa.get("data").split("/")[0])
    })

    # Verifica se o dicionário possui os valores corretos
    assert set(tarefa.values()) == set(tarefa_teste_edicao.values())

    # Deletendo tarefa teste do banco de dados
    response = client.delete(f"/tarefas/{tarefa_teste_id}")
    
    # Verifica se a deleção funcionou
    assert response.status_code == 200

    # Verificando se a tarefa realmente não está no banco de dados
    response = client.get(f"tarefas/{tarefa_teste_id}")

    assert response.status_code == 404


def test_delete_tarefa(client):

    # Crindo tarefa
    tarefa_teste = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"2025-02-21"}
    response = client.post('/tarefas',json=tarefa_teste)

    # Verificando se a tarefa foi criada corretamente, ou seja, se o status da resposta é 201
    assert response.status_code == 201

    # Guardando o id da tarefa teste criada
    tarefa_teste_id = response.get_json().get("id")

    # Deletendo tarefa do banco de dados
    response = client.delete(f"/tarefas/{tarefa_teste_id}")
    
    # Verifica se a deleção funcionou
    assert response.status_code == 200

    # Verificando se a tarefa realmente não está no banco de dados
    response = client.get(f"tarefas/{tarefa_teste_id}")

    assert response.status_code == 404

def test_concluir_tarefa(client):

    # Crindo tarefa
    tarefa_teste = {"titulo":"tarefa teste","descricao":"desc. da tarefa teste","data":"2025-02-21"}
    response = client.post('/tarefas',json=tarefa_teste)

    # Verificando se a tarefa foi criada corretamente, ou seja, se o status da resposta é 201
    assert response.status_code == 201

    # Guardando o id da tarefa teste criada
    tarefa_teste_id = response.get_json().get("id")

    # Guardando o estado da tarefa teste criada
    tarefa_teste_concluida = response.get_json().get("concluida")

    # Testando requisição PATCH em tarefas/<int:id>/concluir
    response = client.patch(f"tarefas/{tarefa_teste_id}/concluir")

    # Verifica se a requisição funcionou
    assert response.status_code == 200

    # Verifica se o estado da resposta é diferente do estado antes da requisição
    assert response.is_json
    assert response.get_json().get("concluida") != tarefa_teste_concluida   

    # Deletendo tarefa do banco de dados
    response = client.delete(f"/tarefas/{tarefa_teste_id}")
    
    # Verifica se a deleção funcionou
    assert response.status_code == 200

    # Verificando se a tarefa realmente não está no banco de dados
    response = client.get(f"tarefas/{tarefa_teste_id}")
    assert response.status_code == 404