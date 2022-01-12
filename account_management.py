def check_parent_pass(password:str, file_name = 'Drive_folder/password.txt')->bool:
    with open(file_name,'r') as f:
        first_line = f.readline()
        f.close()
        first_line = first_line.replace('\n','')
        if password == first_line:
            return True
        else:
            return False

def change_password(new_pass_parent=None, new_pass_children=None, file_name = 'Drive_folder/password.txt'):
    with open(file_name, 'r') as f:
        pass_parent = f.readline()
        pass_children = f.readline()
        if new_pass_parent:
            pass_parent = new_pass_parent + '\n'
        if new_pass_children:
            pass_children = new_pass_children
        f.close()

    with open(file_name, 'w') as f:
        f.writelines([pass_parent, pass_children])
        f.close()

change_password(new_pass_parent='parent',new_pass_children='child')