// Código JS para a Página Inicial
if(window.location.pathname == "/"){

    // Evento de mudança de valor no elemento select de estado de tarefa. Ao filtrar, é chamada a função que busca e exibe os dados 
    let filtro = document.querySelector("#filtro");
    if (filtro){
        filtro.addEventListener("change", async function(){
            preencheTabelaTarefas(filtro.value);
        });
    }

    // Ao carregar a página, é chamada a função que busca os dados e exibe na tabela
    preencheTabelaTarefas(filtro.value);

    // O estado padrão é -1, que retorna todas as tarefas. Estado 0 retorna não concluídas e Estado 1 retorna as concluídas.
    async function preencheTabelaTarefas(filtro=-1){
        
        let tabelaTarefas = document.querySelector("#tabelaTarefas");

        try {

            const response = await fetch("/busca?filtro="+filtro); // Faz a requisição
            const tarefas = await response.json(); // Converte a resposta para JSON

            html="<th>TÍTULO</th><th>DESCRIÇÃO</th><th>DATA</th><th>CONCLUÍDA?</th><th>AÇÕES</th>"

            tarefas.forEach(t => {

                html+="<tr><td>"+t.titulo+"</td><td>"+t.descricao+"</td><td>"+t.data;+"</td>";
                
                if(t.concluida){
                    html+="<td>Sim</td>";
                }else{
                    html+="<td>Não</td>";
                }
                
                html+="<td>";
                html += "<a href='/alterarTarefa?id="+t.id+"'><img src='static/icones/editar.png'></a>";
                html += "<a href='/excluirTarefa?id="+t.id+"'><img src='static/icones/cruz.png'></a>";
                html += "<a href='/concluirTarefa?filtro="+filtro+"&id="+t.id+"'><img src='static/icones/verificar.png'></a>";
                html += "</td></tr>";
            
            });

            tabelaTarefas.innerHTML=html;

        } catch (error) {
            console.error("Erro ao consultar a API:", error);
            tabelaTarefas.innerHTML = "Erro ao carregar os dados.";
        }
    }
}