FROM archlinux:latest

ENV TERMINAL_TITLE="Arch Linux (rolling)"
RUN pacman -Syu --noconfirm bash sudo tmux curl wget git vim nano htop less unzip tzdata python python-pip openssh procps-ng iputils bind base-devel && pacman -Scc --noconfirm
RUN curl -fsSL -o /usr/local/bin/ttyd https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 \
 && echo "8a217c968aba172e0dbf3f34447218dc015bc4d5e59bf51db2f2cd12b7be4f55  /usr/local/bin/ttyd" | sha256sum -c - \
 && chmod +x /usr/local/bin/ttyd

COPY motd /etc/motd
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 7681
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
