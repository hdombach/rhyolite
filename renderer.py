""""
# Overview
Tools focused on actually rendering the source code.
Uses two primary outside tools: pygments for adding syntax
coloring and markdown for turning markdown to html
"""

from io import TextIOWrapper
import pathlib
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import pygments.token
import markdown

from lang_handlers import LangHandler, lang_handler


""""
# CodeHtmlFormatter
A class that makes sure comments with the special tage get rendered
by the markdown package instead of `pygments`  
The class has an internal state to keep track of whether it is currently
a markdown statement
## Properties
- _cur_indent: The indent of the markdown currently being parse
- _cur_clump: The accumalted markdown block currently being parse
"""

class CodeHtmlFormatter(HtmlFormatter):
    def __init__(self, lang_handler: LangHandler):
        super().__init__()
        self._cur_indent: int = 0
        self._cur_clump: str = ""
        self._is_md = False
        self._is_code = False
        self._lang_handler = lang_handler
        """"
        Extions provide links to headers, and emojis :smile:
        """
        self._md = markdown.Markdown(extensions=['toc', 'pymdownx.emoji'])

    def _reset_state(self):
        self._cur_indent = 0
        self._cur_clump = ""

    """"
    ## _md_token
    Returns whether a token is part of a md comment
    """
    def _md_token(self, token) -> bool:
        return self._lang_handler.is_md_token(token)

    """"
    ## format
    - tokensource: List of tokens provided by the lexer
    - outfile:  
      
    Makes sure special comments are skipped by `pygments`
    I chose to convert the token type to `pygments.token.Token` because
    it appears that `HtmlFormatter` leaves it alone
    """
    def format(self, tokensource, outfile):
        more_tokens = []
        for token in tokensource:
            if self._md_token(token):
                more_tokens.append((pygments.token.Token, token[1]))
            else:
                more_tokens.append(token)
        super().format(more_tokens, outfile)

    """"
    ## _start_md_block
      
    Adds html tags to start a md block
    (add end code tag if necessary)
    """
    def _start_md_block(self) -> str:
        result = ""
        result += self._end_code_block()
        if not self._is_md:
            result += '<div class="markdown_block">'
            self._is_md = True
        return result

    """"
    ## _start_code_block
      
    Adds html tags to start a code block
    (and end md tag if necessary)
    """
    def _start_code_block(self) -> str:
        result = ""
        result += self._end_md_block()
        if not self._is_code:
            result += "<pre class='code_block'>"
            self._is_code = True
        return result

    """"
    ## _end_md_block
      
    Adds html tags to end a md block
    """
    def _end_md_block(self) -> str:
        result = ""
        if self._is_md:
            result += "</div>"
            self._is_md = False;
        return result

    """"
    ## _end_code_block
      
    Adds html tags to end a code block
    """
    def _end_code_block(self) -> str:
        result = ""
        if self._is_code:
            result += "</pre>"
            self._is_code = False;
        return result

    """"
    ## _wrap_start
    Detects whether a md block starts in the wrap function  
      
    - src: The raw html that should be replaced with markdown
    """
    def _wrap_start_md(self, src: str):
        info = self._lang_handler.is_md_wrap_start(src)
        if info[0]:
            self._reset_state()
            self._cur_indent = info[1]
            return True
        else:
            return False

    """"
    ## _wrap_end
    Detects whether a md block ends in the wrap function  
      
    - src: The raw html
    """
    def _wrap_end_md(self, src: str):
        if self._lang_handler.is_md_wrap_end(src):
            return True
        else:
            self._cur_clump += src
            return False

    """"
    ## _wrap_num
    - html_src:
    - num
    Adds a number tag a line of html
    """
    def _wrap_line(self, html_src, num):
        result = self._start_code_block()
        result += f"<span class=\"num\">{num}</span>" + html_src
        return result


    """"
    ## _convert_md
    Converts markdown source to html.  
    **NOTE** Is context dependent becuase it assumes it is
    inside a `<pre>' element.
    """
    def _convert_md(self, md_src: str):
        result = ""
        for line in md_src.splitlines():
            for _ in range(0, self._cur_indent):
                if len(line) == 0 or not line[0].isspace():
                    break;
                line = line[1:]
            result += line + "\n"
        result = self._md.convert(result)
        return self._start_md_block() + result + self._end_md_block()


    """"
    ## wrap
    - source: List of strings that get rendered by the format function.  
      
    Renders the markdown comments and inserts line numbers.
    Is called after the source code is colorized by `pygment`.
    """
    def wrap(self, source):
        self._is_md = False
        self._is_code = False
        line_num = 0

        if self._wrap_start_md(""):
            yield 0, self._start_md_block()

        for i, t in source:
            if self._is_md:
                if self._wrap_end_md(t):
                    yield 1, self._convert_md(self._cur_clump)
            else:
                if self._wrap_start_md(t):
                    yield 0, self._start_md_block()
                else:
                    yield i, self._wrap_line(t, line_num)
            line_num += 1
            yield 0, ""

        if self._is_md:
            yield 1, self._convert_md(self._cur_clump)
        yield 0, self._end_md_block() + self._end_code_block()


""""
# render
- in_file
- out_file
- returns: The rendered html src code
Primary function for rendering a source code file
"""
def render(in_file: TextIOWrapper):
    in_text = in_file.read()
    formatter = CodeHtmlFormatter(lang_handler(pathlib.Path(in_file.name)))
    return highlight(in_text, PythonLexer(), formatter)


