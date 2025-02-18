# Função para alterar data de aaaa-mm-dd para dd/mm/aaaa e vice-versa
def converteData(dt):
    
    if dt[2] == "-":
        return dt.split("-")[2]+"-"+dt.split("-")[1]+"-"+dt.split("-")[0]
    else:
        return dt.split("/")[2]+"/"+dt.split("/")[1]+"/"+dt.split("/")[0]
    
