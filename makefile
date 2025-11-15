.PHONY: run

run:
	cmake -S . -B cmake-build-debug
	cmake --build cmake-build-debug
	cp cmake-build-debug/C_Triangle hypotenuse
	./hypotenuse $(ARGS)


build:
	cmake -S . -B cmake-build-debug
	cmake --build cmake-build-debug
