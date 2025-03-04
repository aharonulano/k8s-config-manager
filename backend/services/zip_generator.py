import os
import shutil
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from services.file_generator import generate_deployment, generate_service, generate_configmap, generate_secret

OUTPUT_DIR = "output_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

generator_map = {
    "deployment": generate_deployment,
    "service": generate_service,
    "configmap": generate_configmap,
    "secret": generate_secret,
}

def save_file(content: str, filename: str) -> str:
    """ שמירת קובץ בספריית output_files """
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

def create_zip(resources: list, output_format: str, zip_filename: str) -> str:
    """ יצירת קובץ ZIP עם המשאבים שביקש המשתמש """
    zip_filepath = os.path.join(OUTPUT_DIR, zip_filename)

    with shutil.ZipFile(zip_filepath, 'w') as zipf:
        for resource_type in resources:
            if resource_type in generator_map:
                content = generator_map[resource_type](config={}, output_format=output_format)
                filename = f"{resource_type}.{output_format}"
                file_path = save_file(content, filename)
                zipf.write(file_path, filename)

    return zip_filepath
