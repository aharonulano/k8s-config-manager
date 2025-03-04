from pydantic import BaseModel, Field
from typing import List, Optional

class K8sResourceRequest(BaseModel):
    """Schema for Kubernetes resource generation request"""
    name: str = Field(..., title="Resource Name", description="The name of the Kubernetes resource")
    namespace: Optional[str] = Field("default", title="Namespace", description="The Kubernetes namespace")
    replicas: Optional[int] = Field(1, title="Replicas", description="Number of replicas for the deployment")
    memory: Optional[str] = Field("256Mi", title="Memory", description="Memory request for the pod")
    cpu: Optional[str] = Field("250m", title="CPU", description="CPU request for the pod")
    user: Optional[str] = Field(None, title="User", description="User associated with RBAC or secret")
    password: Optional[str] = Field(None, title="Password", description="Password for secret configurations")
    role: Optional[str] = Field(None, title="Role", description="RBAC role for the user")
    permissions: Optional[List[str]] = Field([], title="Permissions", description="List of permissions for RBAC")
    resource_type: str = Field(..., title="Resource Type", description="Type of Kubernetes resource", example="deployment")

class K8sZipRequest(BaseModel):
    """Schema for generating ZIP with multiple Kubernetes resources"""
    resources: List[str] = Field(..., title="Resources", description="List of Kubernetes resource types (e.g., deployment, service)")
    output_format: str = Field("yaml", title="Output Format", description="Format of the generated files (yaml/json)", regex="^(yaml|json)$")
