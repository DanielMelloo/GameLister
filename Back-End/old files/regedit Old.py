import os
import subprocess
import winreg
import sys

def check_protocol_registration(protocol_name):
    try:
        # Try to open the registry key
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, protocol_name)
        
        # If the key exists, close it and return True
        winreg.CloseKey(registry_key)
        return True
    except FileNotFoundError:
        # If the key does not exist, return False
        return False

def create_protocol_reg(path_exe):
    # Define o nome do protocolo
    protocol_name = "gameLister"

    # Cria a string de comando para o registro
    reg_command = f'''
    Windows Registry Editor Version 5.00

    [HKEY_CLASSES_ROOT\{protocol_name}]
    @="URL:{protocol_name} Protocol"
    "URL Protocol"=""

    [HKEY_CLASSES_ROOT\{protocol_name}\shell]

    [HKEY_CLASSES_ROOT\{protocol_name}\shell\open]

    [HKEY_CLASSES_ROOT\{protocol_name}\shell\open\command]
    @="\"{path_exe}\" \"%1\""

    '''

    # Caminho do arquivo .reg temporário
    archive_reg_temp = os.path.join(path_exe, "temp_registro.reg")


    # Escreve o comando no arquivo .reg temporário
    with open(archive_reg_temp, "w") as file:
        file.write(reg_command)

    # Executa o arquivo .reg
    try:
        subprocess.run(f"regedit /s {archive_reg_temp}", check=True, shell=True)
        print("Registro do protocolo criado com sucesso.")
    except subprocess.CalledProcessError:
        print("Erro ao criar o registro do protocolo. Certifique-se de executar como administrador.")
    finally:
        # Remove o arquivo temporário
        os.remove(archive_reg_temp)

def check_and_create_protocol_reg(program_path): 
    protocol_name = "gameLister"
    if check_protocol_registration(protocol_name):
        print(f"The protocol '{protocol_name}' is already registered.")
    else:
        print(f"The protocol '{protocol_name}' is not registered.")


    create_protocol_reg( os.path.join(program_path, '\\gameLister.exe'))
    

# Exemplo de uso
if __name__ == "__main__":
    print(check_protocol_registration('gameLister'))
    # check_and_create_protocol_reg("C:\\Program Files\\Game Lister")
    # print(check_protocol_registration('gameLister'))

    pass
