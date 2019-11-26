# Paths into the lconfig submodule
LCONFIG=lconfig/lconfig.o
LCTOOLS=lconfig/lctools.o
LCONFIG_PY=lconfig/py/lconfig.py
LPLOT_PY=lconfig/py/lplot.py
# Binary target directory and source files
BIN_D=../bin
BIN_F=monitor.bin monitor.conf $(LCONFIG_PY) $(LPLOT_PY)

monitor.bin: $(LCONFIG) $(LCTOOLS) monitor.c
	gcc $(LCONFIG) $(LCTOOLS) -lm -lLabJackM monitor.c -o monitor.bin
	chmod +x monitor.bin

clean:
	rm -fv *.bin
	rm -fv *.o

install: $(BIN_F)
	cp monitor.bin $(BIN_D)/monitor
	cp monitor.conf $(BIN_D)/monitor.conf
