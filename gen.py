"""Generates one folder per distro (Dockerfile, entrypoint, motd) for the Railway web terminal templates."""
import os, shutil

TTYD = "https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64"
TTYD_SHA = "8a217c968aba172e0dbf3f34447218dc015bc4d5e59bf51db2f2cd12b7be4f55"
COMMON = "bash sudo tmux curl wget git vim nano htop less unzip ca-certificates tzdata"

DISTROS = {
    "ubuntu-22.04": ("ubuntu:22.04", "Ubuntu 22.04 LTS", "apt",
                     f"apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends {COMMON} python3 python3-pip openssh-client procps iputils-ping dnsutils build-essential && rm -rf /var/lib/apt/lists/*"),
    "ubuntu-24.04": ("ubuntu:24.04", "Ubuntu 24.04 LTS", "apt",
                     f"apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends {COMMON} python3 python3-pip openssh-client procps iputils-ping dnsutils build-essential && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null || true"),
    "ubuntu-26.04": ("ubuntu:26.04", "Ubuntu 26.04 LTS", "apt",
                     f"apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends {COMMON} python3 python3-pip openssh-client procps iputils-ping dnsutils build-essential && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null || true"),
    "debian-13": ("debian:trixie", "Debian 13 (trixie)", "apt",
                  f"apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends {COMMON} python3 python3-pip openssh-client procps iputils-ping dnsutils build-essential && rm -rf /var/lib/apt/lists/*"),
    "kali": ("kalilinux/kali-rolling:latest", "Kali Linux (rolling)", "apt",
             f"apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends {COMMON} python3 python3-pip openssh-client procps iputils-ping dnsutils nmap whois netcat-traditional && rm -rf /var/lib/apt/lists/*"),
    "alpine": ("alpine:3.22", "Alpine Linux 3.22", "apk",
               f"apk add --no-cache {COMMON} shadow python3 py3-pip openssh-client procps iputils bind-tools build-base"),
    "fedora": ("fedora:43", "Fedora 43", "dnf",
               f"dnf install -y {COMMON.replace('ca-certificates ', '')} python3 python3-pip openssh-clients procps-ng iputils bind-utils gcc make && dnf clean all"),
    "arch": ("archlinux:latest", "Arch Linux (rolling)", "pacman",
             f"pacman -Syu --noconfirm {COMMON.replace('ca-certificates ', '')} python python-pip openssh procps-ng iputils bind base-devel && pacman -Scc --noconfirm"),
    "rocky-9": ("rockylinux:9", "Rocky Linux 9", "dnf",
                f"dnf install -y --allowerasing {COMMON.replace('ca-certificates ', '').replace('htop ', '')} python3 python3-pip openssh-clients procps-ng iputils bind-utils gcc make && dnf clean all"),
    "almalinux-10": ("almalinux:10", "AlmaLinux 10", "dnf",
                     f"dnf install -y --allowerasing {COMMON.replace('ca-certificates ', '').replace('htop ', '')} python3 python3-pip openssh-clients procps-ng iputils bind-utils gcc make && dnf clean all"),
    "opensuse": ("opensuse/tumbleweed:latest", "openSUSE Tumbleweed", "zypper",
                 f"zypper --non-interactive install {COMMON.replace('tzdata', 'timezone')} python3 python3-pip openssh-clients procps iputils bind-utils gcc make shadow && zypper clean -a"),
}

# SSH variants add sshd (reached through a Railway TCP proxy); AI variants also add Node.js and coding agent CLIs
VARIANTS = {
    "ubuntu-24.04-ssh": ("ubuntu-24.04", False),
    "ubuntu-26.04-ssh": ("ubuntu-26.04", False),
    "debian-13-ssh": ("debian-13", False),
    "kali-ssh": ("kali", False),
    "ubuntu-22.04-ssh": ("ubuntu-22.04", False),
    "fedora-ssh": ("fedora", False),
    "arch-ssh": ("arch", False),
    "alpine-ssh": ("alpine", False),
    "rocky-9-ssh": ("rocky-9", False),
    "almalinux-10-ssh": ("almalinux-10", False),
    "opensuse-ssh": ("opensuse", False),
    "ubuntu-24.04-ai": ("ubuntu-24.04", True),
    "debian-13-ai": ("debian-13", True),
}
NODE = "https://nodejs.org/dist/v24.22.3/node-v24.22.3-linux-x64.tar.xz"
NODE_SHA = "4f2b175a6d53a5c617a80dba2676238a0688cef28c6da4eba35c7d844e66fcfb"
SSH_PKGS = {"apt": "openssh-server xz-utils", "apk": "openssh-server", "dnf": "openssh-server",
            "pacman": "openssh", "zypper": "openssh-server"}
AI_CLIS = "@anthropic-ai/claude-code @openai/codex @google/gemini-cli"

HINT = {"apt": "sudo apt update && sudo apt install -y <package>", "apk": "sudo apk add <package>",
        "dnf": "sudo dnf install -y <package>", "pacman": "sudo pacman -S <package>",
        "zypper": "sudo zypper install <package>"}


def build(key):
    base, ai = VARIANTS.get(key, (key, None))
    image, label, pm, install = DISTROS[base]
    ssh = ai is not None
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), key)
    os.makedirs(d, exist_ok=True)
    shutil.copy("entrypoint.sh", os.path.join(d, "entrypoint.sh"))
    with open(os.path.join(d, "motd"), "w") as f:
        f.write(f"\n  {label} web terminal\n"
                f"  Install software:  {HINT[pm]}\n"
                "  Your files in this home folder survive restarts and redeploys.\n"
                "  tmux keeps your session alive: close the tab and come back any time.\n"
                + ("  Over SSH, run  tmux attach -t main  to join the browser session.\n" if ssh else "")
                + ("  Coding agents:  claude  |  codex  |  gemini   (sign in with your own account)\n" if ai else "")
                + "\n")
    if ssh:
        install = install.replace(" tmux ", f" tmux {SSH_PKGS[pm]} ", 1)
        label += " + SSH"
    extra = ""
    if ai:
        label = label.replace(" + SSH", " AI Coding Box")
        extra = (f"RUN curl -fsSL -o /tmp/node.tar.xz {NODE} \\\n"
                 f" && echo \"{NODE_SHA}  /tmp/node.tar.xz\" | sha256sum -c - \\\n"
                 " && tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1 && rm /tmp/node.tar.xz \\\n"
                 f" && npm install -g {AI_CLIS} && npm cache clean --force\n")
    with open(os.path.join(d, "Dockerfile"), "w") as f:
        f.write(f"""FROM {image}

ENV TERMINAL_TITLE="{label}"{chr(10) + "ENV ENABLE_SSH=1" if ssh else ""}
RUN {install}
{extra}RUN curl -fsSL -o /usr/local/bin/ttyd {TTYD} \\
 && echo "{TTYD_SHA}  /usr/local/bin/ttyd" | sha256sum -c - \\
 && chmod +x /usr/local/bin/ttyd

COPY motd /etc/motd
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 7681{" 22" if ssh else ""}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
""")


if __name__ == "__main__":
    for k in [*DISTROS, *VARIANTS]:
        build(k)
    print(" ".join([*DISTROS, *VARIANTS]))
