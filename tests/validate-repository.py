"""Validate Git-index data, new documentation and recovered artifact integrity."""
import argparse
import ast
from collections import Counter
import csv
import hashlib
from io import BytesIO
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
TEXT = {
    ".csv", ".fcmacro", ".gcode", ".hpp", ".cpp", ".html", ".js", ".json", ".log",
    ".md", ".py", ".ps1", ".sh", ".sha256", ".svg", ".txt", ".xml", ".config", ".rels",
    ".env", ".example", ".yml", ".yaml", ".step", ".stp", ".model",
}
CONTAINERS = {".fcstd", ".fcstd1", ".fcbak", ".fcstd2", ".3mf", ".zip"}
SECRETS = re.compile(
    rb"-----BEGIN (?:OPENSSH |RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY-----"
    rb"|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}"
    rb"|(?:AKIA|ASIA)[A-Z0-9]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}"
    rb"|\b(?:api[_-]?key|password|passwd|wifi[_-]?psk|client_secret)\s*['\"]?\s*[:=]\s*['\"][^'\"\r\n]{6,}['\"]", re.I
)
PRIVATE = re.compile(rb"(?<![\w.])(?:192\.168|10\.\d{1,3}|172\.(?:1[6-9]|2[0-9]|3[01]))\.\d{1,3}\.\d{1,3}(?![\w.])"
                     rb"|[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s<>'\"]+", re.I)
EMAIL = re.compile(rb"(?<![A-Z0-9._%+-])[A-Z0-9._%+-]{1,64}@[A-Z0-9.-]{1,253}\.[A-Z]{2,}", re.I)
SECRET_MARKERS = (b'private key', b'ghp_', b'gho_', b'ghu_', b'ghs_', b'ghr_',
                  b'github_pat_', b'akia', b'asia', b'sk-', b'password', b'passwd',
                  b'api_key', b'apikey', b'api-key', b'wifi', b'client_secret')
LINK = re.compile(r"\]\(([^)\n]+)\)|\bsrc=\"([^\"]+)\"")


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def indexed_paths():
    return [part.decode("utf-8") for part in git("ls-files", "-z").split(b"\0") if part]


def inspect(name, data, failures, counts, depth=0):
    counts["files scanned" if depth == 0 else "embedded files scanned"] += 1
    ext = PurePosixPath(name).suffix.lower()
    lowered = data.lower()
    secret = any(marker in lowered for marker in SECRET_MARKERS) and SECRETS.search(data)
    private = ext in TEXT and (
        (b"@" in data and EMAIL.search(data))
        or (any(marker in lowered for marker in (b"192.168", b"10.", b"172.", b"users"))
            and PRIVATE.search(data))
    )
    if secret or private:
        failures.append(f"Credential or private identifier pattern in {name}")
    if depth == 0 and len(data) >= 100 * 1024**2:
        failures.append(f"GitHub size limit: {name}")
    if depth == 0 and ext in {".png", ".jpg", ".jpeg"}:
        if b"Exif\x00\x00" in data or b"http://ns.adobe.com/xap/1.0/" in data:
            failures.append(f"Photo metadata present: {name}")
    if ext in CONTAINERS and zipfile.is_zipfile(BytesIO(data)):
        if depth >= 4:
            failures.append(f"Container nesting limit: {name}")
            return
        with zipfile.ZipFile(BytesIO(data)) as archive:
            entries = archive.infolist()
            expanded = sum(member.file_size for member in entries)
            if expanded > 500_000_000:
                failures.append(f"Container expansion limit: {name}")
                return
            for member in entries:
                path = PurePosixPath(member.filename.replace("\\", "/"))
                if path.is_absolute() or ".." in path.parts or re.match(r"^[A-Za-z]:", member.filename):
                    failures.append(f"Unsafe container path in {name}")
                    continue
                if not member.is_dir():
                    inspect(f"{name}!{member.filename}", archive.read(member), failures, counts, depth + 1)
    elif ext in CONTAINERS:
        failures.append(f"Unreadable archive: {name}")


def check_docs(files, failures, counts):
    for name in files:
        if not name.endswith(".md") or name.startswith("archive/engineering/"):
            continue
        path = ROOT / name
        content = re.sub(r"(?ms)^" + chr(96) * 3 + r".*?^" + chr(96) * 3 + r"\s*$", "", path.read_text(encoding="utf-8"))
        for match in LINK.finditer(content):
            link = next(item for item in match.groups() if item is not None)
            parts = urlsplit(link)
            if parts.scheme or not parts.path:
                continue
            destination = (path.parent / unquote(parts.path)).resolve().relative_to(ROOT).as_posix()
            counts["relative documentation links"] += 1
            if destination not in files and not any(item.startswith(destination + "/") for item in files):
                failures.append(f"Broken link in {name}: {link}")
            elif parts.fragment and destination.endswith(".md"):
                headings = re.findall(r"(?m)^#+ (.+)$", (ROOT / destination).read_text(encoding="utf-8"))
                anchors = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings}
                if unquote(parts.fragment) not in anchors:
                    failures.append(f"Broken heading link in {name}: {link}")


def check_manifest(files, failures, counts):
    hashed = {}
    with (ROOT / "archive/recovery-manifest.csv").open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            dest = row["destination"]
            if not dest:
                continue
            if dest not in files:
                failures.append(f"Missing manifest destination: {dest}")
                continue
            if dest not in hashed:
                hashed[dest] = hashlib.sha256((ROOT / dest).read_bytes()).hexdigest()
            if row["staged_sha256"] != hashed[dest]:
                failures.append(f"Manifest hash mismatch: {dest}")
    counts["unique manifest destinations verified"] = len(hashed)
    demo = ROOT / "media" / "demonstration"
    expected, name = (demo / "SHA256SUMS").read_text(encoding="utf-8").split()
    if hashlib.sha256((demo / name).read_bytes()).hexdigest() != expected:
        failures.append("Demonstration preview hash mismatch")
    else:
        counts["demonstration previews verified"] += 1


def check_python(files, failures, counts):
    for name in files:
        if not name.endswith(".py"):
            continue
        try:
            ast.parse((ROOT / name).read_bytes(), filename=name)
        except SyntaxError as error:
            if name.startswith("archive/engineering/"):
                print(f"Historical Python syntax finding: {name}:{error.lineno}")
                counts["historical syntax findings"] += 1
            else:
                failures.append(f"Python syntax error: {name}:{error.lineno}: {error.msg}")
        else:
            counts["Python files parsed"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--working-tree", action="store_true", help="scan before staging")
    args = parser.parse_args()
    if args.working_tree:
        file_paths = git("ls-files", "--cached", "--others", "--exclude-standard", "-z")
        files = set(part.decode("utf-8") for part in file_paths.split(b"\0") if part)
    else:
        files = set(indexed_paths())
        subprocess.run(["git", "diff", "--exit-code"], cwd=ROOT, check=True)
    failures = []
    counts = Counter()
    for name in sorted(files):
        inspect(name, (ROOT / name).read_bytes(), failures, counts)
    check_docs(files, failures, counts)
    check_manifest(files, failures, counts)
    check_python(files, failures, counts)
    for key, value in sorted(counts.items()):
        print(f"{key}: {value}")
    for failure in failures:
        print(failure)
    print(f"validation failures: {len(failures)}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
