LCONFIG=lconfig/lconfig.o
LCTOOLS=lconfig/lctools.o

monitor.bin: $(LCONFIG) $(LCTOOLS) monitor.c
	gcc $(LCONFIG) $(LCTOOLS) -lm -lLabJackM monitor.c -o monitor.bin
	chmod +x monitor.bin

clean:
	rm -fv *.bin
	rm -fv *.o

install: monitor.bin monitor.conf
	cp monitor.bin ../monitor
	cp monitor.conf ../monitor.conf
