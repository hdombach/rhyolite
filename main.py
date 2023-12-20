#! /usr/bin/env python3

""""
# Rhyolite
A program for generating a mirror of the source code
with the markdown comments rendered
"""

import argparse
from io import TextIOWrapper
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import pygments.token
import markdown

""""
## get_args
Parses the args provided by the user.
"""
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            prog="rhyolite",
            description="Generates html documentation for a project")
    parser.add_argument("-i", "--in-files", required=True)
    parser.add_argument("-o", "--out-dir", required=True)
    return parser.parse_args()

""""
## convert_md
Converts markdown source to html.
**NOTE** Is context dependent becuase it assumes it is
inside a `<pre>a element.
"""
def convert_md(md_src: str, indent):
    result = ""
    for line in md_src.splitlines():
        for _ in range(0, indent):
            if not line[0].isspace():
                break;
            line = line[1:]
        result += line + "\n"
    result = markdown.markdown(result)
    return '</pre><div class="markdown_block">' + result + '</div><pre>'

""""
## CodeHtmlFormatter
A class that makes sure comments with the special tage get rendered
by the markdown package instead of `pygments`
"""
class CodeHtmlFormatter(HtmlFormatter):
    def __init__(self):
        super().__init__()

    """"
    ### format
    - tokensource: List of tokens provided by the lexer
    - outfile:
    Makes sure special comments are skipped by `pygments`
    I chose to convert the token type to `pygments.token.Token` because
    it appears that `HtmlFormatter` leaves it alone
    """
    def format(self, tokensource, outfile):
        more_tokens = []
        for token in tokensource:
            if '""""' in token[1]:
                more_tokens.append((pygments.token.Token, token[1]))
            else:
                more_tokens.append(token)
        super().format(more_tokens, outfile)

    """"
    ### wrap
    - source: List of strings that get rendered by the format function.
    Renders the markdown comments and inserts line numbers.
    Is called after the source code is colorized by `pygment`.
    """
    def wrap(self, source):
        is_md = False
        clump = ""
        line_num = 0

        yield 0, '<pre>'
        for i, t in source:
            if is_md:
                if "&quot;&quot;&quot;" in t:
                    indent = t.find("&")
                    temp_src = clump
                    clump = ""
                    is_md = False
                    yield 1, convert_md(temp_src, indent)
                else:
                    clump += t
            else:
                if "&quot;&quot;&quot;&quot;\n" in t:
                    is_md = True
                else:
                    yield i, f"<span class=\"num\">{line_num}</span>" + t
            line_num += 1
        yield 0, '</pre>'

""""
## render
- in_file
- out_file
Primary function for rendering a source code file
"""
def render(in_file: TextIOWrapper, out_file: TextIOWrapper):
    in_text = in_file.read()
    formatter = CodeHtmlFormatter()
    html_src = highlight(in_text, PythonLexer(), formatter)
    print(html_src, file=out_file)

def main():
    args = get_args()

    in_files = open(args.in_files, "r")
    out_file = open("./" + args.out_dir + "/" + args.in_files + ".html", "w")

    render(in_files, out_file)

if __name__ == "__main__":
    main()
