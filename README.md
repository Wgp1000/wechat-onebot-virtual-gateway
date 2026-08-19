# WeChat Virtual Gateway / 微信虚拟网关

一个面向中文用户的 Docker 优先 **OneBot V11 微信网关**：在私有 X11 虚拟桌面中运行官方微信 Linux 客户端，并通过管理面板配置正向/反向 WebSocket。

A Docker-first **OneBot V11 gateway for WeChat**, running the official WeChat Linux client inside a private X11 virtual desktop with a browser management panel for forward/reverse WebSocket configuration.

> **当前状态 / Current status**：私聊出站已经过验证；私聊入站仍为实验性功能，默认关闭；群聊和原生 `@` 暂不支持。
>
> Private outbound messaging is verified. Private inbound is experimental and disabled by default. Group inbound and native `@` mentions are not supported.

## 测试与反馈 / Testing and Feedback

本项目目前只经过以下方式测试：

- 人工扫码登录与人工界面验证；
- 本机 Shell 编写的 OneBot V11 WebSocket 客户端；
- 本地 Docker、Gateway、Worker 和面板单元测试。

目前**没有接入任何第三方机器人平台进行兼容性测试**，原因是项目仍处于早期公开测试阶段，维护和测试人员有限。

This project has currently been tested only with manual QR login/UI verification, a local Shell-based OneBot V11 WebSocket client, and local Docker/Gateway/Worker/panel tests. It has **not yet been compatibility-tested with third-party bot platforms** because the project is in an early public-testing stage with limited maintainers and testers.

### 测试与反馈群 / Test and Feedback Group

```text
744528507
```

欢迎加入测试群反馈问题。反馈时请尽量提供：

- 项目版本或 Git commit；
- Linux 发行版和 Docker 版本；
- 使用反向 WS 还是正向 WS；
- 调用的 OneBot Action 或收到的事件结构；
- 脱敏后的面板/Gateway 日志。

请勿在群里发送：二维码、访问 token、微信 profile、聊天截图、聊天记录或任何账号隐私数据。

Please include the project version/commit, Linux distribution, Docker version, WebSocket direction, OneBot action/event shape, and sanitized logs. Never share QR codes, access tokens, WeChat profiles, chat screenshots, chat history, or account secrets.

## 当前能力矩阵 / Capability Matrix

| 能力 / Capability | 状态 / Status | 说明 / Notes |
|---|---|---|
| Docker 中官方微信扫码登录 / Official WeChat QR login in Docker | 已验证 / Verified | 使用官方 Linux 客户端 / Uses the official Linux client. |
| 单一管理面板 / Management panel | 已验证 / Verified | 登录状态、联系人映射、协议配置、脱敏日志 / Login status, mappings, protocol config and sanitized logs. |
| OneBot V11 反向 WS / Reverse WebSocket | 已验证 / Verified | 已用本机 Shell 客户端测试 / Tested with a local Shell client. |
| OneBot V11 正向 WS / Forward WebSocket | 已实现 / Implemented | 支持配置热加载；第三方兼容性待测试 / Hot reload is implemented; third-party compatibility is untested. |
| `get_friend_list` | 已验证 / Verified | 返回已批准的本地联系人映射 / Returns approved local mappings. |
| `send_private_msg` | 已验证 / Verified | 可通过确定性微信 UI 发送文本 / Sends text through the deterministic WeChat UI flow. |
| 私聊文本入站 / Private text inbound | 实验性、默认关闭 / Experimental, disabled | 等待会话身份和正文复制链路进一步验证 / Pending stronger identity and copy verification. |
| 群聊入站 / Group inbound | 暂不支持 / Not supported | 不会伪装成私聊事件 / Never emulated as private events. |
| 原生群聊 `@` / Native group mentions | 暂不支持 / Not supported | 不会把普通文字冒充原生提及 / Literal text is not claimed as a native mention. |
| 文件、图片、语音、贴纸、回复 / Media, files, voice, stickers, replies | 暂不支持 / Not supported | 当前范围为文本 / Current scope is text only. |

## 快速开始 / Quick Start

### 1. 准备官方微信安装包 / Obtain the official client package

从官方渠道下载 Tencent WeChat Linux x86_64 `.deb` 安装包，放到：

Download the official Tencent WeChat Linux x86_64 `.deb` package and place it at:

```text
runtime/installers/WeChatLinux_x86_64.deb
```

安装包出于版权和安全原因不会提交到仓库。请阅读 [`runtime/installers/README.md`](runtime/installers/README.md)。

The installer is intentionally not included in this repository for licensing and security reasons. See [`runtime/installers/README.md`](runtime/installers/README.md).

### 2. 启动 Docker / Start Docker

```bash
docker compose up -d --build
```

### 3. 打开管理面板 / Open the management panel

管理面板是正常使用所需的唯一界面：

The management panel is the only UI required for normal setup:

1. 在面板中扫描官方微信二维码；/ Scan the official WeChat QR code.
2. 在手机上确认登录；/ Confirm login on the phone.
3. 配置 OneBot 正向或反向 WS；/ Configure forward or reverse WS.
4. 配置已批准的联系人映射；/ Configure approved contact mappings.
5. 在面板查看脱敏运行日志；/ View sanitized runtime logs in the panel.

正常使用不需要进入 VNC。VNC、Dashboard 和 Gateway 默认只绑定本机或 Docker 内部网络，不应公开到互联网。

Normal operation does not require VNC. VNC, the dashboard and Gateway are bound to loopback or internal Docker networks by default and must not be publicly exposed.

## OneBot V11 使用方式 / OneBot V11 Usage

### 反向 WS / Reverse WebSocket

默认本机地址：

Default local endpoint:

```text
ws://127.0.0.1:16700
```

获取已批准联系人：

Get approved contacts:

```json
{"action":"get_friend_list","params":{}}
```

发送私聊文本：

Send private text:

```json
{
  "action": "send_private_msg",
  "params": {
    "user_id": 123456,
    "message": "你好 / Hello"
  }
}
```

`send_private_msg` 返回成功表示网关已经通过已验证的微信 UI 提交文本，不代表对方已读或平台级投递回执。

A successful `send_private_msg` response means the gateway submitted the text through the verified WeChat UI flow. It does not prove that the recipient read the message or that platform-level delivery was confirmed.

### 正向 WS / Forward WebSocket

可以在面板中填写正向 WS 地址并启用。配置保存在：

Configure and enable the forward WS URL in the panel. Configuration is stored in:

```text
runtime/gateway/protocol.json
```

正向 WS 配置支持热加载；反向 WS 监听地址或端口变化需要重启 Gateway。宿主机端口默认只发布到 `127.0.0.1`。

Forward WS changes hot-reload. Reverse WS address/port changes require a Gateway restart. Host ports are published to `127.0.0.1` by default.

### 能力状态 / Capability status

调用 `get_status` 可以查看当前明确能力边界：

Call `get_status` to inspect the explicit capability boundary:

```json
{
  "private_text_inbound": false,
  "private_text_inbound_experimental": true,
  "group_inbound": false,
  "native_mentions": false,
  "requires_unpinned_unfolded_inbox": true
}
```

## 私聊入站实验功能 / Experimental Private Inbound

私聊入站当前默认关闭。未来只有同时满足以下条件才会发布消息：

Private inbound is disabled by default. A message will only be published when all of the following evidence is available:

1. 已批准的私聊会话视觉身份；/ Approved private-conversation visual identity.
2. 两帧稳定的会话列表快照；/ Stable two-frame inbox snapshot.
3. 没有置顶或折叠会话；/ No pinned or folded conversations.
4. 已验证选中行和聊天标题；/ Verified selected row and chat header.
5. 聊天区没有被附属窗口遮挡；/ Unobscured message pane.
6. 成功复制一条完整的左侧入站文本气泡；/ Successfully copied one complete incoming text bubble.

使用实验入站功能时，请不要置顶会话，也不要折叠群聊/会话。遇到未知、重复标题、遮挡、群聊或 `@` 情况，系统会隔离而不是错误发布 OneBot 事件。

When experimenting with private inbound, do not pin conversations or fold conversation/group containers. Unknown, duplicate-title, occluded, group, or mention cases are quarantined instead of emitted as incorrect OneBot events.

## 隐私与安全 / Security and Privacy

- 不要把 `runtime/`、`evidence/`、面板 token、微信 profile、SQLite、日志或官方 `.deb` 提交到 Git；/ Never commit runtime state, evidence, tokens, profiles, SQLite databases, logs or the official `.deb`.
- 不要公开 VNC、Docker API、SSH、Dashboard 或 OneBot 端口；/ Do not expose VNC, Docker APIs, SSH, Dashboard or OneBot ports publicly.
- `.gitignore` 已配置用于防止登录资料、二维码和本地证据误提交；/ `.gitignore` is configured to prevent accidental publication of login/session data and evidence.
- 项目不使用私有微信协议模拟，也不解密本地微信数据库；/ The project does not emulate private WeChat protocols or decrypt local WeChat databases.
- 官方微信客户端仍受腾讯相关条款和许可约束；/ The official WeChat client remains subject to Tencent's terms and license.

## 开发测试 / Development Tests

```bash
python3 -m unittest discover -s gateway/tests -v
python3 -m unittest discover -s ui_worker/tests -v
python3 -m unittest discover -s panel/tests -v
```

当前公开版测试结果：

Current public-release test result:

```text
Gateway: 21 tests passed
UI Worker: 60 tests passed
Panel: 14 tests passed
```

## 开源协议 / License

本项目采用 **Apache License 2.0**。官方微信客户端不属于本项目，其使用仍受腾讯相关条款和许可约束。

This project is released under the **Apache License 2.0**. The official WeChat client is not part of this project and remains subject to Tencent's applicable terms and license.
