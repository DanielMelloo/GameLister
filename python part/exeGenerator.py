import PyInstaller.__main__
import os
import ctypes
import sys
import shutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def create_executable(script_name, executable_name, release_dir):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(current_dir, script_name)

    if not os.path.exists(main_py_path):
        print(f"'{script_name}' não encontrado.")
        return

    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    PyInstaller.__main__.run([
        main_py_path,
        '--onefile',
        '--noconsole',
        f'--distpath={release_dir}',
        f'--name={executable_name}',
        f'--specpath={release_dir}',
    ])

    print(f"Executável '{executable_name}.exe' criado em {release_dir}")

def copy_executable(executable_name, source_dir, destination_dir):
    source_path = os.path.join(source_dir, executable_name + '.exe')
    destination_path = os.path.join(destination_dir, executable_name + '.exe')

    if not os.path.exists(source_path):
        print("Executável não encontrado. Não foi possível copiar.")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    shutil.copyfile(source_path, destination_path)
    print(f"Executável copiado para {destination_path}")

if __name__ == "__main__":
    
    # if not is_admin():
    #         # Solicita elevação de privilégios e reinicia o script
    #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(map(str, sys.argv)), None, 1)
    #     sys.exit(0)
    
    script_to_convert = "main.py"
    executable_name = "gameLister"
    release_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release')
    create_executable(script_to_convert, executable_name, release_dir)

        
    # destination_dir = r"C:\Program Files\Game Lister"
    # copy_executable(executable_name, release_dir, destination_dir)

    # input("Pressione Enter para continuar...")