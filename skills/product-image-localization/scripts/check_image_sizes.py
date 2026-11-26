"""Check the strict byte limit for delivered product images."""
import argparse
import sys
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

BYTE_LIMIT = 2_000_000
IMAGE_EXTENSIONS = {".avif", ".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


def collect_sizes(path):
    if path.is_dir():
        return [
            (file.relative_to(path).as_posix(), file.stat().st_size)
            for file in sorted(path.rglob("*"))
            if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
        ]
    if path.suffix.lower() == ".zip":
        with ZipFile(path) as archive:
            corrupt = archive.testzip()
            if corrupt is not None:
                raise ValueError(f"ZIP 条目损坏: {corrupt}")
            return [
                (entry.filename, entry.file_size)
                for entry in archive.infolist()
                if not entry.is_dir()
                and PurePosixPath(entry.filename).suffix.lower() in IMAGE_EXTENSIONS
            ]
    if path.suffix.lower() in IMAGE_EXTENSIONS:
        return [(path.name, path.stat().st_size)]
    raise ValueError("请提供图片、图片目录或 ZIP")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        sizes = collect_sizes(args.path)
        if not sizes:
            raise ValueError("未发现支持的图片")
    except (OSError, ValueError, BadZipFile, RuntimeError, NotImplementedError) as exc:
        print(f"检查失败: {exc}", file=sys.stderr)
        return 2

    oversize = [(name, size) for name, size in sizes if size >= BYTE_LIMIT]
    for name, size in oversize:
        print(f"超限: {name} ({size:,} 字节)", file=sys.stderr)
    print(f"图片 {len(sizes)} 张，最大 {max(size for _, size in sizes):,} 字节，超限 {len(oversize)} 张")
    return 1 if oversize else 0


if __name__ == "__main__":
    raise SystemExit(main())
