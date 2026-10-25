"""Phase 13 Lesson 01 - the tool interface driven by a REAL LLM (learner artifact).

Learner variant of phases/13-tools-and-protocols/01-the-tool-interface/code/main.py:
fake_decide is replaced by a live POST to {BASE_URL}/chat/completions with a
tools=[...] declaration, so the describe -> decide -> execute -> observe loop
runs over a real model. Stdlib only (urllib.request) to keep the wire JSON bare.

Sources: repo lesson docs/en.md; OpenAI-compatible function-calling shape
(tool_calls[].function.arguments is a JSON *string*; results return as role
"tool" messages keyed by tool_call_id).

Run (PowerShell):
  $env:OPENAI_API_KEY = "sk-..."
  python learning-artifacts/p13-01-tool-loop-real/main.py
Optional: OPENAI_BASE_URL (default https://api.openai.com/v1), OPENAI_MODEL.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

MAX_TURNS = 5

API_KEY = 'ujn-rJ3Z73zhUI3Ju9q2AEWYSB-6q-KAkR6h9SButDAuseY'
BASE_URL = 'https://llm.ujn.edu.cn/v1'
MODEL = "GLM-5.3-Flash"


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    executor: Callable[[dict], Any]
    consequential: bool = False


def tool_add(args: dict) -> dict:
    return {"sum": args["a"] + args["b"]}


def tool_get_time(args: dict) -> dict:
    tz = args.get("timezone", "UTC")
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    return {"now": now, "timezone": tz}


def tool_get_weather(args: dict) -> dict:
    fake = {"Bengaluru": 28, "Tokyo": 12, "Zurich": 4, "Lagos": 31}
    city = args["city"]
    units = args.get("units", "celsius")
    temp = fake.get(city, 20)
    if units == "fahrenheit":
        temp = round(temp * 9 / 5 + 32, 1)
    return {"city": city, "temp": temp, "units": units}


REGISTRY: list[Tool] = [
    Tool(
        name="add",
        description=(
            "Use when the user asks for the sum of two numbers. "
            "Do not use for subtraction, product, or symbolic algebra."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"],
        },
        executor=tool_add,
    ),
    Tool(
        name="get_time",
        description=(
            "Use when the user asks what time it is. "
            "Do not use for historical dates or future scheduling."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "timezone": {"type": "string"},
            },
            "required": [],
        },
        executor=tool_get_time,
    ),
    Tool(
        name="get_weather",
        description=(
            "Use when the user asks about current conditions in a named city. "
            "Do not use for forecasts or historical weather data."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "units": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["city"],
        },
        executor=tool_get_weather,
    ),
]


def validate(schema: dict, value: Any) -> list[str]:
    errors: list[str] = []
    t = schema.get("type")
    if t == "object":
        if not isinstance(value, dict):
            return [f"expected object, got {type(value).__name__}"]
        for field in schema.get("required", []):
            if field not in value:
                errors.append(f"missing required field '{field}'")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                errors.extend(validate(sub, value[key]))
        return errors
    if t == "number" and not isinstance(value, (int, float)):
        errors.append(f"expected number, got {type(value).__name__}")
    if t == "string" and not isinstance(value, str):
        errors.append(f"expected string, got {type(value).__name__}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"value {value!r} not in enum {schema['enum']}")
    return errors


def tool_specs() -> list[dict]:
    """describe 步：把注册表翻译成 OpenAI 兼容的 tools 声明发给模型。"""
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.input_schema,
            },
        }
        for t in REGISTRY
    ]


def call_api(messages: list[dict]) -> dict:
    """一次真实的 chat/completions 请求。返回解析后的 JSON。"""
    body = json.dumps(
        {
            "model": MODEL,
            "messages": messages,
            "tools": tool_specs(),
            "tool_choice": "auto",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        # provider 会把可读的错误原因放在响应体里，必须打出来才好排查
        detail = e.read().decode("utf-8", errors="replace")[:600]
        print(f"HTTP {e.code} from {BASE_URL}:\n{detail}")
        raise SystemExit(1) from None


def run_loop(user_msg: str) -> None:
    print("=" * 72)
    print(f"USER : {user_msg}")
    print("-" * 72)
    tools_by_name = {t.name: t for t in REGISTRY}
    messages: list[dict] = [{"role": "user", "content": user_msg}]
    total_tokens = 0
    for turn in range(1, MAX_TURNS + 1):
        payload = call_api(messages)
        total_tokens += payload.get("usage", {}).get("total_tokens", 0)
        assistant = payload["choices"][0]["message"]
        # assistant 消息（含 tool_calls）必须原样进 history，这是协议要求
        messages.append(assistant)
        calls = assistant.get("tool_calls")
        if not calls:
            print(f"TURN {turn} DECIDE : final answer (no tool call)")
            print(f"MODEL : {assistant.get('content')}")
            print(f"TOKENS: {total_tokens} total this query")
            return
        for call in calls:
            fn = call["function"]
            call_id = call["id"]
            print(f"TURN {turn} DECIDE : call {fn['name']} id={call_id}")
            raw_args = fn["arguments"]
            print(f"           raw arguments (JSON string!) = {raw_args}")
            tool = tools_by_name.get(fn["name"])
            try:
                args = json.loads(raw_args)
                parse_err = None
            except json.JSONDecodeError as e:
                args, parse_err = None, f"arguments not valid JSON: {e}"
            errs = [] if parse_err else (
                validate(tool.input_schema, args) if tool else ["unknown tool"]
            )
            if tool is None and not parse_err:
                errs = [f"unknown tool {fn['name']!r}"]
            if parse_err or errs:
                # 生产策略之一：把校验错误当作 tool 结果喂回去，让模型下一轮自我修正
                problem = parse_err or f"validation errors: {errs}"
                print(f"           REJECTED : {problem}")
                print("           FEEDBACK : sending error back to model for retry")
                messages.append(
                    {"role": "tool", "tool_call_id": call_id,
                     "content": json.dumps({"error": problem})}
                )
                continue
            if tool.consequential:
                print("           GATE : tool is consequential, would confirm")
            start = time.perf_counter()
            result = tool.executor(args)
            ms = (time.perf_counter() - start) * 1000
            print(f"TURN {turn} EXECUTE: {tool.name} -> {json.dumps(result)}"
                  f" [{ms:.2f} ms]")
            # observe 步：结果以 role=tool + tool_call_id 回填对话
            messages.append(
                {"role": "tool", "tool_call_id": call_id,
                 "content": json.dumps(result)}
            )
        print(f"TURN {turn} OBSERVE: messages length = {len(messages)}")
    print("LOOP TERMINATED : hit MAX_TURNS circuit breaker")


def main() -> None:
    print("=" * 72)
    print("PHASE 13 LESSON 01 - THE TOOL INTERFACE (REAL LLM)")
    print(f"BASE_URL={BASE_URL}  MODEL={MODEL}")
    print("=" * 72)
    if not API_KEY:
        print("OPENAI_API_KEY is not set. In PowerShell:")
        print('  $env:OPENAI_API_KEY = "sk-..."   # 当前终端会话生效')
        print("可选：$env:OPENAI_BASE_URL / $env:OPENAI_MODEL")
        sys.exit(1)
    for query in (
        "please add 7 and 35",
        "what time is it?",
        "tell me the weather in Tokyo, in fahrenheit please",
        "write me a haiku about tea",
    ):
        run_loop(query)
        print()


if __name__ == "__main__":
    main()
