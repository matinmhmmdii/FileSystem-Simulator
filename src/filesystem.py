from typing import Optional
from .node import Directory, File

class FileSystem:
    def __init__(self):
        self.root = Directory("", None)
        self.current_directory = self.root

    def resolve_path(self, path: str) -> Directory:
        if not path:
            return self.current_directory
        if path == "/":
            return self.root
        if path.startswith("/"):
            current = self.root
            path = path[1:]
        else:
            current = self.current_directory
        parts = path.strip("/").split("/")
        for part in parts:
            if part == "..":
                if current.parent:
                    current = current.parent
            elif part:
                child = current.get_child(part)
                if not isinstance(child, Directory):
                    raise ValueError(f"Path not found or not a directory: {part}")
                current = child
        return current

    def mkdir(self, path: str, folder_name: str):
        try:
            parent = self.resolve_path(path)
            if folder_name in parent.children:
                raise ValueError(f"Directory '{folder_name}' already exists")
            new_dir = Directory(folder_name, parent)
            parent.add_child(new_dir)
        except ValueError as e:
            print(f"Error: {e}")

    def touch(self, path: str, file_name: str):
        try:
            parent = self.resolve_path(path)
            if file_name in parent.children:
                raise ValueError(f"File '{file_name}' already exists")
            new_file = File(file_name, parent)
            parent.add_child(new_file)
        except ValueError as e:
            print(f"Error: {e}")

    def rm(self, path: str):
        try:
            parent_path, name = path.rsplit("/", 1) if "/" in path else ("", path)
            parent = self.resolve_path(parent_path)
            if name not in parent.children:
                raise ValueError(f"Path not found: {name}")
            parent.remove_child(name)
        except ValueError as e:
            print(f"Error: {e}")

    def cd(self, path: str):
        try:
            self.current_directory = self.resolve_path(path)
        except ValueError as e:
            print(f"Error: {e}")

    def ls(self):
        children = sorted(self.current_directory.children.keys())
        print(" ".join(children) if children else "Empty directory")

    def nwfiletxt(self, path: str):
        try:
            parent_path, name = path.rsplit("/", 1) if "/" in path else ("", path)
            parent = self.resolve_path(parent_path)
            node = parent.get_child(name)
            if not isinstance(node, File):
                raise ValueError(f"File not found or not a file: {name}")
            print("Enter the lines (/end/ means done)")
            lines = []
            while True:
                line = input()
                if line == "/end/":
                    break
                lines.append(line)
            node.content = lines
        except ValueError as e:
            print(f"Error: {e}")

    def appendtxt(self, path: str):
        try:
            parent_path, name = path.rsplit("/", 1) if "/" in path else ("", path)
            parent = self.resolve_path(parent_path)
            node = parent.get_child(name)
            if not isinstance(node, File):
                raise ValueError(f"File not found or not a file: {name}")
            print("Enter the lines (/end/ means done)")
            while True:
                line = input()
                if line == "/end/":
                    break
                node.append(line)
        except ValueError as e:
            print(f"Error: {e}")

    def editline(self, path: str, line_num: int, text: str):
        try:
            parent_path, name = path.rsplit("/", 1) if "/" in path else ("", path)
            parent = self.resolve_path(parent_path)
            node = parent.get_child(name)
            if not isinstance(node, File):
                raise ValueError(f"File not found or not a file: {name}")
            node.edit_line(line_num, text)
        except ValueError as e:
            print(f"Error: {e}")

    def cat(self, path: str):
        try:
            parent_path, name = path.rsplit("/", 1) if "/" in path else ("", path)
            parent = self.resolve_path(parent_path)
            node = parent.get_child(name)
            if not isinstance(node, File):
                raise ValueError(f"File not found or not a file: {name}")
            print("\n".join(node.content) if node.content else "Empty file")
        except ValueError as e:
            print(f"Error: {e}")