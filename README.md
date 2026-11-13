# Railway Web Terminals

Password-protected Linux terminals that run on Railway and open in any browser. Each folder is one distro:

| Folder | Base image |
| --- | --- |
| `ubuntu-24.04` | ubuntu:24.04 |
| `ubuntu-26.04` | ubuntu:26.04 |
| `debian-13` | debian:trixie |
| `kali` | kalilinux/kali-rolling |
| `alpine` | alpine:3.22 |
| `fedora` | fedora:43 |
| `arch` | archlinux |
| `rocky-9` | rockylinux:9 |
| `almalinux-10` | almalinux:10 |
| `opensuse` | opensuse/tumbleweed |

Every image runs [ttyd](https://github.com/tsl0922/ttyd) with HTTP basic auth and a persistent `tmux` session. The login user has passwordless sudo and its home folder lives on a Railway volume at `/data`, so files survive restarts and redeploys.

## Variables

| Variable | Required | What it does |
| --- | --- | --- |
| `USERNAME` | yes | Login name for the terminal (also the Linux user) |
| `PASSWORD` | yes | Login password |
| `PORT` | yes | Web port, `7681` |
| `TZ` | no | Time zone, for example `Europe/Berlin` |

## Layout

- `entrypoint.sh`: shared start script (copied into every folder by `gen.py`)
- `gen.py`: writes each folder's `Dockerfile`, `entrypoint.sh` and `motd`

## License

MIT
