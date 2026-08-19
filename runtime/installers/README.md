# WeChat Linux Client Installer

This directory is intentionally empty in the public source repository.

Download the official Tencent WeChat Linux x86_64 `.deb` package yourself and
place it here with this exact name before building:

```text
WeChatLinux_x86_64.deb
```

The Dockerfile verifies the package SHA-256 currently expected by this release.
If Tencent publishes a newer package, update the checksum in
`images/virtual-desktop/Dockerfile` after verifying the official download.
