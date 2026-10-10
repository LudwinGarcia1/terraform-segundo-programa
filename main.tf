# Grupo de recursos principal que delimita el ciclo de vida de los componentes del entorno DEV.
resource "azurerm_resource_group" "rg" {
  name     = local.resource_group_name
  location = var.location

  tags = local.common_tags
}

# Red virtual (Virtual Network) para el aislamiento del tráfico y direccionamiento privado.
resource "azurerm_virtual_network" "vnet" {
  name                = local.virtual_network_name
  address_space       = var.vnet_address_space
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  tags = local.common_tags
}
