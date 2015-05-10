all:
	cp client.py cperf
	chmod +x cperf
	cp arbiter.py arbiter
	chmod +x arbiter
	gcc -shared -c -fPIC raw_socket.c -o function.o
	gcc -shared -Wl,-soname,library.so -o library.so function.o
	
