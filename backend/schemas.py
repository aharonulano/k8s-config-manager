from pydantic import BaseModel
from typing import List, Dict, Optional

class ContainerConfig(BaseModel):
    name: str
    image: str
    ports: List[int]

class DeploymentConfig(BaseModel):
    name: str
    replicas: int
    namespace: str
    containers: List[ContainerConfig]

class ServiceConfig(BaseModel):
    name: str
    namespace: str
    ports: List[Dict[str, int]]  # לדוגמה [{"port": 80, "targetPort": 8080}]

class ConfigMapConfig(BaseModel):
    name: str
    namespace: str
    data: Dict[str, str]

class SecretConfig(BaseModel):
    name: str
    namespace: str
    data: Dict[str, str]  # המידע צריך להיות מקודד ב-Base64 בצד הלקוח
