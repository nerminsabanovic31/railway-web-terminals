#!/bin/bash
# No GPU in the cloud, so start Cinnamon's software rendering session on the Selkies X server
export LIBGL_ALWAYS_SOFTWARE=1
export XDG_SESSION_TYPE=x11
export XDG_SESSION_DESKTOP=cinnamon
export DESKTOP_SESSION=cinnamon
export XDG_CURRENT_DESKTOP=X-Cinnamon
exec dbus-launch --exit-with-session cinnamon-session --session cinnamon2d
