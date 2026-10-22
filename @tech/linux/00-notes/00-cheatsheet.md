# Linux cheatsheet

## Files and permissions

```sh
ls -lah                             # sizes human readable, hidden files included
stat file                           # inode, permissions in octal, all three timestamps
find . -name '*.log' -mtime +7      # .log files older than 7 days
du -sh * | sort -h                  # what is eating the disk here
df -h                               # free space per filesystem
ln -s target link                   # symbolic link
```

Permission bits: `r=4 w=2 x=1`, in the order user, group, others. `chmod 640 f` is
`rw-r-----`. On a directory, `x` means "may enter", `r` means "may list".

## Processes and signals

```sh
ps aux --sort=-%mem | head          # top memory consumers
pgrep -af java                      # find processes by name, with full command line
kill -TERM <pid>                    # ask to stop (15), the handler can clean up
kill -KILL <pid>                    # force stop (9), cannot be trapped
jobs; fg %1; bg %1                  # shell job control
nohup cmd > out.log 2>&1 &          # survive the terminal closing
```

Exit code after a signal is `128 + n`: 130 for INT, 137 for KILL, 143 for TERM.
See [`01-snippets/00-graceful-shutdown-with-trap`](../01-snippets/00-graceful-shutdown-with-trap/).

## systemd

```sh
systemctl status nginx              # state, main pid, last log lines
systemctl restart nginx
systemctl enable --now nginx        # start now and on every boot
journalctl -u nginx -f              # follow one unit's logs
journalctl -p err -b                # errors since the last boot
```

## Text

```sh
grep -rn 'pattern' dir              # recursive, with line numbers
awk -F: '{print $1}' /etc/passwd    # first field of each line
sed -n '10,20p' file                # lines 10 to 20
sort | uniq -c | sort -rn           # frequency count, most common first
tail -f file                        # follow a growing file
```

## Network

```sh
ip -br addr                         # interfaces and addresses, one per line
ss -tlnp                            # listening TCP sockets and their processes
dig +short example.com              # resolve a name
curl -sv https://example.com        # request with headers and TLS details
tcpdump -i any port 443 -nn         # watch packets on a port
```

## Performance

```sh
uptime                              # load average over 1, 5, 15 minutes
vmstat 1                            # run queue, memory, swap, IO wait every second
free -h                             # memory, where "available" is the number that matters
strace -f -p <pid>                  # system calls of a running process
lsof -p <pid>                       # files and sockets a process holds open
```
