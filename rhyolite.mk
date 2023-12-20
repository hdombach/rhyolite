# reguires rhyolite_src, build_dir

rhyolite_gen:
	mkdir -p build
	cp -r static/* build
	./main.py --in-files $(rhyolite_src) --out-dir $(build_dir)
