from typing import Optional
from .node import Directory

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
