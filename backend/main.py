from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from schemas import DeploymentConfig, ServiceConfig, ConfigMapConfig, SecretConfig
from schemas1 import K8sResourceRequest, K8sZipRequest
from services.zip_generator import create_zip
from services.yaml_generator import (
    generate_deployment,
    generate_service,
    generate_configmap,
    generate_secret
)
import os

app = FastAPI()

OUTPUT_DIR = "output_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_file(content: str, filename: str) -> str:
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

@app.post("/generate/{resource_type}/")
def generate_resource(
    resource_type: str,
    output_format: str = Query("yaml", enum=["yaml", "json"]),
    config: dict = None
):
    generator_map = {
        "deployment": generate_deployment,
        "service": generate_service,
        "configmap": generate_configmap,
        "secret": generate_secret,
    }

    if resource_type not in generator_map:
        return {"error": "Invalid resource type"}

    # יצירת הקובץ בפורמט הנדרש
    content = generator_map[resource_type](config, output_format)
    filename = f"{resource_type}.{output_format}"
    file_path = save_file(content, filename)

    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
