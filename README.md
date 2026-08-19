# WeChat Virtual Gateway

A Docker-first **OneBot V11 outbound gateway** built around the official WeChat
Linux client in a private X11 desktop. It uses deterministic X11 input,
clipboard operations and local state; it does not use a private WeChat protocol,
client database decryption, or an AI model at runtime.

> **Project status:** private-message outbound is implemented and verified.
> Inbound private-text work is experimental and disabled by default. Group
> inbound and native `@` mentions are not supported.

## Testing and feedback

This project has currently been tested only by manual verification and a local
Shell-based OneBot V11 WebSocket client. It has **not** yet been integrated or
compatibility-tested with third-party bot platforms because the project is
maintained by a small team.

Join the public test and feedback group:

```text
744528507
```

Please include the following when reporting an issue:

- gateway version / commit;
- Linux distribution and Docker version;
- whether reverse or forward WebSocket was used;
- the OneBot action or event shape involved;
- sanitized gateway/panel logs; never post QR images, access tokens, WeChat
  profile files, chat screenshots, or message history.

### Current capability matrix

| Capability | State | Notes |
|---|---|---|
| Official WeChat QR login in Docker | Verified | Uses the official Linux client. |
| Management panel | Verified | QR/status, mappings, protocol config, sanitized logs. |
| OneBot V11 reverse WebSocket | Verified | Tested with a local Shell WebSocket client. |
| OneBot V11 forward WebSocket | Implemented | Configuration hot-reloads; third-party compatibility still needs testing. |
| `get_friend_list` | Verified | Returns approved local mappings. |
| `send_private_msg` | Verified | UI-submitted text only; no recipient read/delivery guarantee. |
| Private text inbound | Experimental / disabled | Fail-closed while visual identity and copy verification are calibrated. |
| Group inbound | Not supported | Not emitted as private events. |
| Native group `@` mentions | Not supported | Not emulated as literal text. |
| Media/file/sticker/reply fidelity | Not supported | Text-only scope. |

## Supported scope

| Capability | Status |
|---|---|
| Official WeChat QR login in Docker | Supported |
| Token-protected management panel | Supported |
| OneBot V11 reverse WebSocket | Supported |
| OneBot V11 forward WebSocket | Supported; optional |
| `get_friend_list` | Supported for approved mappings |
| `send_private_msg` | Supported; UI-submitted text only |
| Private text inbound | Experimental, disabled by default |
| Group inbound | Not supported |
| Native group mentions | Not supported |
| Media/file/sticker/reply fidelity | Not supported |

## Quick start

### 1. Obtain the official client package

Download the official Tencent WeChat Linux x86_64 `.deb` package and place it at:

```text
runtime/installers/WeChatLinux_x86_64.deb
```

The package is deliberately not included in this repository. See
[`runtime/installers/README.md`](runtime/installers/README.md).

### 2. Build and start

```bash
docker compose up -d --build
```

### 3. Open the management panel

Provide a random `PANEL_TOKEN` to the panel process or your deployment wrapper.
The panel is the normal UI for QR login, protocol configuration, contact mapping,
and sanitized runtime logs. noVNC is maintenance-only and must not be exposed
publicly.

## OneBot V11

### Reverse WebSocket

The default host-local endpoint is:

```text
ws://127.0.0.1:16700
```

Use standard actions:

```json
{"action":"get_friend_list","params":{}}
```

```json
{
  "action": "send_private_msg",
  "params": {
    "user_id": 123456,
    "message": "Hello"
  }
}
```

`send_private_msg` is UI-submitted: an `ok` response means the gateway submitted
the text through the verified WeChat UI flow. It is not proof of recipient read
or delivery.

### Forward WebSocket

Configure the forward URL and enabled state through the panel. Forward WebSocket
configuration hot-reloads. Reverse listener address/port changes require a
gateway restart. Docker publishes the reverse port to `127.0.0.1` by default.

### Capability status

Call `get_status` to retrieve the explicit capability boundary. A current
example:

```json
{
  "private_text_inbound": false,
  "private_text_inbound_experimental": true,
  "group_inbound": false,
  "native_mentions": false,
  "requires_unpinned_unfolded_inbox": true
}
```

## Experimental private inbound roadmap

The project is developing a fail-closed private-text reader. It will publish
nothing unless all evidence is present:

1. approved private conversation visual identity;
2. stable two-frame inbox snapshot;
3. no pinned or folded conversations;
4. verified selected row and chat header;
5. unobscured message pane;
6. verified copy of one complete incoming text bubble.

During experimental use, do **not** pin conversations or fold conversation/group
containers. Unknown, ambiguous, occluded, duplicate-title, group, or mention
cases are quarantined rather than emitted as incorrect OneBot events.

## Security and privacy

- Keep `runtime/`, `evidence/`, panel tokens, screenshots, profile data, SQLite
  databases, logs and the official `.deb` out of Git.
- Do not expose noVNC, Docker APIs, SSH, the dashboard, or OneBot ports to the
  public internet.
- The repository `.gitignore` is designed to prevent accidental publication of
  login/session material, QR images and local evidence.
- This project intentionally avoids private protocol emulation and decrypting
  local WeChat data.

## Development verification

```bash
python3 -m unittest discover -s gateway/tests -v
python3 -m unittest discover -s ui_worker/tests -v
python3 -m unittest discover -s panel/tests -v
```

## License

Apache License 2.0. The official WeChat client remains subject to Tencent's
terms and license.
