import os

def search_default(nome_executavel, caminhos_padroes):
    for caminho in caminhos_padroes:
        caminho_completo = os.path.join(caminho, nome_executavel)
        if os.path.isfile(caminho_completo):
            return caminho_completo
    return None

def general_search(nome_executavel, caminhos_iniciais):
    for caminho_inicial in caminhos_iniciais:
        for raiz, diretorios, arquivos in os.walk(caminho_inicial):
            if nome_executavel in arquivos:
                return os.path.join(raiz, nome_executavel)
    return None

def find_exe(nome_executavel, caminhos_padroes, caminhos_iniciais_generalizados):
    # Primeiro, tenta encontrar nos locais padrões
    caminho_encontrado = search_default(nome_executavel, caminhos_padroes)

    # Se não encontrar, faz uma busca generalizada
    if caminho_encontrado is None:
        for caminho_inicial in caminhos_iniciais_generalizados:
            caminho_encontrado = general_search(nome_executavel, caminho_inicial)
            if caminho_encontrado:
                break

    return caminho_encontrado
