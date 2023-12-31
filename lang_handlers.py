""""
# Overview
Tools that are used by the [renderer](renderer.py.html)
"""

from abc import abstractmethod
from typing import Tuple
import pygments
from pygments.lexers import get_lexer_for_filename
import pygments.token
import pathlib

""""
# lang_handler
Creates a handler by trying to detect the
langauge based on the file extensions
"""
def lang_handler(path: pathlib.Path):
    if path.suffix == ".py":
        return PythonHandler(path.name)
    elif path.suffix == ".md":
        return MarkdownHandler(path.name)
    elif path.suffix == ".h" or path.suffix == ".c":
        return CHandler(path.name)
    else:
        return LangHandler(path.name)

""""
# LangHandler
Abstract class that holds generic functions for all
implimented languages
"""
class LangHandler:
    def __init__(self, filename: str):
        self._filename = filename

    """"
    ## is_implimented
    Whether or not the class is handeled or not
    """
    def is_implimented(self) -> bool:
        return False

    def lexer(self):
        return get_lexer_for_filename(self._filename)

    """"
    ## is_md_token
    - token  
      
    Whether or not the token provided by pygments formatter
    contains a markdown start thing
    """
    @abstractmethod
    def is_md_token(self, token) -> bool:
        return False

    """"
    ## is_md_wrap_start 
    Detects whether or not the start of a md block is in the raw html
      
    ### params:
    - str
    - returns: (bool, int)  
    Wether or not it is the start and the indent
    """
    def is_md_wrap_start(self, src: str) -> Tuple[bool, int]:
        return False, 0

    """"
    ## is_md_wrap_end
    Detects whether or not the end of a md block is in the ray html

    ### params:
    - str
    - returns: bool
    """
    def is_md_wrap_end(self, src: str) -> bool:
        return False

""""
# PythonHandler
Impliments LangHandler for python
"""
class PythonHandler(LangHandler):
    def __init__(self, filename: str):
        super().__init__(filename)

    def is_implimented(self) -> bool:
        return True

    def is_md_token(self, token) -> bool:
        return '""""' in token[1] and pygments.token.Literal.String.Doc in token[0]

    def is_md_wrap_start(self, src: str) -> Tuple[bool, int]:
        return "&quot;&quot;&quot;&quot;\n" in src, src.find("&")

    def is_md_wrap_end(self, src: str) -> bool:
        return "&quot;&quot;&quot;" in src

""""
# MarkdownHandler
Impliments LangHandler for python
"""
class MarkdownHandler(LangHandler):
    def __init__(self, filename: str):
        super().__init__(filename)

    def is_implimented(self) -> bool:
        return True

    def is_md_token(self, token) -> bool:
        return True

    def is_md_wrap_start(self, src: str) -> Tuple[bool, int]:
        return True, 0

    def is_md_wrap_end(self, src: str) -> bool:
        return False

""""
# CHandler
Impliments LangHander for C
"""
class CHandler(LangHandler):
    def __init__(self, filename: str):
        super().__init__(filename)

    def is_implimented(self) -> bool:
        return True

    def is_md_token(self, token) -> bool:
        return '/**' in token[1] and pygments.token.Comment.Multiline in token[0]

    def is_md_wrap_start(self, src: str) -> Tuple[bool, int]:
        return '/**\n' in src, src.find('*')

    def is_md_wrap_end(self, src: str) -> bool:
        return '*/' in src
