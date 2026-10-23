#!/usr/bin/env python3
"""Sammel-Upload von Theme-Dateien über Shopify Staged Uploads.

  upload.py stage   <v2-dir>                    -> Variablen für stagedUploadsCreate (stdout)
  upload.py put     <v2-dir> <targets.json>     -> PUT jeder Datei an ihre signierte URL
  upload.py upsert  <targets.json>              -> Variablen für themeFilesUpsert (stdout)
  upload.py verify  <v2-dir> <checksums.json>   -> Abgleich new_md5 vs. Shopify checksumMd5

targets.json: [{"path": "snippets/x.liquid", "url": "<signierte PUT-URL>"}, ...]
checksums.json: Ausgabe von theme.files.nodes [{"filename","size","checksumMd5"}, ...]
"""
import hashlib, json, pathlib, subprocess, sys

THEME_ID = "gid://shopify/OnlineStoreTheme/207286141265"


def manifest(v2):
    return json.loads((pathlib.Path(v2) / "manifest.json").read_text(encoding="utf-8"))


def staged_name(path):
    return path.replace("/", "__")


def cmd_stage(v2):
    items = []
    for m in manifest(v2):
        f = pathlib.Path(v2) / "new" / m["path"]
        items.append({"filename": staged_name(m["path"]), "mimeType": "text/plain",
                      "resource": "FILE", "httpMethod": "PUT", "fileSize": str(f.stat().st_size)})
    print(json.dumps({"input": items}, ensure_ascii=False))


def cmd_put(v2, targets):
    ok = True
    for t in json.loads(pathlib.Path(targets).read_text(encoding="utf-8")):
        f = pathlib.Path(v2) / "new" / t["path"]
        assert staged_name(t["path"]) in t["url"].split("?")[0], f"URL passt nicht zu {t['path']}"
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT",
                            "-H", "Content-Type: text/plain", "--data-binary", f"@{f}", t["url"]],
                           capture_output=True, text=True)
        print(f"{r.stdout}  {t['path']}")
        ok &= r.stdout == "200"
    sys.exit(0 if ok else 1)


def cmd_upsert(targets):
    files = [{"filename": t["path"], "body": {"type": "URL", "value": t["url"].split("?")[0]}}
             for t in json.loads(pathlib.Path(targets).read_text(encoding="utf-8"))]
    print(json.dumps({"themeId": THEME_ID, "files": files}, ensure_ascii=False))


def cmd_verify(v2, sums):
    have = {n["filename"]: n for n in json.loads(pathlib.Path(sums).read_text(encoding="utf-8"))}
    ok = True
    for m in manifest(v2):
        f = pathlib.Path(v2) / "new" / m["path"]
        md5 = hashlib.md5(f.read_bytes()).hexdigest()
        s = have.get(m["path"], {})
        hit = s.get("checksumMd5") == md5 and str(s.get("size")) == str(f.stat().st_size)
        ok &= hit
        print(f"{'✓' if hit else '✗'} {m['path']}  lokal {f.stat().st_size} {md5}  shopify {s.get('size')} {s.get('checksumMd5')}")
    print("ALLES BYTE-GENAU" if ok else "ABWEICHUNGEN VORHANDEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    c, *a = sys.argv[1:]
    {"stage": cmd_stage, "put": cmd_put, "upsert": cmd_upsert, "verify": cmd_verify}[c](*a)
