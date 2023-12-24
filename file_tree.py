from os import error
from typing import Dict, List
from pathlib import Path
import pathlib

""""
Either represents a file or a dir in the [File Tree](#filetree)
"""

class TreeNode:
    def __init__(self, name: str, is_dir: bool = False, url="#"):
        self.name: str = name
        self.is_dir: bool = is_dir 
        self.children: Dict[str, "TreeNode"] = dict()
        self.url=url

    def tree_view(self, indent:int=0):
        result = ""
        for _ in range(0, indent):
            result += "|"
        if self.is_dir:
            result += "+"
        result += self.name
        result += "\n"
        for child in self.children.values():
            result += child.tree_view(indent+1)
        return result

    def __str__(self):
        return self.tree_view()

    """"
    ## lazy_get
    - name: Name of child to get
    Tries to get the child with the given name  
    If the child does not exist, a directory with that name
    is created and returned
    """
    def lazy_get(self, name: str) -> "TreeNode":
        if name not in self.children:
            self.add_child(TreeNode(name, is_dir=True))
        return self.children[name]

    """"
    ## add_child
    - child: Child to add
    """
    def add_child(self, child: "TreeNode"):
        if child.name in self.children:
            raise error(f"file {child.name} already in {self.name}")
        self.children[child.name] = child


""""
# FileTree
Tool for interacting with tree structure of files given to the program
"""

class FileTree:
    def __init__(self, files: List[str], root_dir_url):
        self.files = files
        self.root_dir = Path(root_dir_url).resolve()
        self.root_node = TreeNode(self.root_dir.name, is_dir=True, url="index.html")
        for file in files:
            self.add_path(file)

    def add_path(self, file_url: str):
        path = Path(file_url).resolve().relative_to(self.root_dir)
        if path.is_dir():
            return

        cur_node = self.root_node
        for part in path.parts[:-1]:
            cur_node = cur_node.lazy_get(part)
        cur_node.add_child(TreeNode(path.parts[-1], url=file_url + ".html"))
