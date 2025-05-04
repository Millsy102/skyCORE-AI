
import difflib

def generate_diff_preview(original, updated, filename="file"):
    original_lines = original.splitlines(keepends=True)
    updated_lines = updated.splitlines(keepends=True)
    diff = difflib.unified_diff(original_lines, updated_lines, fromfile=f"{filename} (before)", tofile=f"{filename} (after)")
    return ''.join(diff)
