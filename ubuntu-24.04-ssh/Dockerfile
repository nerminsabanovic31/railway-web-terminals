FROM ubuntu:24.04

ENV TERMINAL_TITLE="Ubuntu 24.04 LTS + SSH"
ENV ENABLE_SSH=1
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends bash sudo tmux curl wget git vim nano htop less unzip ca-certificates tzdata openssh-server xz-utils python3 python3-pip openssh-client procps iputils-ping dnsutils build-essential && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null || true
RUN curl -fsSL -o /usr/local/bin/ttyd https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 \
 && echo "8a217c968aba172e0dbf3f34447218dc015bc4d5e59bf51db2f2cd12b7be4f55  /usr/local/bin/ttyd" | sha256sum -c - \
 && chmod +x /usr/local/bin/ttyd

COPY motd /etc/motd
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 7681 22
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
