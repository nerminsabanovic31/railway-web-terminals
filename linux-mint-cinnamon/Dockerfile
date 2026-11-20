# Linux Mint 22.3 "Zena" with the Cinnamon desktop, streamed to the browser by linuxserver's Selkies.
# Mint 22 is built on Ubuntu 24.04, so this starts from linuxserver's noble Selkies base and adds
# Mint's own repository, artwork and Cinnamon on top, the way webtop builds its desktops.
FROM linuxmintd/mint22.3-amd64 AS mint

FROM ghcr.io/linuxserver/baseimage-selkies:ubuntunoble

LABEL org.opencontainers.image.source="https://github.com/nerminsabanovic31/railway-web-terminals"

ENV TITLE="Linux Mint Cinnamon"

# Mint's signing key and package pins, taken from the Mint team's official image
COPY --from=mint /etc/apt/trusted.gpg.d/linuxmint-keyring.gpg /etc/apt/trusted.gpg.d/
COPY --from=mint /etc/apt/preferences.d/official-package-repositories.pref /etc/apt/preferences.d/

RUN echo "deb http://packages.linuxmint.com zena main upstream import backport" \
      > /etc/apt/sources.list.d/linuxmint.list \
  && apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --allow-downgrades --no-install-recommends base-files/zena \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       cinnamon cinnamon-session cinnamon-control-center cinnamon-settings-daemon nemo nemo-fileroller \
       mint-common mint-info-cinnamon mint-artwork mint-themes mint-x-icons mint-y-icons mint-cursor-themes \
       fonts-ubuntu gnome-terminal xed xviewer xreader file-roller gvfs librsvg2-common \
       xdg-user-dirs dbus-x11 zip unzip firefox libgl1-mesa-dri mesa-utils \
  && grep -q '^NAME="Linux Mint"' /etc/os-release \
  && rm -f /etc/xdg/autostart/cinnamon-screensaver.desktop /etc/xdg/autostart/xscreensaver.desktop \
  && apt-get autoclean \
  && rm -rf /config/.cache /var/lib/apt/lists/* /var/tmp/* /tmp/*

COPY root/ /
RUN glib-compile-schemas /usr/share/glib-2.0/schemas && chmod +x /defaults/startwm.sh

EXPOSE 3000
