build_dir = build
rhyolite_src = main.py renderer.py

include rhyolite.mk

all: rhyolite_gen

clean:
	rm -r build
