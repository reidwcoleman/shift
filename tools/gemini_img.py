"""Tiny Gemini image client. Usage: gemini_img.py OUT.png "prompt" [ref1.png ref2.png ...]"""
import sys, os, json, base64, urllib.request, mimetypes
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def key():
    for line in open(os.path.join(ROOT, ".env")):
        if line.startswith("GEMINI_API_KEY="): return line.split("=",1)[1].strip().strip('"')
    raise SystemExit("no GEMINI_API_KEY in .env")
def generate(prompt, refs=(), model="gemini-3.1-flash-image", aspect="1:1", out=None):
    parts = []
    for r in refs:
        mt = mimetypes.guess_type(r)[0] or "image/png"
        parts.append({"inline_data": {"mime_type": mt, "data": base64.b64encode(open(r,"rb").read()).decode()}})
    parts.append({"text": prompt})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key()}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p:
                data = base64.b64decode(p["inlineData"]["data"])
                if out: open(out, "wb").write(data)
                return data
    raise RuntimeError(json.dumps(d)[:800])
if __name__ == "__main__":
    out, prompt, refs = sys.argv[1], sys.argv[2], sys.argv[3:]
    generate(prompt, refs, out=out); print("wrote", out)
