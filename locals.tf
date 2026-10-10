# Valores locales calculados para la nomenclatura CAF (Cloud Adoption Framework)
# y la taxonomía común de etiquetas de gobernanza en Azure.
locals {
  resource_group_name  = "rg-${var.project_name}-${var.environment}-${var.location}-001"
  virtual_network_name = "vnet-${var.project_name}-${var.environment}-${var.location}-001"

  common_tags = merge(
    var.tags,
    {
      Project     = var.project_name
      Environment = var.environment
      Location    = var.location
      Practice    = "segundo-programa"
      Owner       = "Ludwin Garcia Gaytan"
      ManagedBy   = "terraform"
    }
  )
}
