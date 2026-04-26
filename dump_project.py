import os
from pathlib import Path
from collections import defaultdict

# ================= CONFIG =================
PROJECT_ROOT = Path(".").resolve()
OUTPUT_FILE = "project_dump.txt"

EXCLUDE_DIRS = {
    "__pycache__",
    "migrations",
    "staticfiles",
    "media",
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "tests",
}

EXCLUDE_FILES = {
    "__init__.py",
    "admin.py",
    "apps.py",
}

INCLUDE_EXTENSIONS = {
    ".py",
    ".html",
    ".js",
    ".ts",
    ".json",
    ".md",
    ".txt",
    ".css",
}

MAX_FILE_SIZE_MB = 2
# ==========================================


def should_skip_file(file_path: Path) -> bool:
    if file_path.name in EXCLUDE_FILES:
        return True

    if not any(file_path.name.endswith(ext) for ext in INCLUDE_EXTENSIONS):
        return True

    try:
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            return True
    except Exception:
        return True

    return False


def get_app_name(file_path: Path) -> str:
    parts = file_path.relative_to(PROJECT_ROOT).parts
    return parts[0] if len(parts) > 1 else "root"


def collect_files_grouped(root: Path):
    grouped = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root):
        # prune unwanted directories early
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for filename in filenames:
            file_path = Path(dirpath) / filename

            if should_skip_file(file_path):
                continue

            app_name = get_app_name(file_path)
            grouped[app_name].append(file_path)

    return grouped


def write_output(grouped_files):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for app in sorted(grouped_files.keys()):
            out.write("\n" + "#" * 80 + "\n")
            out.write(f"APP: {app}\n")
            out.write("#" * 80 + "\n\n")

            for file_path in sorted(grouped_files[app]):
                try:
                    relative_path = file_path.relative_to(PROJECT_ROOT)

                    out.write("=" * 80 + "\n")
                    out.write(f"FILE: {relative_path}\n")
                    out.write("=" * 80 + "\n\n")

                    with open(file_path, "r", encoding="utf-8") as f:
                        out.write(f.read())
                        out.write("\n\n")

                except Exception as e:
                    print(f"Skipping {file_path}: {e}")


def main():
    grouped_files = collect_files_grouped(PROJECT_ROOT)
    write_output(grouped_files)
    print(f"Done. Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()