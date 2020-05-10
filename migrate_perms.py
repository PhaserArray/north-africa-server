from sys import argv
from os.path import abspath, join
from xml.etree import ElementTree


old_file_path = None
new_file_path = None
out_folder_path = None

if len(argv) == 4:
    print("Three arguments provided, attempting to parse as paths.")
    old_file_path = abspath(argv[1])
    new_file_path = abspath(argv[2])
    out_folder_path = abspath(argv[3])
else:
    print(f"{len(argv)-1} arguments provided, please input the relative/absolute paths.")
    old_file_path = abspath(input("Enter old perms file path: "))
    new_file_path = abspath(input("Enter new perms file path: "))
    out_folder_path = abspath(input("Enter output folder path: "))

print(f"\nOld perms file path: {old_file_path}")
print(f"New perms file path: {new_file_path}")
print(f"Out perms folder path: {out_folder_path}\n")


print("Grabbing members from the old perms file!")
old_perms_members = {}
with open(old_file_path, mode="r") as old_file:
    old_perms_groups = ElementTree.parse(old_file).findall(".//Groups/Group")
    for old_group in old_perms_groups:
        old_perms_members[old_group.find("Id").text] = list(old_group.find("Members"))


print("Adding members to the new perms file.")
with open(new_file_path, mode="r+") as new_file:
    new_tree = ElementTree.parse(new_file)
    new_perms_groups = new_tree.getroot().findall(".//Groups/Group")
    for new_group in new_perms_groups:
        id = new_group.find("Id").text
        if id in old_perms_members:
            new_group.find("Members").extend(old_perms_members[id])
    new_tree.write(join(out_folder_path, "Permissions.config.xml.output"))
print("Done! Don't remember to remove .output from the end of the file before you move it to the server!")