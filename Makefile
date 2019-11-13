
all:
	sudo rm -r build;\
	mkdir build;\
	cd build;\
	cmake ../;\
	sudo make install;\
	sudo ldconfig;\
	sudo gnuradio-companion;