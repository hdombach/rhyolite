build_dir = build
rhyolite_src = main.py

include rhyolite.mk

all: rhyolite_src

clean:
	rm -r build
