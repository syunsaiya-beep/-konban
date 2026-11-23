#!/usr/bin/env python3
"""LM Studio のローカルサーバー(OpenAI互換API)にチャットを送る最小クライアント。

使い方:
  1. LM Studio でモデルを読み込み、Developer タブから「Start Server」を押す
  2. python lmstudio_chat.py "こんにちは"
環境変数:
  LMSTUDIO_URL    既定 http://localhost:1234/v1
  LMSTUDIO_MODEL  未指定なら読み込み済みモデルを自動選択
"""
import json
import os
import sys
import urllib.request

BASE = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1")


def _request(path, payload=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def chat(prompt, model=None, system="あなたは親切なアシスタントです。"):
    model = model or os.environ.get("LMSTUDIO_MODEL") or _request("/models")["data"][0]["id"]
    res = _request("/chat/completions", {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    })
    return res["choices"][0]["message"]["content"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('使い方: python lmstudio_chat.py "質問"')
    print(chat(" ".join(sys.argv[1:])))
