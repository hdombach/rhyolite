#! /usr/bin/env python3

""""
# Rhyolite
A program for generating a mirror of the source code
with the markdown comments rendered
"""

import argparse
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
    out_file = open("./" + build_dir_url + "/" + in_file_url + ".html", "w")
    rendered_html = render(in_file)

    print(template.render(formatted_code = rendered_html, root_node=root_node), file=out_file)

def main():
    args = get_args()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("codegen"))
    page_template = env.get_template("page.html")
    tree_template = env.get_template("file_tree_page.html")

    tree = FileTree(args.in_files, args.root_dir)
    print(tree.root_node)
    for in_file_url in args.in_files:
        code_gen(in_file_url, args.out_dir, page_template, tree.root_node)
    print(tree_template.render(root_node = tree.root_node), file=open(args.out_dir + "/index.html", "w"))

if __name__ == "__main__":
    main()
