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