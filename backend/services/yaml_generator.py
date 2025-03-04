import yaml
import json
from schemas import DeploymentConfig, ServiceConfig, ConfigMapConfig, SecretConfig

def generate_deployment(config: DeploymentConfig, output_format: str = "yaml") -> str:
    k8s_manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": config.name, "namespace": config.namespace},
        "spec": {
            "replicas": config.replicas,
            "selector": {"matchLabels": {"app": config.name}},
            "template": {
                "metadata": {"labels": {"app": config.name}},
                "spec": {
                    "containers": [
                        {"name": c.name, "image": c.image, "ports": [{"containerPort": p} for p in c.ports]}
                        for c in config.containers
                    ]
                }
            },
        },
    }
    return yaml.dump(k8s_manifest, default_flow_style=False) if output_format == "yaml" else json.dumps(k8s_manifest, indent=4)

def generate_service(config: ServiceConfig, output_format: str = "yaml") -> str:
    k8s_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": config.name, "namespace": config.namespace},
        "spec": {
            "selector": {"app": config.name},
            "ports": [{"port": p["port"], "targetPort": p["targetPort"]} for p in config.ports]
        }
    }
    return yaml.dump(k8s_manifest, default_flow_style=False) if output_format == "yaml" else json.dumps(k8s_manifest, indent=4)

def generate_configmap(config: ConfigMapConfig, output_format: str = "yaml") -> str:
    k8s_manifest = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": config.name, "namespace": config.namespace},
        "data": config.data
    }
    return yaml.dump(k8s_manifest, default_flow_style=False) if output_format == "yaml" else json.dumps(k8s_manifest, indent=4)

def generate_secret(config: SecretConfig, output_format: str = "yaml") -> str:
    k8s_manifest = {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {"name": config.name, "namespace": config.namespace},
        "data": config.data  # הנתונים צריכים להיות מקודדים ב-Base64
    }
    return yaml.dump(k8s_manifest, default_flow_style=False) if output_format == "yaml" else json.dumps(k8s_manifest, indent=4)
