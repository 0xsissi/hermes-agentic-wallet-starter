"""Build a source-only ZIP. Runtime directories and credentials are never included."""
from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP_LEVEL = {
    ".gitignore", ".gitattributes", "AGENTS.md", "install.ps1", "install.sh", "LICENSE",
    "package.json", "README.md", "starter.mjs", "versions.json",
}
DIRECTORIES = {".github", "assets", "docs", "lib", "scripts", "tests"}
ALLOWED_SUFFIXES = {".md", ".mjs", ".py", ".yml", ".yaml", ".svg", ".png"}
APPROVED_TEXT = {"docs/X-LONGPOST.txt", "docs/X-LONGPOST.html", "docs/X-PASTE.html"}


def sources() -> list[Path]:
    files = [ROOT / name for name in TOP_LEVEL]
    for name in DIRECTORIES:
        directory = ROOT / name
        if directory.exists():
            files.extend(p for p in directory.rglob("*") if p.is_file())
    result = []
    for file in sorted(files):
        relative = file.relative_to(ROOT)
        if any(part in {"__pycache__", "node_modules", ".runtime", ".git"} for part in relative.parts):
            continue
        if relative.parts[0] not in TOP_LEVEL and file.suffix not in ALLOWED_SUFFIXES and relative.as_posix() not in APPROVED_TEXT:
            raise RuntimeError(f"Unexpected source type: {relative}")
        if file.is_symlink() or any(p.is_symlink() for p in file.parents if p != ROOT.parent):
            raise RuntimeError(f"Symlink is not a distributable source file: {relative}")
        if not file.is_file():
            raise RuntimeError(f"Missing source: {relative}")
        result.append(file)
    return result


def main() -> None:
    output_dir = ROOT.parent / "output"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "hermes-agentic-wallet-starter-0.1.0.zip"
    manifest = []
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in sources():
            data = file.read_bytes()
            relative = file.relative_to(ROOT).as_posix()
            archive.writestr(f"hermes-agentic-wallet-starter/{relative}", data)
            manifest.append(f"{hashlib.sha256(data).hexdigest()}  {relative}")
        archive.writestr("hermes-agentic-wallet-starter/SHA256SUMS.txt", "\n".join(manifest) + "\n")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".zip.sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    print(f"Built {output}: {len(manifest)} source files, {output.stat().st_size} bytes")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
