# Kali Linux Commands — Complete Practical Guide
### Simple English • Beginner to Advanced • Command Examples • Cybersecurity & SOC Labs

> Use these commands only on your own Kali Linux machine, disposable virtual machine, or systems you have explicit permission to test. Some commands can delete data, change system settings, disconnect networking, or affect other users. Read the explanation before running a command.

## Table of Contents
1. How to read a command
2. Terminal basics and help
3. Navigation and file listing
4. Create, view, copy, move, and delete files
5. Search files and text
6. Paths, wildcards, quotes, and redirection
7. Users and groups
8. Permissions and ownership
9. Processes and jobs
10. System information and performance
11. Disk, partitions, file systems, and mounts
12. Packages and software
13. Network commands
14. DNS and web troubleshooting
15. SSH and secure file transfer
16. Logs and SOC investigation
17. Archives and compression
18. Text processing
19. Bash scripting basics
20. Scheduling tasks and services
21. Hashes, signatures, and file inspection
22. Security tools commonly found in Kali
23. Safe lab workflow
24. Troubleshooting commands
25. Common mistakes
26. Practice labs
27. Interview questions
28. Quick command cheat sheet
29. Official references

---

## 1. How to read a command

A terminal is a text-based way to tell the operating system what to do. Kali uses a Linux shell, commonly Bash.

Example:
```bash
ls -lah /home
```

- `ls` is the command.
- `-lah` contains options that change its behavior.
- `/home` is the argument telling it which location to list.

### Important symbols

| Symbol | Meaning |
|---|---|
| `~` | Your home directory in a shell |
| `/` | Root of the Linux directory tree |
| `.` | Current directory |
| `..` | Parent directory |
| `*` | Wildcard matching many names |
| `?` | Wildcard matching one character in shell patterns |
| `|` | Send one command's output into another command |
| `>` | Write output to a file, replacing existing contents |
| `>>` | Append output to a file |
| `2>` | Redirect error output |
| `&&` | Run the next command only if the previous command succeeds |
| `;` | Run the next command after the previous one finishes, whether it succeeds or fails |
| `$(...)` | Use the output of a command inside another command |
| `\` at line end | Continue a command on the next line |

**Be careful with spaces and quotes.** `my notes.txt` is two words to the shell unless quoted or escaped. Use `"my notes.txt"`.

## 2. Terminal basics and help

| Command | What it does | Example |
|---|---|---|
| `man` | Opens the manual for a command | `man ls` |
| `command --help` | Shows quick help when supported | `ip --help` |
| `help` | Help for Bash built-ins | `help cd` |
| `whatis` | One-line manual description, if its database is available | `whatis chmod` |
| `apropos` | Searches manual descriptions | `apropos network` |
| `history` | Shows commands in the current shell history | `history` |
| `clear` | Clears the visible terminal screen | `clear` |
| `reset` | Resets a confused terminal display | `reset` |
| `date` | Shows date and time | `date` |
| `cal` | Displays a calendar if installed | `cal` |
| `whoami` | Prints the current effective username | `whoami` |
| `id` | Shows user and group IDs | `id` |
| `pwd` | Prints the current directory | `pwd` |
| `echo` | Prints text or variable values | `echo "$HOME"` |
| `printf` | Prints formatted text reliably | `printf 'Hello\\n'` |
| `type` | Tells how the shell interprets a command name | `type cd` |
| `command -v` | Finds a command in the current shell environment | `command -v python3` |

Tip: press **Tab** to complete names and use the Up/Down arrow keys to review earlier commands. Press **Ctrl+C** to interrupt many running terminal commands. It does not undo changes already made.

## 3. Navigation and file listing

### Move between folders

```bash
pwd                 # Where am I?
ls                  # List the current folder
ls -l               # Detailed list
ls -a               # Include hidden names
ls -lah             # Detailed, human-readable sizes, including hidden names
cd /etc             # Go to /etc
cd ..               # Go to parent folder
cd ~                # Go to your home folder
cd -                # Return to the previous directory
```

### Understand common listing options

- `-l`: long format, including permissions, owner, size, and time.
- `-a`: show names beginning with a dot.
- `-h`: human-readable sizes such as KB or MB.
- `-R`: list recursively; output can become very large.
- `-d`: show the directory itself rather than listing its contents.

Examples:
```bash
ls -ld /etc
ls -lh /var/log
ls -lt                 # Sort by modification time, newest first
ls -ltr                # Reverse time order
```

### Inspect a path

```bash
file /etc/passwd       # Identify the kind of file
stat /etc/passwd       # Detailed metadata
readlink -f /bin/ls    # Resolve a path through symbolic links
realpath .             # Print an absolute path, if installed
namei -l /etc/hosts    # Show path components and permissions
```

A filename does not prove what the file contains. `file` checks file signatures and content clues, not whether the file is safe.

## 4. Create, view, copy, move, and delete files

### Create files and folders

```bash
mkdir practice
mkdir -p ~/kali-lab/docs
touch ~/kali-lab/docs/notes.txt
printf 'First line\\nSecond line\\n' > ~/kali-lab/docs/notes.txt
```

- `mkdir`: creates a directory.
- `mkdir -p`: also creates missing parent directories.
- `touch`: creates an empty file if it does not exist; otherwise it updates timestamps.
- `>`: creates or overwrites the destination file.

### Read file contents

| Command | Use |
|---|---|
| `cat file` | Print a small file |
| `less file` | Read long output page by page; press q to quit |
| `head file` | Show first 10 lines by default |
| `head -n 20 file` | Show first 20 lines |
| `tail file` | Show last 10 lines |
| `tail -n 50 file` | Show last 50 lines |
| `tail -f file` | Follow new lines as they are written |
| `nl -ba file` | Display lines with numbers |
| `wc -l file` | Count lines |
| `wc -w file` | Count words |
| `wc -c file` | Count bytes |

For logs, `tail -f` is useful for observing new events, but the file may require elevated permissions. Use only on logs you are allowed to access.

### Copy, move, rename, and delete

```bash
cp notes.txt notes-copy.txt
cp -r folder-a folder-b
mv oldname.txt newname.txt
mv notes.txt ~/kali-lab/
rm notes-copy.txt
rmdir empty-folder
```

- `cp`: copies files.
- `cp -r`: copies directories and their contents.
- `mv`: moves or renames.
- `rm`: deletes directory entries; it normally does not send files to a graphical Trash.
- `rmdir`: removes an empty directory.

**Danger:** Never test destructive commands on important files. Avoid casually running `rm -rf`, especially with wildcards, variables, or administrator privileges. Always check the path with `pwd` and `ls) first.

### Safer interactive options

```bash
cp -i source.txt destination.txt
mv -i source.txt destination.txt
rm -i test-file.txt
```

The `-i` option asks before overwriting or removing in supported commands. It is a helpful guard, not a replacement for checking paths.

## 5. Search files and text

### Find files by name, type, or size

```bash
find ~/kali-lab -type f
find ~/kali-lab -type f -name '*.txt'
find ~/kali-lab -type d
find ~/kali-lab -type f -size +10M
find ~/kali-lab -type f -mtime -7
```

- `-type f`: regular files.
- `-type d`: directories.
- `-name '*.txt'`: names ending in .txt. Quote the pattern so the shell does not expand it early.
- `-size +10M`: files larger than roughly 10 MiB according to find's size rules.
- `-mtime -7`: modified less than seven 24-hour periods ago.

Use a narrow starting folder. Searching the whole system can be slow and may produce permission errors.

### Search inside text

```bash
grep 'error' app.log
grep -i 'failed' app.log
grep -n 'failed' app.log
grep -in 'failed' app.log
grep -Rni 'TODO' ~/kali-lab
```

- `grep`: searches for matching text.
- `-i`: ignore letter case.
- `-n`: show line numbers.
- `-R`: search recursively.
- `-v`: show lines that do not match.
- `-E`: use extended regular expressions.

Search with context:
```bash
grep -n -C 2 'failed' app.log
```
This displays two lines before and after each match.

### Locate installed commands

```bash
command -v python3
which python3
whereis python3
locate notes.txt
```

`locate` depends on an installed and updated index, so it may be unavailable or stale. `which` is common, but `command -v` is often more reliable inside a shell.

## 6. Paths, wildcards, quotes, and redirection

### Wildcards

```bash
ls *.txt
ls report-?.txt
find . -type f -name '*.log'
```

- `*.txt` matches names ending in .txt in the current directory.
- `report-?.txt` matches one character in place of ?.
- Wildcards are expanded by the shell before a command receives its arguments.

### Quotes

```bash
mkdir "project notes"
printf '%s\\n' "A phrase with spaces"
```

- Double quotes preserve spaces but still allow variable expansion such as `"$HOME"`.
- Single quotes preserve the text literally, so variables are not expanded.
- Backslash can escape special characters, but quoting is often clearer.

### Redirect output

```bash
ls -la > listing.txt
date >> listing.txt
find ~/kali-lab -type f 2> errors.txt
command > output.txt 2>&1
```

- `>` replaces a file's contents.
- `>>` appends.
- `2>` redirects error messages.
- `2>&1` sends standard error to the same destination as standard output in this ordering.

### Pipes

```bash
ps aux | less
grep -i 'failed' auth.log | wc -l
find ~/kali-lab -type f | sort
```

A pipe sends one command's output to the next command as input. This is how small tools can be combined into useful workflows.

## 7. Users and groups

| Command | What it tells you |
|---|---|
| `whoami` | Current effective username |
| `id` | User ID, primary group, and group memberships |
| `groups` | Groups for the current user or named user |
| `getent passwd` | Account records from configured account sources |
| `getent group` | Group records from configured group sources |
| `who` | Users with logged-in sessions, depending on session setup |
| `w` | Logged-in users and activity summary |
| `last` | Login history from available accounting data |
| `passwd` | Change your password, or an account password with appropriate privileges |
| `sudo command` | Run a command with approved elevated privileges |
| `sudo -l` | Show commands the current user may run through sudo |

Account records:
- `/etc/passwd` usually lists local account metadata.
- `/etc/shadow` commonly stores protected local password hashes and aging information.
- `/etc/group` lists local groups.
- `/etc/gshadow` contains protected group-related information.

Do not publish credential files or their contents. Network identity services can change where account data is authoritative.

### Add or manage users (administrative changes)

```bash
sudo adduser labuser
sudo passwd labuser
sudo usermod -aG sudo labuser
id labuser
```

These commands change the machine. Use them only on your own VM and understand the effect before adding administrative group membership. To remove a test account, consult `man deluser` and back up any data first.

## 8. Permissions and ownership

Inspect permissions:
```bash
ls -l file.txt
stat file.txt
getfacl file.txt
```

Change basic permissions:
```bash
chmod 640 file.txt
chmod u+x script.sh
chmod go-rwx private.txt
```

Change owner/group (requires permission):
```bash
sudo chown labuser:labuser file.txt
```

### Numeric permission quick guide

| Number | Meaning |
|---:|---|
| 0 | no permissions |
| 1 | execute/search |
| 2 | write |
| 3 | write + execute |
| 4 | read |
| 5 | read + execute |
| 6 | read + write |
| 7 | read + write + execute |

Example: `chmod 640 file.txt` gives owner read/write, group read, and others no basic mode-bit access.

For a **directory**, read means listing names, execute means traversing/searching, and write means changing entries when the other access requirements are satisfied. Parent directory permissions also matter.

Avoid `chmod -R 777` as a general fix. It can expose data and allow unwanted changes.

## 9. Processes and jobs

A process is a running program. Each process has a process ID (PID).

```bash
ps
ps aux
top
htop
pgrep firefox
pidof ssh
pstree
```

- `ps aux`: snapshot of many processes.
- `top`: live process and resource view; press q to quit.
- `htop`: friendlier interactive viewer if installed.
- `pgrep`: find process IDs by name or pattern.
- `pstree`: display parent/child process relationships.

### Stop a process

```bash
kill PID
kill -TERM PID
kill -KILL PID
```

Replace PID with the actual process ID. TERM requests a graceful stop. KILL forces termination and should be a last resort because the process cannot clean up. Do not kill unfamiliar system processes blindly.

### Shell jobs

```bash
long_command &
jobs
fg
bg
```

The ampersand runs a command in the background. In an interactive shell, Ctrl+Z suspends the foreground job; `bg` resumes it in the background and `fg` brings it to the foreground.

### What files a process uses

```bash
lsof -p PID
lsof /path/to/file
fuser -v /path/to/file
```

These tools may need installation or elevated access. Use them only for processes and files you are authorized to inspect.

## 10. System information and performance

```bash
uname -a
hostname
hostnamectl
uptime
free -h
df -h
du -sh ~/kali-lab
lscpu
lsmem
vmstat 1
```

| Command | Meaning |
|---|---|
| `uname -a` | Kernel and system details |
| `hostnamectl` | Hostname and system identification on systemd systems |
| `uptime` | How long the system has been running and load averages |
| `free -h` | Memory summary |
| `df -h` | Space available on mounted file systems |
| `du -sh folder` | Approximate disk usage of a folder |
| `lscpu` | CPU information |
| `lsmem` | Memory block information on supported systems |
| `vmstat 1` | Repeated memory/process/I/O summary every second; Ctrl+C stops it |

Load average is not the same as CPU percentage. Interpret it with CPU count and other system metrics.

## 11. Disk, partitions, file systems, and mounts

Read-only inspection commands:
```bash
lsblk
lsblk -f
blkid
df -hT
du -sh /path
findmnt
mount
cat /etc/fstab
```

- `lsblk -f`: lists block devices and file-system information.
- `blkid`: identifies file-system labels and UUIDs.
- `df -hT`: shows space and file-system type for mounted systems.
- `findmnt`: shows mount relationships.
- `/etc/fstab`: configuration for file systems that may be mounted at boot.

Mounting/unmounting changes system state:
```bash
# Example only: requires a real, verified device and an appropriate mount point.
sudo mount /dev/DEVICE /mnt/lab
sudo umount /mnt/lab
```

Do not copy this placeholder literally. Never guess a device name. Incorrect mount, format, partition, or disk-write commands can destroy data. Do not run `mkfs`, `dd` to a device, or partition editors as casual practice.

## 12. Packages and software

Kali is based on Debian and uses APT for package management.

```bash
sudo apt update
apt search nmap
apt show nmap
sudo apt install nmap
sudo apt remove nmap
sudo apt autoremove
dpkg -l
dpkg -L nmap
command -v nmap
```

- `apt update`: refreshes package metadata; it does not itself upgrade installed packages.
- `apt search`: searches package names and descriptions.
- `apt show`: displays package information.
- `apt install`: installs software.
- `apt remove`: removes a package but may leave configuration files.
- `apt autoremove`: proposes removal of automatically installed packages no longer needed; review the list.
- `dpkg -l`: lists installed package records.
- `dpkg -L`: lists files installed by a package.

Upgrade only when you have a backup/snapshot and enough disk space:
```bash
sudo apt upgrade
```

Do not blindly add unknown repositories or run install scripts from untrusted sources as root.

## 13. Network commands

### Interfaces and addresses

```bash
ip addr
ip link
ip route
ip neigh
```

- `ip addr`: shows IP addresses and network interfaces.
- `ip link`: shows link status.
- `ip route`: shows routes and the default gateway.
- `ip neigh`: shows the neighbor cache, such as local IPv4 ARP entries or IPv6 neighbor data.

### Connectivity checks

```bash
ping -c 4 1.1.1.1
ping -c 4 example.com
tracepath example.com
```

A failed ping does not prove a host is offline; firewalls may block ICMP. Use only a small number of diagnostic requests.

### Listening sockets and connections

```bash
ss -tuln
ss -tunap
ip route
```

- `ss -tuln`: shows listening TCP/UDP sockets with numeric addresses/ports.
- `ss -tunap`: shows TCP/UDP sockets and processes where permissions allow.
- `sudo` may be needed to see process details.

### Transfer and web requests

```bash
curl -I https://example.com
curl -L https://example.com -o page.html
wget https://example.com/
```

- `curl -I`: requests response headers (server behavior varies).
- `curl -L`: follows redirects.
- `-o`: saves response content to a named file.
- `wget`: downloads content.

Only download files from trusted sources and inspect them before running. HTTPS does not guarantee a file is safe.

## 14. DNS and web troubleshooting

```bash
getent hosts example.com
dig example.com
dig A example.com
dig MX example.com
nslookup example.com
resolvectl status
cat /etc/resolv.conf
```

- `getent hosts`: uses configured system name-resolution sources.
- `dig`: queries DNS and shows detailed response data; install the package providing it if missing.
- `A`: IPv4 address record.
- `MX`: mail-exchange record.
- `nslookup`: another DNS query utility.
- `resolvectl status`: resolver details on systems using systemd-resolved.

### Check HTTP response details

```bash
curl -sS -D headers.txt -o body.html https://example.com/
curl -v https://example.com/
```

Verbose output can reveal request/response details. Do not share output that contains session cookies, authorization headers, or other secrets.

## 15. SSH and secure file transfer

SSH provides encrypted remote terminal access. Use it only for accounts and hosts you are authorized to access.

```bash
ssh username@host
ssh -p 2222 username@host
scp report.txt username@host:/home/username/
sftp username@host
```

- `ssh`: remote shell connection.
- `-p`: specifies the remote SSH port.
- `scp`: copies files over SSH.
- `sftp`: interactive file transfer over SSH.

### SSH keys

```bash
ssh-keygen -t ed25519
ls -la ~/.ssh
ssh -o IdentitiesOnly=yes username@host
```

Generate keys for your own account and protect the private key. The public key may be shared with a server administrator; the private key must not be uploaded to GitHub or sent to other people. Use a passphrase where practical.

Useful configuration paths:
- `~/.ssh/`: per-user SSH client keys and configuration.
- `/etc/ssh/sshd_config`: common SSH server configuration file.
- `/etc/ssh/`: system SSH configuration directory.

## 16. Logs and SOC investigation

### Read common log locations

```bash
ls -lah /var/log
sudo journalctl -n 100
sudo journalctl --since "1 hour ago"
sudo journalctl -u ssh
sudo journalctl -f
```

- `journalctl`: reads the systemd journal when available.
- `-n 100`: shows the last 100 entries.
- `--since`: filters by time.
- `-u ssh`: filters by service unit name; the actual unit may differ.
- `-f`: follows new entries.

Common file-based log paths can include:
- `/var/log/auth.log` on some Debian/Kali setups.
- `/var/log/syslog` on some setups.
- `/var/log/kern.log` on some setups.
- Service-specific logs under `/var/log/`.

Not every file exists on every installation. Some logs are stored only in the journal, and access/retention vary.

### Investigate a suspicious file without executing it

```bash
file suspicious.bin
stat suspicious.bin
sha256sum suspicious.bin
ls -l suspicious.bin
strings -n 8 suspicious.bin | head -n 50
```

- `file`: content-type clues.
- `stat`: metadata and timestamps.
- `sha256sum`: cryptographic hash for comparing exact content.
- `strings`: extracts printable sequences; it can produce false clues and does not prove intent.

Do not execute a suspicious file to “see what it does.” Preserve evidence and follow your organization's incident-response procedure.

### Authentication investigation

```bash
who
w
last
sudo journalctl --since today
```

Login records depend on system configuration and log retention. A missing event is not proof that an event did not happen.

### A simple SOC workflow
1. Record host, user, path, timestamp, alert, and scope.
2. Preserve evidence; do not delete or modify the file.
3. Inspect metadata, permissions, file type, and hash.
4. Review process, authentication, service, and network logs where available.
5. Compare with the host's normal behavior.
6. Escalate and document conclusions, confidence, and missing evidence.

## 17. Archives and compression

```bash
tar -czf lab-backup.tar.gz ~/kali-lab
tar -tzf lab-backup.tar.gz
tar -xzf lab-backup.tar.gz -C ~/restore-lab
gzip file.txt
gunzip file.txt.gz
zip -r lab.zip ~/kali-lab
unzip -l lab.zip
```

- `tar -czf`: creates a gzip-compressed tar archive.
- `tar -tzf`: lists archive contents without extracting.
- `tar -xzf`: extracts an archive.
- `-C`: chooses the extraction directory.
- `gzip`/ `gunzip`: compress/decompress individual files.
- `zip -r`: recursively creates a ZIP archive.
- `unzip -l`: lists ZIP contents.

Inspect archives before extracting. Archives may contain absolute paths, unusual names, or very large content. Extract untrusted archives into a dedicated empty folder.

## 18. Text processing

| Command | Use | Example |
|---|---|---|
| `sort` | Sort lines | `sort names.txt` |
| `uniq` | Remove adjacent duplicate lines | `sort names.txt | uniq` |
| `cut` | Select fields/columns | `cut -d: -f1 /etc/passwd` |
| `tr` | Translate/delete characters | `tr 'a-z' 'A-Z' < names.txt` |
| `sed` | Stream editing | `sed -n '1,10p' file.txt` |
| `awk` | Field-based text processing | `awk '{print $1}' file.txt` |
| `tee` | Show output and write it to a file | `command | tee output.txt` |
| `xargs` | Build command arguments from input | `printf '%s\\n' a b | xargs printf '%s\\n'` |
| `diff` | Compare text files | `diff old.txt new.txt` |
| `comm` | Compare sorted files | `comm a.txt b.txt` |

Be cautious when combining `find`, `xargs`, and deletion commands. First list the targets, inspect the output, and only then perform any authorized change.

## 19. Bash scripting basics

A script stores commands in a file so they can be repeated consistently.

Example safe script:
```bash
#!/usr/bin/env bash
set -u

printf 'User: %s\\n' "$USER"
printf 'Home: %s\\n' "$HOME"
printf 'Current directory: '
pwd

printf '\\nDisk usage for home:\\n'
df -h "$HOME"
```

Save it as `system-summary.sh`, then run:
```bash
chmod u+x system-summary.sh
./system-summary.sh
```

Basic concepts:
- `#!/usr/bin/env bash`: asks the environment to locate Bash.
- Variables: `name="value"`.
- Read a variable: `"$name"`.
- `if`, `case`, `for`, and `while`: control flow.
- `$?`: exit status of the previous command; 0 usually means success.
- `set -u`: report use of unset variables.
- `set -e`: can stop a script on errors, but has exceptions; understand it before relying on it.

Do not run scripts copied from the internet without reading and understanding them first, especially scripts that use `sudo`, download code, change firewall settings, or delete files.

## 20. Scheduling tasks and services

### Services on systemd systems

```bash
systemctl status ssh
systemctl list-units --type=service --state=running
journalctl -u ssh -n 50
```

Administrative changes:
```bash
sudo systemctl start SERVICE
sudo systemctl stop SERVICE
sudo systemctl restart SERVICE
sudo systemctl enable SERVICE
```

Replace SERVICE with the actual unit name. Start/stop/restart changes live system state. Enable usually configures a service to start at boot; it does not necessarily start it immediately.

### Scheduled tasks

```bash
crontab -l
crontab -e
systemctl list-timers
```

Cron schedule fields normally represent minute, hour, day of month, month, and day of week. Test scheduled scripts manually first and use absolute paths. Do not create persistence on machines you do not administer.

## 21. Hashes, signatures, and file inspection

```bash
sha256sum file.iso
sha512sum file.iso
md5sum file.iso
gpg --verify file.sig file
```

- SHA-256/SHA-512 hashes can help verify exact file identity.
- MD5 is legacy and should not be relied on for security against deliberate tampering.
- A signature can help establish authenticity if the signing key and verification process are trusted.
- A hash alone does not tell you whether a file is malicious.

For package checks and signed downloads, use the publisher's official verification instructions. Do not trust a hash copied from the same untrusted location as the file without independent validation.

## 22. Security tools commonly found in Kali

Kali contains many security tools, but packages vary by installation. Verify availability with `command -v TOOL` or `apt show PACKAGE`.

| Tool | General purpose | Safe beginner example |
|---|---|---|
| Nmap | Network discovery and service enumeration | `nmap -sV 127.0.0.1` against your own machine |
| Wireshark / tshark | Packet capture and analysis | Open a capture file you are authorized to analyze |
| tcpdump | Capture or inspect network packets | `sudo tcpdump -i lo` to observe loopback traffic; stop with Ctrl+C |
| Burp Suite | Inspect and test web requests | Configure a local training application and browser |
| OWASP ZAP | Web application security testing | Use its test features against a local lab |
| sqlmap | Automated SQL injection testing | Use only a deliberately vulnerable local lab you own |
| Nikto | Web server checks | Use only against an authorized lab target |
| Gobuster / ffuf | Content and path discovery | Use against a local practice app or explicitly authorized scope |
| John the Ripper / Hashcat | Password-audit tools | Use synthetic hashes in an offline training lab |
| Metasploit Framework | Exploit validation and security testing | Use intentionally vulnerable local VMs in an isolated network |

Never scan, brute-force, exploit, or enumerate systems merely because they are reachable. Authorization and scope come first. A tool's presence in Kali does not grant permission to use it against a target.

## 23. Safe lab workflow

Create a practice folder:
```bash
mkdir -p ~/kali-lab/{files,logs,output}
printf 'Failed login for demo user\\nSuccessful login for demo user\\n' > ~/kali-lab/logs/auth-demo.log
```

Inspect it:
```bash
pwd
find ~/kali-lab -maxdepth 3 -type f
file ~/kali-lab/logs/auth-demo.log
grep -in 'failed' ~/kali-lab/logs/auth-demo.log
sha256sum ~/kali-lab/logs/auth-demo.log
```

Save a command report:
```bash
{
  printf 'Date: '; date
  printf 'User: '; whoami
  printf 'Host: '; hostname
  printf '\\nDisk space:\\n'
  df -h "$HOME"
} > ~/kali-lab/output/system-report.txt
```

This lab teaches navigation, file creation, search, hashing, and redirection without changing system configuration.

## 24. Troubleshooting commands

| Problem | Try | What it checks |
|---|---|---|
| Command not found | `command -v name` | Whether the shell can locate it |
| Permission denied | `ls -l path`, `namei -l path` | File and parent-directory permissions |
| Disk full | `df -h`, `du -sh folder` | File-system space and directory usage |
| Cannot resolve hostname | `getent hosts example.com`, `resolvectl status` | Name resolution |
| No network route | `ip addr`, `ip route` | Interface and route configuration |
| Service not working | `systemctl status SERVICE`, `journalctl -u SERVICE -n 50` | Service state and recent logs |
| Process using a port | `ss -tuln` | Listening sockets |
| File type unclear | `file path`, `stat path` | Type clues and metadata |
| Need help | `man command`, `command --help` | Documentation |

Do not automatically use `sudo` whenever an error appears. First understand why permission is denied and whether elevated access is actually necessary.

## 25. Common mistakes beginners make

1. Confusing `/` (root directory) with `/root` (root user's home).
2. Assuming every Linux executable ends with `.exe` or any extension.
3. Forgetting quotes around paths containing spaces.
4. Using `>` when they meant `>>`, overwriting a file by mistake.
5. Running `rm -rf` without checking the exact path.
6. Treating `chmod 777` as a universal permissions fix.
7. Assuming `ping` failure means the target is offline.
8. Assuming a file hash proves that a file is safe.
9. Running copied shell scripts without reading them.
10. Using `sudo` for commands that do not need it.
11. Confusing `apt update` with upgrading installed packages.
12. Assuming every system has `/var/log/auth.log`; logs vary by configuration.
13. Assuming every interface is called eth0 or every disk is /dev/sda.
14. Uploading logs, private keys, password hashes, tokens, or sensitive screenshots to GitHub.
15. Scanning targets without permission or ignoring the defined scope.

## 26. Practice labs

### Lab 1 — Navigate and explore
Goal: understand directories and paths.

```bash
pwd
ls -la
cd /etc
pwd
cd ~
mkdir -p ~/kali-lab/navigation
touch ~/kali-lab/navigation/test.txt
find ~/kali-lab/navigation -maxdepth 2 -type f
```

Questions:
- What is your home directory?
- What is the difference between `ls` and `ls -la`?
- What is the absolute path of test.txt?

### Lab 2 — Permissions
Goal: understand read/write/execute.

```bash
printf 'Permission practice\\n' > ~/kali-lab/permissions.txt
ls -l ~/kali-lab/permissions.txt
chmod 600 ~/kali-lab/permissions.txt
stat ~/kali-lab/permissions.txt
chmod 640 ~/kali-lab/permissions.txt
```

Explain what changed and why a file can be inaccessible even if its own permissions seem correct.

### Lab 3 — Search a log
Goal: search, count, and preserve output.

```bash
grep -in 'failed' ~/kali-lab/logs/auth-demo.log
grep -ic 'failed' ~/kali-lab/logs/auth-demo.log
grep -in 'failed' ~/kali-lab/logs/auth-demo.log > ~/kali-lab/output/failed-lines.txt
cat ~/kali-lab/output/failed-lines.txt
```

Explain the difference between matching lines and counting matches.

### Lab 4 — File metadata and hashing
Goal: inspect a file without executing it.

```bash
file ~/kali-lab/logs/auth-demo.log
stat ~/kali-lab/logs/auth-demo.log
sha256sum ~/kali-lab/logs/auth-demo.log
cp ~/kali-lab/logs/auth-demo.log ~/kali-lab/logs/auth-demo-copy.log
sha256sum ~/kali-lab/logs/auth-demo-copy.log
```

Question: why do identical copies normally have the same SHA-256 hash?

### Lab 5 — System and network overview
Goal: gather basic diagnostics.

```bash
whoami
hostname
uname -a
uptime
free -h
df -h
ip addr
ip route
ss -tuln
```

Write a short report with date, hostname, available disk space, interfaces, and listening ports. Do not include private IP or host details in a public report unless you intend to share them.

### Lab 6 — SOC mini-investigation
Goal: investigate a harmless simulated event.

1. Use the demo log created in Lab 1/3.
2. Search for failed events using grep.
3. Count matches using wc -l or grep -c.
4. Record the file metadata using stat.
5. Calculate SHA-256.
6. Write a short note: what was found, what it does not prove, and what additional logs would be needed.

Never manufacture a conclusion beyond the evidence.

## 27. Interview questions

**Q1. What is a shell?**  
A shell reads commands and asks the operating system to run them. Bash is a common Linux shell.

**Q2. What is the difference between an absolute and relative path?**  
An absolute path starts from the root, such as /etc/hosts. A relative path is interpreted from the current directory.

**Q3. What does `ls -la` show?**  
A detailed listing that includes hidden names, with permissions, owners, sizes, and timestamps.

**Q4. What is the difference between `cp` and `mv`?**  
cp copies data to another path; mv moves or renames a path.

**Q5. What is grep used for?**  
It searches text for lines matching a pattern.

**Q6. What is the difference between `>` and `>>`?**  
`>` overwrites/creates the output file; `>>` appends to it.

**Q7. What does chmod 640 mean?**  
Owner can read/write, group can read, and others have no basic mode-bit permissions.

**Q8. What is a PID?**  
A process identifier assigned to a running process.

**Q9. What is the difference between df and du?**  
df reports file-system space; du estimates space used by files/directories.

**Q10. What is the purpose of ip addr and ip route?**  
ip addr shows interface addresses; ip route shows routing information.

**Q11. What does ss -tuln show?**  
Listening TCP/UDP sockets with numeric addresses and ports.

**Q12. What does apt update do?**  
It refreshes package metadata; it does not itself upgrade installed packages.

**Q13. What is journalctl?**  
A command for viewing the systemd journal, when the system uses it.

**Q14. Why should a SOC analyst calculate a file hash?**  
To compare exact file content with another copy or trusted reference. A hash does not by itself determine whether a file is malicious.

**Q15. Why should you avoid running suspicious files?**  
Execution can alter the system, destroy evidence, or trigger malicious behavior.

**Q16. Why is sudo powerful?**  
It can run commands with elevated privileges, so a mistake may affect the entire system.

**Q17. What is a symbolic link?**  
A file-system object that points to another path.

**Q18. Why is chmod 777 risky?**  
It grants read, write, and execute permissions to everyone under the basic mode-bit model.

## 28. Quick command cheat sheet

```bash
# Identity and location
whoami
id
pwd
hostname

# List and navigate
ls -lah
cd /path
cd ..
cd ~

# Create and inspect
mkdir -p ~/lab
touch ~/lab/file.txt
cat ~/lab/file.txt
less /path/to/large-file
file /path/to/file
stat /path/to/file

# Copy/move/delete — verify paths first
cp source destination
mv source destination
rm -i test-file

# Search
find ~/lab -type f
grep -in 'word' file.txt
command -v nmap

# Permissions
ls -l file
chmod 640 file
getfacl file

# Processes
ps aux
top
pgrep process-name
ss -tuln

# System and storage
uname -a
uptime
free -h
df -h
du -sh ~/lab
lsblk -f
findmnt

# Network
ip addr
ip route
ping -c 4 example.com
getent hosts example.com
curl -I https://example.com

# Logs
journalctl -n 100
journalctl --since today
tail -f /path/to/log

# Hash and package
sha256sum file
apt search package-name
apt show package-name
```

## 29. Official references

- Kali Linux documentation: https://www.kali.org/docs/
- Debian Reference: https://www.debian.org/doc/manuals/debian-reference/
- Linux man-pages: https://man7.org/linux/man-pages/
- GNU Coreutils manual: https://www.gnu.org/software/coreutils/manual/
- GNU Bash manual: https://www.gnu.org/software/bash/manual/
- systemd journalctl manual: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
- Nmap reference guide: https://nmap.org/book/man.html
- OpenSSH manual pages: https://www.openssh.com/manual.html

## Final learning roadmap

**Beginner:** terminal help → navigation → files/folders → paths → permissions.

**Intermediate:** find/grep → users/groups → processes → storage → packages → networking → logs.

**Cybersecurity/SOC:** hashes → SSH → service logs → process/socket inspection → evidence handling → safe lab reports.

**Advanced:** Bash scripting → service troubleshooting → packet analysis → authorized security testing → automation and documentation.

**Remember:** Understand the command, inspect the target path, use least privilege, preserve evidence, and practice in your own lab before making system-wide changes.
