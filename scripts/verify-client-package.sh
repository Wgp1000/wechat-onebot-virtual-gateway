#!/bin/sh
set -eu

package_path="${WECHAT_PACKAGE_PATH:-}"
expected_sha256="${WECHAT_PACKAGE_SHA256:-}"

if [ -z "$package_path" ] || [ -z "$expected_sha256" ]; then
  echo "client package is not configured" >&2
  exit 2
fi
case "$package_path" in
  /installers/*.deb) ;;
  *) echo "package must be a mounted /installers/*.deb path" >&2; exit 2 ;;
esac
if [ ! -f "$package_path" ]; then
  echo "package file not found: $package_path" >&2
  exit 2
fi
actual_sha256="$(sha256sum "$package_path" | awk '{print $1}')"
if [ "$actual_sha256" != "$expected_sha256" ]; then
  echo "package SHA-256 mismatch" >&2
  exit 3
fi
printf 'package verified: %s\n' "$package_path"
