#!/usr/bin/env python3
"""Emit a mock UI event into a running GatewayService demonstration.

This file documents the transport boundary; the real AT-SPI worker will use the
same payload contract after a user-controlled WeChat sign-in.
"""

MOCK_UI_EVENT = {
    "event_id": "mock-ui-example-001",
    "conversation_id": "alice",
    "sender_id": "alice",
    "sender_name": "Alice",
    "text": "hello from the mock UI worker",
}
