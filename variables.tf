variable "project_name" {
  description = "Nombre corto del proyecto para nombrar los recursos en Azure."
  type        = string
  default     = "utvt-net"

  validation {
    condition     = length(var.project_name) >= 3 && length(var.project_name) <= 20 && can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "project_name debe tener entre 3 y 20 caracteres y contener solo minúsculas, números o guiones."
  }
}

variable "environment" {
  description = "Ambiente del despliegue: dev, qa o prod."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "qa", "prod"], var.environment)
    error_message = "environment debe ser uno de los siguientes: dev, qa o prod."
  }
}

variable "location" {
  description = "Región de Azure donde se desplegarán los recursos (autorizada por Azure Policy)."
  type        = string
  default     = "eastus"
}

variable "vnet_address_space" {
  description = "Espacios de direcciones CIDR para la red virtual."
  type        = list(string)
  default     = ["10.0.0.0/16"]

  validation {
    condition     = length(var.vnet_address_space) > 0 && alltrue([for cidr in var.vnet_address_space : can(cidrnetmask(cidr))])
    error_message = "vnet_address_space debe contener al menos un bloque CIDR válido."
  }
}

variable "tags" {
  description = "Etiquetas adicionales para la gobernanza de los recursos."
  type        = map(string)
  default = {
    managed_by = "terraform"
  }
}

variable "subscription_id" {
  description = "Identificador UUID de la suscripción de Azure."
  type        = string
  sensitive   = true

  validation {
    condition     = can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", var.subscription_id))
    error_message = "subscription_id debe tener formato UUID válido."
  }
}
