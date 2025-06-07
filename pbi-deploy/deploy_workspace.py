from pathlib import Path
import os
from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items

root_directory = Path(__file__).resolve().parent

# Parameters for the FabricWorkspace Connection
workspace_id = os.getenv("FABRIC_WORKSPACE_ID")
repository_directory = os.path.join(os.getenv("GITHUB_WORKSPACE", "."), "src")
client_id = os.getenv("FABRIC_CLIENT_ID")
client_secret = os.getenv("FABRIC_CLIENT_SECRET")
tenant_id = os.getenv("FABRIC_TENANT_ID")

# Verificação das variáveis obrigatórias
missing_vars = []
if not client_id:
    missing_vars.append("FABRIC_CLIENT_ID")
if not client_secret:
    missing_vars.append("FABRIC_CLIENT_SECRET")
if not tenant_id:
    missing_vars.append("FABRIC_TENANT_ID")

if missing_vars:
    raise ValueError(f"As seguintes variáveis de ambiente estão vazias ou não definidas: {', '.join(missing_vars)}")

token_credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)

# Supported Item Types fabric-cicd
item_type_in_scope = [
                      "SemanticModel", 
                      "Report", 
                      "DataPipeline", 
                      "Environment", 
                      "Notebook", 
                      "Lakehouse", 
                      "MirroredDatabase", 
                      "VariableLibrary", 
                      "CopyJob", 
                      "Eventhouse",
                      "KQLDatabase",
                      "KQLQueryset",
                      "Reflex",
                      "Eventstream",
                      "Warehouse",
                      "SQLDatabase"
                      ]

# Initialize the FabricWorkspace object with the configured parameters
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    repository_directory=repository_directory,
    item_type_in_scope=item_type_in_scope,
    token_credential=token_credential,
)

# Publish all items defined in item_type_in_scope
publish_all_items(target_workspace)
