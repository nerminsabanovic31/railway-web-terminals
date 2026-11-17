#!/bin/sh
# Starts a password-protected browser terminal (ttyd + tmux) with a persistent home on /data.
set -eu

if [ -z "${PASSWORD:-}" ]; then
  echo "PASSWORD is not set. Add it in Railway → Variables and redeploy." >&2
  exit 1
fi
USERNAME="${USERNAME:-admin}"
PORT="${PORT:-7681}"
HOME_DIR="/data/home"

# Create the login user once; the home folder lives on the volume
if ! id "$USERNAME" >/dev/null 2>&1; then
  if command -v useradd >/dev/null 2>&1; then
    useradd -M -d "$HOME_DIR" -s /bin/bash "$USERNAME"
  else
    adduser -D -H -h "$HOME_DIR" -s /bin/bash "$USERNAME"
  fi
fi
echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/terminal
chmod 440 /etc/sudoers.d/terminal

mkdir -p "$HOME_DIR"
if [ ! -f "$HOME_DIR/.bashrc" ]; then
  cp -a /etc/skel/. "$HOME_DIR/" 2>/dev/null || true
  cat >> "$HOME_DIR/.bashrc" <<'RC'

# Web terminal
export PS1='\[\e[1;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ '
[ -z "${TERMINAL_QUIET:-}" ] && [ -f /etc/motd ] && cat /etc/motd
RC
  echo 'set -g mouse on' > "$HOME_DIR/.tmux.conf"
fi
chown -R "$USERNAME" "$HOME_DIR" 2>/dev/null || true

[ -n "${TZ:-}" ] && [ -f "/usr/share/zoneinfo/$TZ" ] && ln -sf "/usr/share/zoneinfo/$TZ" /etc/localtime

# SSH images only: sshd on port 22 (Railway TCP proxy), same user and password, host keys kept on the volume
if [ -n "${ENABLE_SSH:-}" ] && [ -x /usr/sbin/sshd ]; then
  mkdir -p /data/ssh /run/sshd
  for t in rsa ecdsa ed25519; do
    [ -f "/data/ssh/ssh_host_${t}_key" ] || ssh-keygen -q -t "$t" -N '' -f "/data/ssh/ssh_host_${t}_key"
  done
  echo "$USERNAME:$PASSWORD" | chpasswd
  mkdir -p "$HOME_DIR/.ssh"
  if [ -n "${AUTHORIZED_KEYS:-}" ]; then
    printf '%s\n' "$AUTHORIZED_KEYS" > "$HOME_DIR/.ssh/authorized_keys"
  fi
  chmod 700 "$HOME_DIR/.ssh"
  [ -f "$HOME_DIR/.ssh/authorized_keys" ] && chmod 600 "$HOME_DIR/.ssh/authorized_keys"
  chown -R "$USERNAME" "$HOME_DIR/.ssh"
  # Standalone config so every distro behaves the same, whatever its default sshd_config looks like
  cat > /etc/ssh/railway_sshd_config <<CONF
Port 22
HostKey /data/ssh/ssh_host_ed25519_key
HostKey /data/ssh/ssh_host_ecdsa_key
HostKey /data/ssh/ssh_host_rsa_key
PermitRootLogin no
PasswordAuthentication ${SSH_PASSWORD_LOGIN:-yes}
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AllowUsers $USERNAME
Subsystem sftp internal-sftp
CONF
  /usr/sbin/sshd -e -f /etc/ssh/railway_sshd_config
fi

exec ttyd --writable --port "$PORT" \
  --credential "$USERNAME:$PASSWORD" \
  --client-option fontSize=15 \
  --client-option titleFixed="${TERMINAL_TITLE:-Web Terminal}" \
  sudo -u "$USERNAME" -i env HOME="$HOME_DIR" TMUX_TMPDIR=/tmp tmux new-session -A -s main
