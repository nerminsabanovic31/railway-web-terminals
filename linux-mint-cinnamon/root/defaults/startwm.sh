#!/bin/bash
# No GPU in the cloud, so start Cinnamon's software rendering session
exec dbus-launch --exit-with-session cinnamon-session --session cinnamon2d > /dev/null 2>&1
