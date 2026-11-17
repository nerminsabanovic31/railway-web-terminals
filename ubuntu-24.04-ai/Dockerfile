FROM ubuntu:24.04

ENV TERMINAL_TITLE="Ubuntu 24.04 LTS AI Coding Box"
ENV ENABLE_SSH=1
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends bash sudo tmux openssh-server xz-utils curl wget git vim nano htop less unzip ca-certificates tzdata python3 python3-pip openssh-client procps iputils-ping dnsutils build-essential && rm -rf /var/lib/apt/lists/* && userdel -r ubuntu 2>/dev/null || true
RUN curl -fsSL -o /tmp/node.tar.xz https://nodejs.org/dist/v24.22.3/node-v24.22.3-linux-x64.tar.xz \
 && echo "4f2b175a6d53a5c617a80dba2676238a0688cef28c6da4eba35c7d844e66fcfb  /tmp/node.tar.xz" | sha256sum -c - \
 && tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1 && rm /tmp/node.tar.xz \
 && npm install -g @anthropic-ai/claude-code @openai/codex @google/gemini-cli opencode-ai && npm cache clean --force
RUN curl -fsSL -o /usr/local/bin/ttyd https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 \
 && echo "8a217c968aba172e0dbf3f34447218dc015bc4d5e59bf51db2f2cd12b7be4f55  /usr/local/bin/ttyd" | sha256sum -c - \
 && chmod +x /usr/local/bin/ttyd

COPY motd /etc/motd
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 7681 22
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
