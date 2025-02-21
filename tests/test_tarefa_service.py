from services.tarefa_service import validaDadosRecebidos

def teste_dados_validos():
    dados = {"titulo"   : "Fazer compras" , 
             "descricao": "Ir ao mercado e comprar todos os itens da lista" ,
             "data"     : "2025-02-25",
            }
    
    assert(validaDadosRecebidos(dados)) == True

def teste_dados_vazios():
    dados = {"titulo"   : "Fazer compras" , 
             "descricao": "" ,
             "data"     : "2025-02-25",
            }
    
    assert(validaDadosRecebidos(dados)) == False

def teste_dados_faltando():
    dados = {"titulo"   : "Fazer compras" , 
             "data"     : "2025-02-25",
            }
    
    assert(validaDadosRecebidos(dados)) == False

def teste_dados_extras():

    dados = {"titulo"   : "Fazer compras" , 
             "descricao": "Ir ao mercado e comprar todos os itens da lista" ,
             "data"     : "2025-02-25",
             "hora"     : "10:00"
            }
    
    assert(validaDadosRecebidos(dados)) == False