"""Generates one folder per distro (Dockerfile, entrypoint, motd) for the Railway web terminal templates."""
import os, shutil

TTYD = "https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64"
TTYD_SHA = "8a217c968aba172e0dbf3f34447218dc015bc4d5e59bf51db2f2cd12b7be4f55"
COMMON = "bash sudo tmux curl wget git vim nano htop less unzip ca-certificates tzdata"

DISTROS = {
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

HINT = {"apt": "sudo apt update && sudo apt install -y <package>", "apk": "sudo apk add <package>",
        "dnf": "sudo dnf install -y <package>", "pacman": "sudo pacman -S <package>",
        "zypper": "sudo zypper install <package>"}


def build(key):
    image, label, pm, install = DISTROS[key]
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), key)
    os.makedirs(d, exist_ok=True)
    shutil.copy("entrypoint.sh", os.path.join(d, "entrypoint.sh"))
    with open(os.path.join(d, "motd"), "w") as f:
        f.write(f"\n  {label} web terminal\n"
                f"  Install software:  {HINT[pm]}\n"
                "  Your files in this home folder survive restarts and redeploys.\n"
                "  tmux keeps your session alive: close the tab and come back any time.\n\n")
    with open(os.path.join(d, "Dockerfile"), "w") as f:
        f.write(f"""FROM {image}

ENV TERMINAL_TITLE="{label}"
RUN {install}
RUN curl -fsSL -o /usr/local/bin/ttyd {TTYD} \\
 && echo "{TTYD_SHA}  /usr/local/bin/ttyd" | sha256sum -c - \\
 && chmod +x /usr/local/bin/ttyd

COPY motd /etc/motd
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 7681
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
""")


if __name__ == "__main__":
    for k in DISTROS:
        build(k)
    print(" ".join(DISTROS))
