#!/bin/sh
# Compatibility wrapper: configuration is supplied through the environment.
# No credential prompt or configuration file generation is required.
set -eu
exec "$@"
