#!/bin/bash
# No GPU in the cloud, so start Cinnamon's software rendering session
export LIBGL_ALWAYS_SOFTWARE=1
exec dbus-launch --exit-with-session cinnamon-session --session cinnamon2d
