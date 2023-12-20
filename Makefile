build_dir = build
rhyolite_src = main.py

include rhyolite.mk

all: rhyolite_gen

clean:
	rm -r build
