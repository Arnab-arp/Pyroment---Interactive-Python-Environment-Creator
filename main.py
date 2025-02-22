import os
import json
import sys
import shutil
from platform import system

from prettytable import PrettyTable
from tkinter import filedialog

CONFIG = os.path.join(os.getcwd(), 'PYROMENT_ENV_PATHS.json')
def LoadJson():
    global CONFIG

    if not os.path.exists(CONFIG):
        return {}

    with open(CONFIG, 'r') as f:
        return json.load(f)

def AddJson(data):
    global CONFIG
    with open(CONFIG, 'w') as f:
        json.dump(data, f, indent=4)
    return


def ShowOptions():
    options = ('Create An Environment',
               'Select Environment From List',
               'Choose Existing Environment',
               'Delete Environment',
               'Exit')
    for ind, val in enumerate(options):
        print(
            f'({ind + 1}) {val}'
        )
    return

def ActivateEnvironment(env_path):
    env_name = os.path.basename(env_path)
    if not os.path.exists(os.path.join(env_path, 'Scripts/Activate.ps1')):
        print("(-) The Folder You Have Selected Is Not An Environment Directory")
        os.system('pause')
        os.system('cls')
        return
    temp_dec = input(f'Do You Want To Activate >> {env_name} << (y/n)? ').lower()
    if temp_dec == 'y':
        os.system('cls')
        cmd = 'powershell -Noexit -Command "& {Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force;cd %envname%\Scripts; .\Activate.ps1; cd ..; cd ..;}'.replace(
            '%envname%', env_path)
        os.system(cmd)
        os.system('cls')
        return
    os.system('cls')
    return

def CreateEnvironment():
    os.system('cls')
    print('------------------------------------------------------')
    print('                (Create Environment)                  ')
    print('------------------------------------------------------\n')

    env_name = input("Name Of Your Environment (q to quit): ")
    if env_name.lower() == 'q':
        os.system('cls')
        return
    print('Select Folder Where The Environment Will Be Created')
    env_path = filedialog.askdirectory(title="Select Folder")

    print('--------------- [INFO] --------------- ')
    print(
        f'-> Environment Name       : {env_name}\n'
        f'-> Environment Location   : {env_path}\n'
        f'-> Python Version         : {sys.version}'
    )
    print('--------------- [INFO] --------------- ')

    temp_dec = input('Do You Want To Proceed (y/n)? ').lower()
    if temp_dec != 'y':
        return
    os.system('cls')
    print('(-) Setting Execution Policy to RemoteSigned for the current user')
    os.system('powershell -Command "& {Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force}')
    print('(-) Command Execution Successful')

    set_path = os.path.join(env_path, env_name)
    print(f'(-) Creating Environment : {env_name}\n'
          f'(-) Location : {env_path}')

    os.system(f'python -m venv {set_path}')
    print('(-) Environment Created Successfully\n')
    venv_data = LoadJson()
    venv_data[env_name] = set_path
    AddJson(venv_data)

    ActivateEnvironment(set_path)

    return

def SelectFromList():
    os.system('cls')

    print('----------------------------------------------------')
    print('                (Select From List)                  ')
    print('----------------------------------------------------\n')

    venv_data = LoadJson()
    if len(venv_data) == 0:
        print(f'Currently There Are No Environment Path Registered in {CONFIG} file.'
              f'Please Create An Environment First Or If You Already Have An Existing'
              f'Environment Select The third Option "Choose Existing Environment" '
              f'From Options To Add It In The List.')
        os.system('pause')
        os.system('cls')
        return

    table = PrettyTable(['Environment Name', 'Environment Path'])
    for key, value in venv_data.items():
        table.add_row([key, value])
    print(table)

    flg = True
    set_path = None
    while flg:
        _name = input("Enter Environment Name (q to quit): ")
        if _name.lower() == 'q':
            os.system('cls')
            return
        if _name not in venv_data.keys():
            print('\n(-) Invalid Name. Write The Name From The List.\n')
        else:
            flg = False
            set_path = venv_data[_name]

    ActivateEnvironment(set_path)

def ChooseExisting():
    os.system('cls')
    print('--------------------------------------------------------')
    print('                (Existing Environment)                  ')
    print('--------------------------------------------------------\n')
    venv_data = LoadJson()
    print('Select The Environment Folder')

    env_path = filedialog.askdirectory(title="Select Folder")
    if env_path == '':
        print('\n(-) No Directory Was Selected\n')
        os.system('pause')
        os.system('cls')
        return
    _name = os.path.basename(env_path)
    if _name not in venv_data.keys():
        venv_data[_name] = env_path
        AddJson(venv_data)
    ActivateEnvironment(env_path)

def Delete():
    os.system('cls')
    print('--------------------------------------------------------------------')
    print('                (Delete Environment - Danger Zone)                  ')
    print('--------------------------------------------------------------------\n')
    venv_data = LoadJson()
    if len(venv_data) == 0:
        print(f'Currently There Are No Environment Path Registered in {CONFIG} file.'
              f'Please Create An Environment First Or If You Already Have An Existing'
              f'Environment Select The third Option "Choose Existing Environment" '
              f'From Options To Add It In The List.')
        os.system('pause')
        os.system('cls')
        return

    table = PrettyTable(['Environment Name', 'Environment Path'])
    for key, value in venv_data.items():
        table.add_row([key, value])
    print(table)

    flg = True
    set_path = None
    _name = None
    while flg:
        _name = input("Enter Environment Name To Delete (q to quit): ")
        if _name.lower() == 'q':
            os.system('cls')
            return
        if _name not in venv_data.keys():
            print('\n(-) Invalid Name. Write The Name From The List.\n')
        else:
            flg = False
            set_path = venv_data[_name]
    print('\n** WARNING : YOU ARE ABOUT TO DELETE AN ENVIRONMENT. ONCE DELETED IT CAN NOT BE RECOVERED. **\n')

    print('--------------- [INFO] --------------- ')
    print(f'ENVIRONMENT NAME      : {_name}\n'
          f'ENVIRONMENT PATH      : {set_path}\n'
          f'** PLEASE DOUBLE CHECK EVERYTHING BEFORE PROCEEDING **')
    print('--------------- [INFO] --------------- \n')
    dec = input("Do you want to continue? (y/n) ").lower()
    if dec != 'y':
        os.system('cls')
        return
    print(f'(-) Deletion of Environment : {_name} [In Progress]')
    try:
        shutil.rmtree(set_path)
        del venv_data[_name]
        AddJson(venv_data)
        print(f'(-) Deletion of Environment : {_name} [Successful]')
    except Exception as e:
        print(f'(-) Deletion of Environment : {_name} [Unsuccessful]\n'
              f'(-) ERROR : {e}')
    finally:
        os.system('pause')
        os.system('cls')

def main():
    while True:
        print('-----------------------------------------------------------------------------')
        print(f'        Pyroment : A python Environment Manipulation Program\n'
              f'        Created By : Arnab Pramanik\n'
              f'        Version : 1.2 BETA\n'
              f'        Creation Date : 3rd Feb 2025\n'
              f'        Updated Date : 5th Feb 2025\n'
              f'        Supported OS : Windows 11')
        print('-----------------------------------------------------------------------------\n')
        ShowOptions()
        user = input('\nSelect Options: ')
        if user == '5':
            break
        elif user == '1':
            CreateEnvironment()
        elif user == '2':
            SelectFromList()
        elif user == '3':
            ChooseExisting()
        elif user == '4':
            Delete()




    pass

if __name__ == '__main__':
    main()
