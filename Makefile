build_dir = build
rhyolite_src = main.py renderer.py file_tree.py lang_handlers.py README.md test/*

include rhyolite.mk

all: rhyolite_gen

clean:
	rm -r build
