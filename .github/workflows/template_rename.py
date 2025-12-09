#!/usr/bin/env python3
import os
import re
import sys

def main() -> None:
    # print(sys.argv, len(sys.argv))
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments!")
    
    repo_name = str(sys.argv[1])
    if repo_name.find('-PCB') == -1:
        raise ValueError("Incorrect repo name!")
    
    original_name = "hermes-template"
    new_name = repo_name.split('/')[1].replace('-PCB', '')
    
    if new_name.find('-') < 1:
        raise ValueError("Incorrect repo name!")
    
    placeholder_pretty_name = "template_pretty_name"
    project_name = new_name.split('-')[0].upper()
    pcb_name = new_name.split('-',1)[1].replace('-', ' ').title()
    pretty_name = project_name + ' ' + pcb_name + " Board"
    
    # Rename files
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))
    for root, dirs, files in os.walk(repo_root):
        for file in files:
            new_filename = file.replace(original_name, new_name)
            if new_filename != file:
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)

    os.rename(os.path.join(repo_root, "README.md"), os.path.join(repo_root, "USAGE.md"))
    os.rename(os.path.join(repo_root, "README.md.template"), os.path.join(repo_root, "README.md"))
    
    # Replace pretty name in files
    cmd = f"sed -i 's/{placeholder_pretty_name}/{pretty_name}/' README.md"
    os.system(cmd)
    cmd = f"sed -i 's/{placeholder_pretty_name}/{pretty_name}/' PCB/*.kicad_*"
    os.system(cmd)
    
    # Copy original PCB layout
    os.system(f"cp PCB/{new_name}-PCB.kicad_pcb PCB/.original_pcb_layout")

    return


if __name__ == '__main__':    
    main()
