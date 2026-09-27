import os
import zipfile
import io

def get_workspace_zip(directory):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(directory):
            # Ignore virtual environments, git, and python caches
            if "venv" in root or ".git" in root or "__pycache__" in root:
                continue
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zip_file.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer
