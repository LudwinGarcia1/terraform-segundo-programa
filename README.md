# Segundo programa de Terraform: Redes en Azure

Práctica académica de Terraform basada en el laboratorio [`segundo-programa`](https://github.com/jorgealmeidamontiel/terraform-laboratories/tree/main/segundo-programa).

Despliega en Microsoft Azure la infraestructura básica de red para un entorno de desarrollo (`dev`), incluyendo un Grupo de Recursos y una Red Virtual (*Virtual Network*), siguiendo las convenciones de nomenclatura del Cloud Adoption Framework (CAF) y las directivas de gobernanza regional de Azure for Students.

## Recursos Gestionados

| Recurso | Nombre CAF | Descripción |
|---|---|---|
| `azurerm_resource_group` | `rg-utvt-net-dev-eastus-001` | Grupo de recursos contenedor para el entorno de desarrollo. |
| `azurerm_virtual_network` | `vnet-utvt-net-dev-eastus-001` | Red virtual con espacio de direcciones CIDR `10.0.0.0/16`. |

## Estructura del Proyecto

| Archivo | Propósito |
|---|---|
| `providers.tf` | Declaración del bloque `terraform` y configuración del proveedor `hashicorp/azurerm`. |
| `variables.tf` | Definición de variables tipadas (`string`, `list`, `map`) con reglas de validación. |
| `locals.tf` | Nombres calculados con formato CAF y combinación (*merge*) de etiquetas de gobernanza. |
| `main.tf` | Definición de los recursos de Azure (`azurerm_resource_group` y `azurerm_virtual_network`). |
| `outputs.tf` | Exportación de identificadores, nombres y bloques CIDR generados. |
| `terraform.tfvars.example` | Plantilla de configuración con parámetros recomendados. |
| `.gitignore` | Exclusión de archivos de estado (`*.tfstate`) y valores sensibles (`*.tfvars`). |

## Requisitos Previos

- **Terraform CLI**: `>= 1.9.0` (probado con `v1.16.2`).
- **Azure CLI**: `2.90.0` o superior con sesión iniciada (`az login`).
- **Proveedor registrado**: `Microsoft.Network` en la suscripción activa.

## Instrucciones de Ejecución

```bash
# 1. Iniciar sesión en Microsoft Azure
az login

# 2. Registrar el proveedor de redes (si no estuviese activo)
az provider register --namespace Microsoft.Network --wait

# 3. Preparar variables de entorno
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars colocando el subscription_id correspondiente

# 4. Inicializar y validar
terraform init
terraform validate

# 5. Planificar y aplicar
terraform plan -out tfplan
terraform apply tfplan

# 6. Consultar salidas
terraform output

# 7. Destruir recursos al finalizar la práctica
terraform destroy -auto-approve
```
