# reguires rhyolite_src, rhyolite_build_dir

rhyolite_gen:
	mkdir -p build
	cp -r static/* build
	./main.py --in-files $(rhyolite_src) --out-dir $(rhyolite_build_dir)
