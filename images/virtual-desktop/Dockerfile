FROM docker.1ms.run/debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99 \
    VNC_PORT=5900 \
    NOVNC_PORT=6080 \
    QT_ACCESSIBILITY=1

RUN sed -i 's|http://deb.debian.org/debian|http://mirrors.tuna.tsinghua.edu.cn/debian|g; s|http://security.debian.org/debian-security|http://mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        imagemagick \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatomic1 \
        libgbm1 \
        libnspr4 \
        libnss3 \
        libpulse0 \
        libxcomposite1 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 \
        libxkbcommon0 \
        at-spi2-core \
        dbus-x11 \
        openbox \
        python3 \
        python3-pyatspi \
        python3-tk \
        supervisor \
        tesseract-ocr \
        tesseract-ocr-chi-sim \
        tigervnc-standalone-server \
        websockify \
        novnc \
        xvfb \
        x11-apps \
        x11-utils \
        x11-xserver-utils \
        xclip \
        xdotool \
        x11vnc \
    && rm -rf /var/lib/apt/lists/*

COPY runtime/installers/WeChatLinux_x86_64.deb /tmp/WeChatLinux_x86_64.deb
RUN echo 'c9765e87ee5133bf4bb50d585c1814fafd995e3fb0da62c5ed07259b43dada7b  /tmp/WeChatLinux_x86_64.deb' | sha256sum -c - \
    && apt-get update \
    && apt-get install -y --no-install-recommends /tmp/WeChatLinux_x86_64.deb \
    && rm -f /tmp/WeChatLinux_x86_64.deb \
    && rm -rf /var/lib/apt/lists/*
COPY images/virtual-desktop/start.sh /usr/local/bin/start-virtual-desktop
COPY images/virtual-desktop/dashboard.py /usr/local/bin/dashboard.py
COPY images/virtual-desktop/ui_probe.py /usr/local/bin/ui_probe.py
COPY images/virtual-desktop/x11_probe.py /usr/local/bin/x11_probe.py
COPY ui_worker /usr/local/lib/ui_worker
COPY gateway /usr/local/lib/gateway
RUN chmod 0755 /usr/local/bin/start-virtual-desktop

EXPOSE 6080 8088
ENTRYPOINT ["/usr/local/bin/start-virtual-desktop"]
