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
| `ubuntu-24.04-ssh` | ubuntu:24.04, plus an SSH server |
| `ubuntu-26.04-ssh` | ubuntu:26.04, plus an SSH server |
| `debian-13-ssh` | debian:trixie, plus an SSH server |
| `kali-ssh` | kalilinux/kali-rolling, plus an SSH server |
| `ubuntu-24.04-ai` | ubuntu:24.04, SSH, Node.js 24, Claude Code, Codex CLI and Gemini CLI |
| `debian-13-ai` | debian:trixie, SSH, Node.js 24, Claude Code, Codex CLI and Gemini CLI |

Every image runs [ttyd](https://github.com/tsl0922/ttyd) with HTTP basic auth and a persistent `tmux` session. The login user has passwordless sudo and its home folder lives on a Railway volume at `/data`, so files survive restarts and redeploys.

The `-ssh` and `-ai` images also run OpenSSH on port 22 for a Railway TCP proxy. SSH uses the same `USERNAME` and `PASSWORD` (or keys from `AUTHORIZED_KEYS`), root login is disabled, and host keys are stored in `/data/ssh` so they stay the same across redeploys. Run `tmux attach -t main` over SSH to join the browser session.

## Variables

| Variable | Required | What it does |
| --- | --- | --- |
| `USERNAME` | yes | Login name for the terminal (also the Linux user) |
| `PASSWORD` | yes | Login password |
| `PORT` | yes | Web port, `7681` |
| `TZ` | no | Time zone, for example `Europe/Berlin` |
| `AUTHORIZED_KEYS` | no | SSH images: public keys, one per line |
| `SSH_PASSWORD_LOGIN` | no | SSH images: set to `no` to allow key login only |

## Layout

- `entrypoint.sh`: shared start script (copied into every folder by `gen.py`)
- `gen.py`: writes each folder's `Dockerfile`, `entrypoint.sh` and `motd`

## License

MIT
