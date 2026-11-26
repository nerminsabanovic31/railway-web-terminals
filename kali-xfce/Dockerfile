# Kali Linux with the XFCE desktop (Kali's own default desktop), streamed to the browser by
# linuxserver's Selkies. Built on linuxserver's Kali Selkies base like their kali-linux image,
# but with XFCE instead of KDE Plasma so it stays well under 1 GB of memory when idle.
FROM ghcr.io/linuxserver/baseimage-selkies:kali

LABEL org.opencontainers.image.source="https://github.com/nerminsabanovic31/railway-web-terminals"

ENV TITLE="Kali Linux XFCE"

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       xfce4-session xfwm4 xfdesktop4 xfce4-panel xfce4-settings xfconf xfce4-appfinder \
       xfce4-terminal xfce4-notifyd xfce4-taskmanager xfce4-screenshooter libxfce4ui-utils \
       thunar thunar-archive-plugin tumbler gvfs mousepad ristretto xarchiver \
       kali-themes kali-desktop-base kali-menu kali-tools-top10 \
       firefox-esr dbus-x11 xdg-user-dirs zip unzip 7zip \
  && rm -f /etc/xdg/autostart/xscreensaver.desktop /etc/xdg/autostart/light-locker.desktop \
       /etc/xdg/autostart/xfce4-power-manager.desktop \
  && apt-get autoclean \
  && rm -rf /config/.cache /var/lib/apt/lists/* /var/tmp/* /tmp/*

COPY root/ /
RUN chmod +x /defaults/startwm.sh

EXPOSE 3000
