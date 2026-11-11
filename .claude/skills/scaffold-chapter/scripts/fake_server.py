"""A stand-in OpenAI-compatible server, so workbooks can execute without a model.

    python fake_server.py [port=11434] [content]

Every POST answers with one assistant message whose content is `content`
(default: a snippet that satisfies the Chapter 3 cells). Chapters whose cells
need tool calls or embeddings: extend `reply()` for those request shapes.
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 11434
CONTENT = sys.argv[2] if len(sys.argv) > 2 else "def roman_to_int(s):\n    return 3\n\nAnswer: 5"


def reply(path, body):
    return {
        "model": body.get("model", "fake"),
        "choices": [{"index": 0, "message": {"role": "assistant", "content": CONTENT}}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1},
    }


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        data = json.dumps(reply(self.path, body)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
