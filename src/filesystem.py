from typing import Optional
from copy import deepcopy
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

    def deline(self, path: str, line_num: int):
        try:
            parent_path, name = path.rsplit("/", 1) if "/" in path else ("", path)
            parent = self.resolve_path(parent_path)
            node = parent.get_child(name)
            if not isinstance(node, File):
                raise ValueError(f"File not found or not a file: {name}")
            node.delete_line(line_num)
        except ValueError as e:
            print(f"Error: {e}")

    def mv(self, src_path: str, dst_path: str):
        try:
            src_parent_path, src_name = src_path.rsplit("/", 1) if "/" in src_path else ("", src_path)
            src_parent = self.resolve_path(src_parent_path)
            node = src_parent.get_child(src_name)
            if not node:
                raise ValueError(f"Source path not found: {src_path}")
            dst_parent_path, dst_name = dst_path.rsplit("/", 1) if "/" in dst_path else ("", dst_path)
            dst_parent = self.resolve_path(dst_parent_path)
            dst_node = dst_parent.get_child(dst_name)
            if isinstance(dst_node, Directory):
                dst_parent = dst_node
                dst_name = src_name
            elif dst_node:
                raise ValueError(f"Destination already exists: {dst_path}")
            src_parent.remove_child(src_name)
            node.name = dst_name if dst_name else src_name
            if isinstance(node, File) and not node.name.endswith(".txt"):
                node.name += ".txt"
            dst_parent.add_child(node)
            node.parent = dst_parent
        except ValueError as e:
            print(f"Error: {e}")

    def cp(self, src_path: str, dst_path: str):
        try:
            src_parent_path, src_name = src_path.rsplit("/", 1) if "/" in src_path else ("", src_path)
            src_parent = self.resolve_path(src_parent_path)
            node = src_parent.get_child(src_name)
            if not node:
                raise ValueError(f"Source path not found: {src_path}")
            dst_parent_path, dst_name = dst_path.rsplit("/", 1) if "/" in dst_path else ("", dst_path)
            dst_parent = self.resolve_path(dst_parent_path)
            if dst_name in dst_parent.children:
                raise ValueError(f"Destination already exists: {dst_path}")
            if isinstance(node, File):
                new_file = File(dst_name, dst_parent)
                new_file.content = deepcopy(node.content)
                dst_parent.add_child(new_file)
            else:
                new_dir = Directory(dst_name, dst_parent)
                dst_parent.add_child(new_dir)
                self._copy_directory(node, new_dir)
        except ValueError as e:
            print(f"Error: {e}")

    def _copy_directory(self, src_dir: Directory, dst_dir: Directory):
        for name, node in src_dir.children.items():
            if isinstance(node, File):
                new_file = File(name, dst_dir)
                new_file.content = deepcopy(node.content)
                dst_dir.add_child(new_file)
            else:
                new_subdir = Directory(name, dst_dir)
                dst_dir.add_child(new_subdir)
                self._copy_directory(node, new_subdir)

    def rename(self, path: str, new_name: str):
        try:
            parent_path, name = path.rsplit("/", 1) if "/" in path else ("", path)
            parent = self.resolve_path(parent_path)
            node = parent.get_child(name)
            if not node:
                raise ValueError(f"Path not found: {path}")
            if new_name in parent.children:
                raise ValueError(f"Name '{new_name}' already exists")
            if isinstance(node, File) and not new_name.endswith(".txt"):
                new_name += ".txt"
            parent.remove_child(name)
            node.name = new_name
            parent.add_child(node)
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