#! /usr/bin/env python3

""""
# Rhyolite
A program for generating a mirror of the source code
with the markdown comments rendered
"""

import argparse
import pathlib
from file_tree import FileTree
from renderer import render
import jinja2

""""
# get_args
Parses the args provided by the user.
"""
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            prog="rhyolite",
            description="Generates html documentation for a project")
    parser.add_argument("-i","--in-files",
            help="List of files to generate documentation for",
            required=True,
            type=str,
            action="extend",
            nargs="+")

    parser.add_argument("-o", "--out-dir",
                        help="Where to place the rendered documentation",
                        required=True)

    parser.add_argument("-r", "--root-dir",
                        help="The root directory of the project",
                        default=".",
                        type=str)

    return parser.parse_args()

""""
# code_gen
- in_file_url
- build_dir_url
- template: jinja2 template used to generate the final file
"""
def code_gen(in_file_url: str, build_dir_url: str, template: jinja2.Template, root_node):
    in_file = open(in_file_url, "r")
    out_file_url = "./" + build_dir_url + "/" + in_file_url + ".html"
    rendered_html = render(in_file)

    pathlib.Path(out_file_url).parent.mkdir(parents=True, exist_ok=True)

    """"
    Figure out the position of the root directory in relation to the 
    file currently being rendered so that files like `index.js` can be
    correctly included
    """
    root_url = pathlib.Path(out_file_url).relative_to(build_dir_url)
    root_url_str = "./"
    for _ in range(1, len(root_url.parents)):
        root_url_str += "../"

    print(template.render(formatted_code = rendered_html, root_node=root_node, root_url=root_url_str), file=open(out_file_url, "w"))

def main():
    args = get_args()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("codegen"))
    page_template = env.get_template("page.html")
    tree_template = env.get_template("file_tree_page.html")

    tree = FileTree(args.in_files, args.root_dir)
    print(tree.root_node)
    for in_file_url in args.in_files:
        code_gen(in_file_url, args.out_dir, page_template, tree.root_node)
    print(tree_template.render(root_node = tree.root_node, root_url="./"), file=open(args.out_dir + "/index.html", "w"))

if __name__ == "__main__":
    main()
