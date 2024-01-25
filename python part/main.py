import subprocess
import os
import ctypes
import sys
import json
import os

# ========= #
#  Módulos  #
# ========= #

import regedit
import laucherFind
import paths

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_appdata_path(filename):
    # Obtém o caminho da pasta AppData
    appdata_dir = os.environ['APPDATA']

    # Cria o caminho para a pasta específica 'Game Lister'
    game_lister_dir = os.path.join(appdata_dir, 'Game Lister')

    # Cria a pasta 'Game Lister' se ela não existir
    if not os.path.exists(game_lister_dir):
        os.makedirs(game_lister_dir)

    # Constrói o caminho completo do arquivo
    file_path = os.path.join(game_lister_dir, filename)
    return file_path

def load_saved_paths():
    file_path = get_appdata_path('launcher_paths.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_paths(launcher_data):
    file_path = get_appdata_path('launcher_paths.json')
    with open(file_path, 'w') as file:
        # Usando indent=4 para uma formatação mais legível
        json.dump(launcher_data, file, indent=4)

        
def locate_launcher(exe_name, default_paths, general_paths):
    try:
        path = laucherFind.find_exe(exe_name, default_paths, general_paths)

        if not path:
            raise ValueError(f"Launcher '{exe_name}' não encontrado nos caminhos especificados.")

        try:
            subprocess.Popen([path])
        except Exception as exec_error:
            raise ValueError(f"Erro ao tentar executar o launcher: {exec_error}")

    except ValueError as error:
        print(f"Erro: {error}")
        return  # Adiciona um retorno aqui para sair da função se houver um erro

    # Carrega os caminhos salvos e atualiza com o novo caminho encontrado
    saved_paths = load_saved_paths()
    saved_paths[exe_name] = path
    save_paths(saved_paths)  # Atualizado para chamar sem o argumento de caminho de arquivo
 
    
def open_exe(path): 
        if path:
            try:
                subprocess.Popen([path])
                print(f"Executável '{path}' aberto com sucesso.")
            except Exception as e:
                print(f"Erro ao abrir o executável: {e}")
        else:
            print("Caminho do executável não fornecido.")

def open_launcher(launcher_name):
    save_file = 'launcher_paths.json'  # Defina o caminho do arquivo de dados salvos
    saved_paths = load_saved_paths()

    # Tenta usar o caminho salvo
    if launcher_name in saved_paths:
        open_exe(saved_paths[launcher_name])
        return

    # Se o caminho não estiver salvo, use o processo padrão
    name_attr = f'name_{launcher_name}'
    default_paths_attr = f'default_paths_{launcher_name}'

    launcher_name_value = getattr(paths, name_attr, None)
    default_paths_value = getattr(paths, default_paths_attr, None)

    if launcher_name_value is not None and default_paths_value is not None:
        launcher_path = locate_launcher(launcher_name_value, default_paths_value, paths.general_paths)

        # Salva o caminho encontrado para uso futuro
        if launcher_path:
            saved_paths[launcher_name] = launcher_path
            save_paths(save_file, saved_paths)

            open_exe(launcher_path)
        else:
            print(f"Caminho para o launcher '{launcher_name}' não encontrado.")
    else:
        print(f"Launcher '{launcher_name}' não encontrado.")

def main():
    
    # ==================== # 
    #  Insert de Registro  #
    # ==================== #
    
    protocol_name = 'gamelister'
    executable_path = 'C:\\Program Files\\Game Lister\\gameLister.exe'
    
    if not regedit.is_protocol_reg_created(protocol_name):
        if not is_admin():
                # Solicita elevação de privilégios e reinicia o script
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(map(str, sys.argv)), None, 1)
            sys.exit(0)
            
        regedit.check_and_create_protocol_reg(protocol_name, executable_path)
        

    # ================== # 
    #  Laucher Openners  #
    # ================== #
    
    # Verifica se algum argumento foi passado
    if len(sys.argv) > 1:
        
        commmand = sys.argv[1]
        
        if commmand.startswith('gamelister://'):
            commmand = commmand.replace("gamelister://", "", 1)
    
        if 'open_launcher' in commmand:
            
            subCommmand = commmand.replace("open_launcher/", "", 1)
        
            open_launcher(subCommmand)

                
        else:
            print("Argumento não reconhecido: " + commmand)
    else:
        print("Nenhum argumento fornecido.")

if __name__ == "__main__":
    main()

    pass

