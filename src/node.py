from typing import Dict, List, Optional

class Node:
    def __init__(self, name: str, parent: Optional['Directory'] = None):
        self.name = name
        self.parent = parent

    def get_path(self) -> str:
        if self.parent is None:
            return "/"
        parent_path = self.parent.get_path()
        return f"{parent_path}/{self.name}" if parent_path != "/" else f"/{self.name}"

class File(Node):
    def __init__(self, name: str, parent: 'Directory'):
        if not name.endswith(".txt"):
            name += ".txt"
        super().__init__(name, parent)
        self.content: List[str] = []

    def append(self, text: str):
        self.content.append(text)

    def edit_line(self, line_num: int, text: str):
        if not isinstance(line_num, int) or line_num < 1:
            raise ValueError("Line number must be a positive integer")
        if line_num > len(self.content) + 1:
            raise ValueError(f"Line number {line_num} is out of range (file has {len(self.content)} lines)")
        if line_num > len(self.content):
            self.content.append(text)
        else:
            self.content[line_num - 1] = text

class Directory(Node):
    def __init__(self, name: str, parent: Optional['Directory'] = None):
        super().__init__(name, parent)
        self.children: Dict[str, Node] = {}

    def add_child(self, node: Node):
        self.children[node.name] = node
        node.parent = self

    def remove_child(self, name: str):
        if name in self.children:
            del self.children[name]

    def get_child(self, name: str) -> Optional[Node]:
        return self.children.get(name)