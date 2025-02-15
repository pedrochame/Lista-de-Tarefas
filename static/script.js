//Código JS para as Páginas de Criação e Edição de Tarefa
if(["/criarTarefa","/alterarTarefa"].includes(window.location.pathname)){
    
    //Colocando máscara no campo DATA
    defineMascaraData();

    //Deixando a cor do texto no campo DATA em preto quando focado
    personalizaCampoData();

    //Ao enviar o formulario, é verificado se o campo DATA está preenchido corretamente
    let form = document.querySelector("#formulario");
    if(form){
        form.addEventListener("submit", function(event){

            //Se a data preenchida não é válida ou é posterior à data atual, o envio não acontece
            if(verificaData() == false){
                personalizaCampoDataErro(true);
                //Interrompendo comportamento padrão do evento
                event.preventDefault();
            }

        });
    }

}

function personalizaCampoData(){
    let data = document.querySelector("#data");
    if(data){
        data.addEventListener("focus",function(){
            personalizaCampoDataErro(false);
        });
    }
}

function personalizaCampoDataErro(erro=false){
    let data = document.querySelector("#data");
    if(data){
        if(erro){
            document.querySelector("#msgData").style.display = "block";
            data.style.color = "red";
        }else{
            document.querySelector("#msgData").style.display = "none";
            data.style.color = "black";
        }
    }
}

function verificaData(){
    let data = document.querySelector("#data");
    if(data){
        if(data.value.length!=10){
            return false;
        }

        if(data.value.split("/")[0]>31 || data.value.split("/")[1]>12){
            return false;
        }

        let dataTarefa = data.value.split("/")[2]+"-"+data.value.split("/")[1]+"-"+data.value.split("/")[0];
        let hoje = new Date();
        let dataAtual = hoje.getFullYear()+"-"+retornaMesStr(hoje.getMonth())+"-"+hoje.getDate();

        if(dataTarefa < dataAtual){
            return false;
        }

    }else{
        return false;
    }
    return true;
}

function retornaMesStr(mes){
    if(mes<10){
        return "0"+(mes+1);
    }
    return (mes+1);
}


/////////////// [REVISAR]

function defineMascaraData(){
    let data = document.querySelector("#data");
    if(data){
        data.addEventListener("input", function(e){

            //Se o caractere digitado no campo for o 11° ou não for um número, o mesmo é retirado

            // 0 -> 48 em ASCII | 9 -> 57 em ASCII
            let x = e.target.value.split("").pop();
            if((this.value.length == 11) || !(x.charCodeAt(0) >= 48 && x.charCodeAt(0) <= 57)){
                let v = this.value.split("");
                v.pop();
                this.value = v.join("");
            }

            //Se for o 3° dígito, coloca-se a barra de separação dia-mês
            //Se for o 5° dígito, coloca-se a barra de separação mês-ano
            if(this.value.length == 2 || this.value.length == 5){
                this.value += "/";
            }

        });
    }
}

///////////////

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

            html="<th>TÍTULO</th><th>DESCRIÇÃO</th><th>DATA</th><th>CONCLUÍDA?</th><th>AÇÕES</th>";

            tarefas.forEach(t => {


                //Se a tarefa já foi concluída, sua linha é verde. Se não, é vermelha.
                let corTarefa;
                if(t.concluida){
                    corTarefa = "style='background-color:rgba(0,255,0,0.15);'";
                }else{
                    corTarefa = "style='background-color:rgba(255,0,0,0.15);'";
                }




                html+="<tr><td "+corTarefa+">"+t.titulo+"</td><td "+corTarefa+">"+t.descricao+"</td><td "+corTarefa+">"+t.data;+"</td>";
                
                if(t.concluida){
                    html+="<td "+corTarefa+">Sim</td>";
                }else{
                    html+="<td "+corTarefa+">Não</td>";
                }


                html+="<td "+corTarefa+"><div class='col-12 d-flex'>";

                //Os ícones de ação de EDITAR e CONCLUIR só são exibidos se a tarefa ainda não tiver sido concluída
                let mostraIcones;
                if(t.concluida){
                    mostraIcones = "style='display:none;'";
                }else{
                    mostraIcones = "style='display:inline;'";
                }


                html += "<div class='col-4'><a "+mostraIcones+" href='/concluirTarefa?filtro="+filtro+"&id="+t.id+"'><img class='icone img-fluid' src='static/icones/concluir.png'></a></div>";


                html += "<div class='col-4'><a href='/excluirTarefa?filtro="+filtro+"&id="+t.id+"'><img class='icone img-fluid' src='static/icones/apagar.png'></a></div>";


                html += "<div class='col-4'><a "+mostraIcones+"href='/alterarTarefa?id="+t.id+"'><img class='icone img-fluid' src='static/icones/editar.png'></a></div>";
                
                html += "</div></td></tr>";
            
            });

            tabelaTarefas.innerHTML=html;

            //Personalizando os ícones de ação cada vez que a exibição dos registros é atualizada
            personalizaIcones();

        } catch (error) {
            console.error("Erro ao consultar a API:", error);
            tabelaTarefas.innerHTML = "Erro ao carregar os dados.";
        }
    }

    function personalizaIcones(){

        //Ao passar o mouse sobre os ícones, os mesmos são alterados para a versão colorida
        let icones = document.querySelectorAll(".icone");
        if (icones) {
            icones.forEach(icone => {
                let nome = icone.src.split("/")[icone.src.split("/").length-1];
                icone.addEventListener("mouseover", function () {
                    icone.src = "static/icones/cor-"+nome;
                });
                icone.addEventListener("mouseout", function () {
                    icone.src = "static/icones/"+nome.replace("cor-","");
                });
            });
        }
    }

}