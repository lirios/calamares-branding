#!/bin/sh
xhost +
exec sudo -E /usr/bin/calamares --platform xcb
