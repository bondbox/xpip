MAKEFLAGS += --always-make

all: build reinstall test


clean:
	make -C xpip-build clean
	make -C xpip-mirror clean
	make -C xpip-upload clean


build:
	make -C xpip-build build
	make -C xpip-mirror build
	make -C xpip-upload build


install:
	make -C xpip-build install
	make -C xpip-mirror install
	make -C xpip-upload install

uninstall:
	make -C xpip-build uninstall
	make -C xpip-mirror uninstall
	make -C xpip-upload uninstall

reinstall: uninstall install


upload:
	make -C xpip-build upload
	make -C xpip-mirror upload
	make -C xpip-upload upload


test:
	make -C xpip-build test
	make -C xpip-mirror test
	make -C xpip-upload test
