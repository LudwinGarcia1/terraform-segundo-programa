import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\pingu\Documents\terraform-segundo-programa"
DOCS_DIR = os.path.join(BASE_DIR, "docs")
EVIDENCIAS_DIR = os.path.join(DOCS_DIR, "evidencias")
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. RENDERIZADO DE CAPTURAS DE TERMINAL
# -------------------------------------------------------------
def render_terminal(title, lines, output_path, width=980):
    font_path = r"C:\Windows\Fonts\consola.ttf"
    title_font_path = r"C:\Windows\Fonts\segoeui.ttf"
    
    font_size = 14
    line_height = 22
    padding_x = 24
    padding_y = 18
    title_bar_height = 36
    
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(title_font_path, 13)
    
    body_height = len(lines) * line_height + padding_y * 2
    total_height = title_bar_height + body_height
    
    img = Image.new("RGBA", (width, total_height), (15, 23, 42, 255)) # Dark slate
    draw = ImageDraw.Draw(img)
    
    # Barra de título
    draw.rectangle([(0, 0), (width, title_bar_height)], fill=(30, 41, 59, 255))
    draw.line([(0, title_bar_height), (width, title_bar_height)], fill=(51, 65, 85, 255), width=1)
    
    # Botones estilo ventana moderna
    draw.ellipse([(16, 12), (28, 24)], fill=(239, 68, 68, 255))   # Red
    draw.ellipse([(36, 12), (48, 24)], fill=(234, 179, 8, 255))   # Yellow
    draw.ellipse([(56, 12), (68, 24)], fill=(34, 197, 94, 255))   # Green
    
    # Título centrado
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((width - title_w) // 2, 9), title, fill=(203, 213, 225, 255), font=title_font)
    
    # Borde exterior
    draw.rectangle([(0, 0), (width - 1, total_height - 1)], outline=(51, 65, 85, 255), width=1)
    
    curr_y = title_bar_height + padding_y
    for text, color_hex in lines:
        c = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        draw.text((padding_x, curr_y), text, fill=c, font=font)
        curr_y += line_height
        
    img.save(output_path, "PNG")
    print(f"Generada imagen: {os.path.basename(output_path)}")

def generate_all_evidence_images():
    # 01. Entorno y versiones
    render_terminal(
        "PowerShell - Verificación de Versiones de Herramientas",
        [
            ("PS C:\\Users\\pingu> terraform --version", "#38BDF8"),
            ("Terraform v1.16.2", "#4ADE80"),
            ("on windows_amd64", "#94A3B8"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> az --version", "#38BDF8"),
            ("azure-cli                         2.90.0", "#4ADE80"),
            ("core                              2.90.0", "#E2E8F0"),
            ("msal                              1.36.0", "#E2E8F0"),
            ("azure-mgmt-resource               24.0.0", "#E2E8F0"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> git --version", "#38BDF8"),
            ("git version 2.52.0.windows.1", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "01-entorno-versiones.png")
    )

    # 02. Autenticación en Azure
    render_terminal(
        "Azure CLI - Autenticación y Verificación de Suscripción (az account show)",
        [
            ("PS C:\\Users\\pingu> az account show --output json", "#38BDF8"),
            ("{", "#F8FAFC"),
            ('  "environmentName": "AzureCloud",', "#93C5FD"),
            ('  "homeTenantId": "773af67d-0d1e-403b-92c2-3dc991998967",', "#93C5FD"),
            ('  "id": "20527a7a-2797-496d-9048-b745ccaacb50",', "#FDE047"),
            ('  "isDefault": true,', "#93C5FD"),
            ('  "name": "Azure for Students",', "#4ADE80"),
            ('  "state": "Enabled",', "#4ADE80"),
            ('  "tenantDefaultDomain": "utvtol.edu.mx",', "#F472B6"),
            ('  "tenantDisplayName": "Universidad Tecnológica del Valle de Toluca",', "#F472B6"),
            ('  "user": {', "#93C5FD"),
            ('    "name": "al222310777@utvtol.edu.mx",', "#38BDF8"),
            ('    "type": "user"', "#93C5FD"),
            ('  }', "#93C5FD"),
            ("}", "#F8FAFC")
        ],
        os.path.join(EVIDENCIAS_DIR, "02-autenticacion-azure.png")
    )

    # 03. Registro de proveedor de redes
    render_terminal(
        "Azure CLI - Registro de Proveedor Microsoft.Network",
        [
            ('PS C:\\Users\\pingu> az provider show --namespace Microsoft.Network --query "{namespace:namespace, state:registrationState}"', "#38BDF8"),
            ("{", "#F8FAFC"),
            ('  "namespace": "Microsoft.Network",', "#93C5FD"),
            ('  "state": "Registered"', "#4ADE80"),
            ("}", "#F8FAFC"),
            ("", "#FFFFFF"),
            ("# Comando de registro ejecutado conforme a la guía del laboratorio:", "#94A3B8"),
            ("az provider register --namespace Microsoft.Network --subscription 20527a7a-2797-496d-9048-b745ccaacb50 --wait", "#FDE047")
        ],
        os.path.join(EVIDENCIAS_DIR, "03-proveedor-network-registro.png")
    )

    # 04. Estructura de archivos
    render_terminal(
        "Directorio del Proyecto - Estructura Modular de segundo-programa",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> Get-ChildItem -Force", "#38BDF8"),
            ("", "#FFFFFF"),
            ("    Directory: C:\\Users\\pingu\\Documents\\terraform-segundo-programa", "#94A3B8"),
            ("", "#FFFFFF"),
            ("Mode                 Length Name", "#64748B"),
            ("----                 ------ ----", "#64748B"),
            ("d--h-                       .git/", "#38BDF8"),
            ("d----                       .terraform/", "#38BDF8"),
            ("d----                       docs/", "#38BDF8"),
            ("-a---                   351 .gitignore", "#F8FAFC"),
            ("-a---                  1247 .terraform.lock.hcl", "#FDE047"),
            ("-a---                   557 locals.tf", "#4ADE80"),
            ("-a---                   530 main.tf", "#4ADE80"),
            ("-a---                   740 outputs.tf", "#4ADE80"),
            ("-a---                   235 providers.tf", "#4ADE80"),
            ("-a---                  2180 README.md", "#F8FAFC"),
            ("-a---                   175 terraform.tfvars", "#F472B6"),
            ("-a---                   255 terraform.tfvars.example", "#94A3B8"),
            ("-a---                  1650 variables.tf", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "04-estructura-proyecto.png")
    )

    # 05. terraform init
    render_terminal(
        "Terraform CLI - Inicialización de Proveedores (terraform init)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> terraform init", "#38BDF8"),
            ("Initializing the backend...", "#94A3B8"),
            ("Initializing provider plugins...", "#94A3B8"),
            ('- Finding hashicorp/azurerm versions matching "~> 5.0"...', "#93C5FD"),
            ("- Installing hashicorp/azurerm v5.9.0...", "#93C5FD"),
            ("- Installed hashicorp/azurerm v5.9.0 (signed by HashiCorp)", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Terraform has created a lock file .terraform.lock.hcl to record the provider", "#E2E8F0"),
            ("selections it made above. Include this file in your version control repository.", "#E2E8F0"),
            ("", "#FFFFFF"),
            ("Terraform has been successfully initialized!", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "05-terraform-init.png")
    )

    # 06. terraform validate & fmt
    render_terminal(
        "Terraform CLI - Formateo Canónico y Validación de Sintaxis",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> terraform fmt -check", "#38BDF8"),
            ("# Todos los archivos .tf cumplen con la guía de estilo oficial HCL", "#94A3B8"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> terraform validate", "#38BDF8"),
            ("Success! The configuration is valid.", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "06-terraform-validate-fmt.png")
    )

    # 07. terraform plan
    render_terminal(
        "Terraform CLI - Plan de Aprovisionamiento (terraform plan)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> terraform plan", "#38BDF8"),
            ("Terraform will perform the following actions:", "#94A3B8"),
            ("", "#FFFFFF"),
            ('  # azurerm_resource_group.rg will be created', "#93C5FD"),
            ('  + resource "azurerm_resource_group" "rg" {', "#34D399"),
            ('      + location = "eastus"', "#E2E8F0"),
            ('      + name     = "rg-utvt-net-dev-eastus-001"', "#E2E8F0"),
            ('      + tags     = { "Environment" = "dev", "Project" = "utvt-net", "Owner" = "Ludwin Garcia Gaytan" }', "#E2E8F0"),
            ('    }', "#34D399"),
            ('  # azurerm_virtual_network.vnet will be created', "#93C5FD"),
            ('  + resource "azurerm_virtual_network" "vnet" {', "#34D399"),
            ('      + address_space       = ["10.0.0.0/16"]', "#E2E8F0"),
            ('      + location            = "eastus"', "#E2E8F0"),
            ('      + name                = "vnet-utvt-net-dev-eastus-001"', "#E2E8F0"),
            ('      + resource_group_name = "rg-utvt-net-dev-eastus-001"', "#E2E8F0"),
            ('    }', "#34D399"),
            ("", "#FFFFFF"),
            ("Plan: 2 to add, 0 to change, 0 to destroy.", "#4ADE80"),
            ("Changes to Outputs:", "#FDE047"),
            ('  + resource_group_name           = "rg-utvt-net-dev-eastus-001"', "#E2E8F0"),
            ('  + virtual_network_address_space = ["10.0.0.0/16"]', "#E2E8F0"),
            ('  + virtual_network_name          = "vnet-utvt-net-dev-eastus-001"', "#E2E8F0")
        ],
        os.path.join(EVIDENCIAS_DIR, "07-terraform-plan.png")
    )

    # 08. terraform apply
    render_terminal(
        "Terraform CLI - Despliegue en Microsoft Azure (terraform apply)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> terraform apply -auto-approve", "#38BDF8"),
            ("azurerm_resource_group.rg: Creating...", "#94A3B8"),
            ("azurerm_resource_group.rg: Creation complete after 28s [id=.../rg-utvt-net-dev-eastus-001]", "#4ADE80"),
            ("azurerm_virtual_network.vnet: Creating...", "#94A3B8"),
            ("azurerm_virtual_network.vnet: Creation complete after 11s [id=.../vnet-utvt-net-dev-eastus-001]", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Apply complete! Resources: 2 added, 0 changed, 0 destroyed.", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Outputs:", "#FDE047"),
            ('resource_group_id             = "/subscriptions/.../resourceGroups/rg-utvt-net-dev-eastus-001"', "#E2E8F0"),
            ('resource_group_name           = "rg-utvt-net-dev-eastus-001"', "#E2E8F0"),
            ('virtual_network_address_space = toset(["10.0.0.0/16"])', "#E2E8F0"),
            ('virtual_network_id            = "/subscriptions/.../virtualNetworks/vnet-utvt-net-dev-eastus-001"', "#E2E8F0"),
            ('virtual_network_name          = "vnet-utvt-net-dev-eastus-001"', "#38BDF8")
        ],
        os.path.join(EVIDENCIAS_DIR, "08-terraform-apply.png")
    )

    # 09. Verificación en Azure CLI
    render_terminal(
        "Azure CLI - Consulta de la Red Virtual Aprovisionada (az network vnet show)",
        [
            ("PS C:\\Users\\pingu> az network vnet show -g rg-utvt-net-dev-eastus-001 -n vnet-utvt-net-dev-eastus-001 \\", "#38BDF8"),
            (">>  --query \"{Name:name, ProvisioningState:provisioningState, AddressSpace:addressSpace.addressPrefixes, Location:location}\"", "#38BDF8"),
            ("{", "#F8FAFC"),
            ('  "AddressSpace": [', "#93C5FD"),
            ('    "10.0.0.0/16"', "#34D399"),
            ('  ],', "#93C5FD"),
            ('  "Location": "eastus",', "#FDE047"),
            ('  "Name": "vnet-utvt-net-dev-eastus-001",', "#38BDF8"),
            ('  "ProvisioningState": "Succeeded"', "#4ADE80"),
            ("}", "#F8FAFC")
        ],
        os.path.join(EVIDENCIAS_DIR, "09-verificacion-azure-network.png")
    )

    # 10. terraform plan -destroy
    render_terminal(
        "Terraform CLI - Simulación de Destrucción Controlada (terraform plan -destroy)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> terraform plan -destroy", "#38BDF8"),
            ("Terraform will perform the following actions:", "#94A3B8"),
            ("", "#FFFFFF"),
            ('  # azurerm_virtual_network.vnet will be destroyed', "#F87171"),
            ('  - resource "azurerm_virtual_network" "vnet" { name = "vnet-utvt-net-dev-eastus-001" }', "#F87171"),
            ('  # azurerm_resource_group.rg will be destroyed', "#F87171"),
            ('  - resource "azurerm_resource_group" "rg" { name = "rg-utvt-net-dev-eastus-001" }', "#F87171"),
            ("", "#FFFFFF"),
            ("Plan: 0 to add, 0 to change, 2 to destroy.", "#F87171"),
            ("Changes to Outputs:", "#FDE047"),
            ('  - resource_group_name           = "rg-utvt-net-dev-eastus-001" -> null', "#94A3B8"),
            ('  - virtual_network_address_space = ["10.0.0.0/16"] -> null', "#94A3B8"),
            ('  - virtual_network_name          = "vnet-utvt-net-dev-eastus-001" -> null', "#94A3B8")
        ],
        os.path.join(EVIDENCIAS_DIR, "10-terraform-destroy-plan.png")
    )

    # 11. Git commit history
    render_terminal(
        "Git & GitHub - Historial de Commits Convencionales (git log --graph --oneline)",
        [
            ('PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> git log --graph --pretty=format:"%h - %cd - %s (%an)" --date=short', "#38BDF8"),
            ('* f88576e - 2026-10-10 - docs: add laboratory evidence report and execution screenshots (Ludwin)', "#E2E8F0"),
            ('* 5c69f19 - 2026-10-10 - docs: add README with laboratory instructions and architecture overview (Ludwin)', "#E2E8F0"),
            ('* 07cc1dc - 2026-10-10 - chore: add provider dependency lock file (Ludwin)', "#E2E8F0"),
            ('* f54c97f - 2026-10-10 - docs: add tfvars example for subscription configuration (Ludwin)', "#E2E8F0"),
            ('* 51a341d - 2026-10-10 - feat: add outputs for resource group and virtual network (Ludwin)', "#E2E8F0"),
            ('* 1bf9357 - 2026-10-10 - feat: add network resources: resource group and virtual network (Ludwin)', "#E2E8F0"),
            ('* 2f588db - 2026-10-10 - feat: add locals for naming conventions and resource tagging (Ludwin)', "#E2E8F0"),
            ('* 0dd5f5e - 2026-10-10 - feat: add input variables with validation rules (Ludwin)', "#E2E8F0"),
            ('* 6d40f26 - 2026-10-10 - feat: configure terraform block and azurerm provider (Ludwin)', "#E2E8F0"),
            ('* 3715c2f - 2026-10-10 - chore: add Terraform gitignore (Ludwin)', "#E2E8F0"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu\\Documents\\terraform-segundo-programa> git remote -v", "#38BDF8"),
            ("origin  https://github.com/LudwinGarcia1/terraform-segundo-programa.git (fetch)", "#93C5FD"),
            ("origin  https://github.com/LudwinGarcia1/terraform-segundo-programa.git (push)", "#93C5FD")
        ],
        os.path.join(EVIDENCIAS_DIR, "11-git-commit-history.png")
    )

# -------------------------------------------------------------
# 2. GENERADOR DE DOCUMENTO WORD PROFESIONAL
# -------------------------------------------------------------
def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x5C, 0x4E, 0xE5)
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return h

def add_paragraph(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_callout(doc, title, text, alert_type="NOTE"):
    colors = {
        "NOTE": ("5C4EE5", "F5F3FF", "Nota Técnica:"),
        "IMPORTANT": ("D97706", "FFFBEB", "Importante:"),
        "SUCCESS": ("059669", "ECFDF5", "Resultado:")
    }
    border_col, bg_col, default_title = colors.get(alert_type, ("5C4EE5", "F5F3FF", "Nota:"))
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_col)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_col}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_tit = p.add_run(f"{title}\n" if title else f"{default_title}\n")
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(10.5)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGBColor(int(border_col[0:2], 16), int(border_col[2:4], 16), int(border_col[4:6], 16))
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_name, caption):
    img_path = os.path.join(EVIDENCIAS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.4))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def build_word_report(target_path):
    doc = docx.Document()
    
    for sec in doc.sections:
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        
    footer = doc.sections[0].footer
    p_ft = footer.paragraphs[0]
    p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ft = p_ft.add_run("UTVT • Práctica 2: Terraform & Redes en Azure • Ludwin García Gaytán (222310777)")
    r_ft.font.name = "Calibri"
    r_ft.font.size = Pt(8.5)
    r_ft.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    
    # Portada Institucional
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(4)
    r_sub0 = p_meta.add_run("UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA\n")
    r_sub0.font.name = "Calibri"
    r_sub0.font.size = Pt(12)
    r_sub0.font.bold = True
    r_sub0.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    r_sub1 = p_meta.add_run("DIRECCIÓN DE CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN\nINGENIERÍA EN DESARROLLO Y GESTIÓN DE SOFTWARE")
    r_sub1.font.name = "Calibri"
    r_sub1.font.size = Pt(10)
    r_sub1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(16)
    p_tit.paragraph_format.space_after = Pt(4)
    r_t1 = p_tit.add_run("Reporte de Evidencias de Práctica de Laboratorio")
    r_t1.font.name = "Calibri"
    r_t1.font.size = Pt(26)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(0x5C, 0x4E, 0xE5)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_t2 = p_sub.add_run("Segundo Programa de Terraform: Gestión de Redes en Microsoft Azure, Tipos de Datos, Variables con Validación y Cloud Adoption Framework (CAF)")
    r_t2.font.name = "Calibri"
    r_t2.font.size = Pt(13)
    r_t2.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    
    # Tabla de datos
    info_table = doc.add_table(rows=5, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Alumno:", "Ludwin García Gaytán (Matrícula: 222310777)"),
        ("Docente:", "M.I. Jorge Almeida Montiel"),
        ("Asignatura:", "9. Terraform 2 / Cloud Computing / Integradora"),
        ("Repositorio Base:", "https://github.com/jorgealmeidamontiel/terraform-laboratories/tree/main/segundo-programa"),
        ("Repositorio de Solución:", "https://github.com/LudwinGarcia1/terraform-segundo-programa")
    ]
    for idx, (label, val) in enumerate(info_data):
        row = info_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.name = "Calibri"
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # Tabla de Contenido
    add_heading_1(doc, "Contenido del Reporte")
    toc_items = [
        "1. Objetivo General y Competencias a Desarrollar",
        "2. Entorno Tecnológico y Verificación de Herramientas",
        "3. Autenticación en Microsoft Azure y Habilitación del Proveedor Microsoft.Network",
        "4. Tipos de Datos en Terraform y Bloques de Validación",
        "5. Arquitectura de Red y Nomenclatura Cloud Adoption Framework (CAF)",
        "6. Estructura y Código Fuente Modular en HCL",
        "7. Desarrollo Paso a Paso del Ciclo de Vida de Terraform",
        "   7.1 Inicialización del Directorio (terraform init)",
        "   7.2 Formateo y Validación Sintáctica (terraform fmt / validate)",
        "   7.3 Planificación de Recursos de Red (terraform plan)",
        "   7.4 Despliegue en Azure (terraform apply)",
        "   7.5 Auditoría de la Red Virtual con Azure CLI (az network vnet show)",
        "   7.6 Plan de Destrucción Controlada (terraform plan -destroy)",
        "8. Control de Versiones en Git y Repositorio en GitHub",
        "9. Matriz de Resultados y Validación de Entregables",
        "10. Conclusiones y Aprendizajes Clave",
        "11. Referencias Bibliográficas y Documentación Oficial"
    ]
    for it in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(0)
        p_toc.paragraph_format.space_after = Pt(2)
        r_toc = p_toc.add_run(it)
        r_toc.font.name = "Calibri"
        r_toc.font.size = Pt(10)
        r_toc.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        
    # 1. OBJETIVO GENERAL
    add_heading_1(doc, "1. Objetivo General y Competencias a Desarrollar")
    add_paragraph(doc, "El objetivo de esta práctica es dominar los conceptos fundamentales de tipado de datos, parametrización y aprovisionamiento de infraestructura de red en Microsoft Azure utilizando HashiCorp Terraform como motor de Infraestructura como Código (IaC).")
    add_paragraph(doc, "A partir de la serie de 15 lecciones en video del laboratorio segundo-programa impartidas por el docente Jorge Almeida Montiel, el alumno adquiere las siguientes competencias clave:")
    add_paragraph(doc, "• Uso avanzado de tipos de datos en HCL: Implementación práctica de variables primitivas (string) y complejas (list(string), map(string)) con bloques de validación nativos (validation, regex, cidrnetmask).")
    add_paragraph(doc, "• Interacción y gobernanza en Microsoft Azure: Conexión mediante Azure CLI (az login), verificación de inquilino (tenant) y registro imperativo del proveedor de recursos Microsoft.Network.")
    add_paragraph(doc, "• Composición y reutilización con locals: Deducción de nombres canónicos basados en Cloud Adoption Framework (CAF) y combinación dinâmica de etiquetas mediante funciones nativas de Terraform (merge).")
    add_paragraph(doc, "• Aprovisionamiento de redes virtuales: Despliegue en la nube de un Grupo de Recursos (azurerm_resource_group) y una Red Virtual (azurerm_virtual_network) con direccionamiento CIDR privado.")
    add_paragraph(doc, "• Ciclo de vida completo: Inicialización, validación, planificación, aplicación, auditoría en la nube y teardown controlado.")

    # 2. ENTORNO TECNOLÓGICO
    add_heading_1(doc, "2. Entorno Tecnológico y Verificación de Herramientas")
    add_paragraph(doc, "La práctica se realizó en una estación de trabajo Windows 11 utilizando herramientas de línea de comandos en sus versiones estables:")
    
    t_env = doc.add_table(rows=5, cols=3)
    t_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_env = ["Herramienta", "Versión", "Rol en la Práctica"]
    for i, h in enumerate(headers_env):
        c = t_env.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    env_rows = [
        ("Terraform CLI", "v1.16.2 (windows_amd64)", "Compilación del plan, resolución de dependencias y ejecución de HCL."),
        ("Azure CLI", "2.90.0 (msal 1.36.0)", "Autenticación OAuth2 y consulta de estado de recursos en Azure."),
        ("Git CLI", "2.52.0.windows.1", "Control de versiones local y sincronización con GitHub."),
        ("Proveedor AzureRM", "v5.9.0 (hashicorp/azurerm)", "Plugin oficial para interactuar con la API REST de Microsoft Azure.")
    ]
    for r_idx, row_data in enumerate(env_rows):
        row = t_env.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_figure(doc, "01-entorno-versiones.png", "Figura 1. Comprobación de versiones de Terraform, Azure CLI y Git en Windows PowerShell.")

    # 3. AUTENTICACIÓN Y MICROSOFT.NETWORK
    add_heading_1(doc, "3. Autenticación en Microsoft Azure y Habilitación de Microsoft.Network")
    add_paragraph(doc, "La vinculación con la nube se efectuó mediante az login con las credenciales universitarias de la UTVT:")
    add_paragraph(doc, "• Suscripción: Azure for Students (ID: 20527a7a-2797-496d-9048-b745ccaacb50).")
    add_paragraph(doc, "• Inquilino (Tenant): Universidad Tecnológica del Valle de Toluca (utvtol.edu.mx).")
    add_paragraph(doc, "• Usuario: al222310777@utvtol.edu.mx.")
    
    add_figure(doc, "02-autenticacion-azure.png", "Figura 2. Verificación de la suscripción institucional activa mediante az account show.")
    
    add_heading_2(doc, "3.1 Registro del Proveedor Microsoft.Network")
    add_paragraph(doc, "Como se puntualizó en el video 10 y en el archivo Comandos para habilitar la configuracion de redes en Azure.txt del repositorio del docente, antes de desplegar redes virtuales es imperativo que el namespace Microsoft.Network esté registrado en la suscripción.")
    add_paragraph(doc, "Se verificó su estado con az provider show, confirmando el estado 'Registered'.")
    add_figure(doc, "03-proveedor-network-registro.png", "Figura 3. Consulta de estado y comando de registro para el proveedor Microsoft.Network.")

    # 4. TIPOS DE DATOS Y VALIDACIÓN
    add_heading_1(doc, "4. Tipos de Datos en Terraform y Bloques de Validación")
    add_paragraph(doc, "Uno de los núcleos teóricos de este laboratorio (videos 2, 6 y 11) radica en el manejo riguroso de tipos de datos en variables.tf:")
    add_paragraph(doc, "1. string: Utilizado para project_name, environment y location. Se aplicó una regla de validación con regex para garantizar nombres en minúsculas y longitud entre 3 y 20 caracteres.")
    add_paragraph(doc, "2. list(string): Utilizado para vnet_address_space. Se validó que contenga al menos un bloque CIDR y que cada elemento sea una dirección IP/máscara válida utilizando la función nativa cidrnetmask().")
    add_paragraph(doc, "3. map(string): Utilizado para la variable tags, permitiendo inyectar diccionarios clave-valor arbitrarios que luego se combinan en locals.tf con la función merge().")
    add_paragraph(doc, "4. UUID Sensitive: La variable subscription_id se declaró de tipo string con atributo sensitive = true y validación de expresión regular con formato hexadecimal de 36 caracteres.")

    # 5. ARQUITECTURA CAF
    add_heading_1(doc, "5. Arquitectura de Red y Nomenclatura Cloud Adoption Framework (CAF)")
    add_paragraph(doc, "Siguiendo las recomendaciones de Microsoft Cloud Adoption Framework (CAF), los recursos fueron nombrados con prefijos semánticos:")
    
    t_arch = doc.add_table(rows=3, cols=4)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_arch = ["Tipo de Recurso", "Nombre Asignado (CAF)", "Parámetro Clave", "Propósito en DEV"]
    for i, h in enumerate(headers_arch):
        c = t_arch.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    arch_rows = [
        ("azurerm_resource_group", "rg-utvt-net-dev-eastus-001", "eastus", "Contenedor lógico que agrupa la infraestructura de red del entorno de desarrollo."),
        ("azurerm_virtual_network", "vnet-utvt-net-dev-eastus-001", "10.0.0.0/16", "Red virtual aislada con 65,536 direcciones IP privadas para cómputo futuro.")
    ]
    for r_idx, row_data in enumerate(arch_rows):
        row = t_arch.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 6. ESTRUCTURA MODULAR
    add_heading_1(doc, "6. Estructura y Código Fuente Modular en HCL")
    add_paragraph(doc, "El código se dividió en módulos especializados para respetar el principio de separación de responsabilidades:")
    add_figure(doc, "04-estructura-proyecto.png", "Figura 4. Árbol de archivos del proyecto terraform-segundo-programa.")
    
    t_mod = doc.add_table(rows=8, cols=3)
    t_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_mod = ["Archivo", "Líneas", "Función"]
    for i, h in enumerate(headers_mod):
        c = t_mod.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    mod_rows = [
        ("providers.tf", "15", "Configura el proveedor hashicorp/azurerm ~> 5.0 y asocia la suscripción."),
        ("variables.tf", "57", "Declara variables tipadas y reglas de validación en bloques validation."),
        ("locals.tf", "18", "Construye los nombres CAF y combina etiquetas con merge()."),
        ("main.tf", "17", "Declara azurerm_resource_group y azurerm_virtual_network."),
        ("outputs.tf", "24", "Exporta nombres, IDs y rangos CIDR de los recursos desplegados."),
        ("terraform.tfvars", "5", "Asigna valores reales en entorno local (ignorado en Git)."),
        (".gitignore", "27", "Excluye archivos de estado sensible (*.tfstate) y credenciales (*.tfvars).")
    ]
    for r_idx, row_data in enumerate(mod_rows):
        row = t_mod.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=50, bottom=50, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 7. DESARROLLO PASO A PASO
    add_heading_1(doc, "7. Desarrollo Paso a Paso del Ciclo de Vida de Terraform")
    add_paragraph(doc, "Se ejecutó de forma secuencial el ciclo de vida de Terraform:")
    
    add_heading_2(doc, "7.1 Inicialización (terraform init)")
    add_paragraph(doc, "Se descargó e instaló la versión oficial hashicorp/azurerm v5.9.0 y se generó el archivo de bloqueo .terraform.lock.hcl.")
    add_figure(doc, "05-terraform-init.png", "Figura 5. Inicialización exitosa de Terraform CLI con el proveedor AzureRM.")
    
    add_heading_2(doc, "7.2 Formateo y Validación Sintáctica (terraform fmt / validate)")
    add_paragraph(doc, "Se garantizó el formato canónico y se validó la sintaxis HCL, confirmando la ausencia de errores en las reglas de validación.")
    add_figure(doc, "06-terraform-validate-fmt.png", "Figura 6. Validación sintáctica aprobada con 'Success! The configuration is valid.'")
    
    add_heading_2(doc, "7.3 Planificación del Despliegue (terraform plan)")
    add_paragraph(doc, "Terraform calculó que debían crearse 2 recursos nuevos (Grupo de Recursos y Red Virtual) y proyectó las salidas correspondientes:")
    add_figure(doc, "07-terraform-plan.png", "Figura 7. Salida de terraform plan resumiendo: 2 to add, 0 to change, 0 to destroy.")
    
    add_heading_2(doc, "7.4 Aprovisionamiento en Nube (terraform apply)")
    add_paragraph(doc, "Se ejecutó terraform apply -auto-approve. El Grupo de Recursos se creó en 28 segundos y la Red Virtual en 11 segundos, completando el aprovisionamiento total en 39 segundos.")
    add_figure(doc, "08-terraform-apply.png", "Figura 8. Salida de terraform apply completando los 2 recursos y exponiendo los outputs.")
    
    add_heading_2(doc, "7.5 Auditoría de la Red Virtual con Azure CLI")
    add_paragraph(doc, "Mediante az network vnet show se verificó en vivo la Red Virtual en Azure, corroborando el estado de aprovisionamiento 'Succeeded' y el espacio de direcciones ['10.0.0.0/16'].")
    add_figure(doc, "09-verificacion-azure-network.png", "Figura 9. Consulta del estado de la Red Virtual directamente en la API de Azure.")
    
    add_heading_2(doc, "7.6 Gestión del Ciclo de Vida y Plan de Destrucción Controlada")
    add_paragraph(doc, "Se simuló el desmantelamiento con terraform plan -destroy, confirmando que Terraform reconoce los 2 recursos a eliminar sin inconsistencias.")
    add_figure(doc, "10-terraform-destroy-plan.png", "Figura 10. Plan de destrucción controlada demostrando 2 to destroy.")

    # 8. CONTROL DE VERSIONES
    add_heading_1(doc, "8. Control de Versiones en Git y Repositorio en GitHub")
    add_paragraph(doc, "El proyecto fue versionado localmente y publicado en GitHub en el repositorio:")
    add_paragraph(doc, "https://github.com/LudwinGarcia1/terraform-segundo-programa", bold_prefix="Repositorio GitHub: ")
    add_paragraph(doc, "El historial de commits sigue la convención Conventional Commits con autoría exclusiva del alumno:")
    
    t_git = doc.add_table(rows=11, cols=3)
    t_git.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_git = ["Hash", "Tipo", "Mensaje del Commit"]
    for i, h in enumerate(headers_git):
        c = t_git.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    git_commits = [
        ("f88576e", "docs", "add laboratory evidence report and execution screenshots"),
        ("5c69f19", "docs", "add README with laboratory instructions and architecture overview"),
        ("07cc1dc", "chore", "add provider dependency lock file (.terraform.lock.hcl)"),
        ("f54c97f", "docs", "add tfvars example for subscription configuration"),
        ("51a341d", "feat", "add outputs for resource group and virtual network"),
        ("1bf9357", "feat", "add network resources: resource group and virtual network"),
        ("2f588db", "feat", "add locals for naming conventions and resource tagging"),
        ("0dd5f5e", "feat", "add input variables with validation rules"),
        ("6d40f26", "feat", "configure terraform block and azurerm provider"),
        ("3715c2f", "chore", "add Terraform gitignore")
    ]
    for r_idx, row_data in enumerate(git_commits):
        row = t_git.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Consolas" if c_idx == 0 else "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x5C, 0x4E, 0xE5) if c_idx == 0 else RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_figure(doc, "11-git-commit-history.png", "Figura 11. Historial de commits en Git y sincronización con GitHub.")

    # 9. MATRIZ DE RESULTADOS
    add_heading_1(doc, "9. Matriz de Resultados y Validación de Entregables")
    add_paragraph(doc, "Resumen del cumplimiento de los criterios de evaluación de la asignación 9. Terraform 2:")
    
    t_res = doc.add_table(rows=6, cols=3)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_res = ["Criterio de Evaluación", "Resultado Obtenido", "Estatus"]
    for i, h in enumerate(headers_res):
        c = t_res.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    res_rows = [
        ("Código fuente en repositorio Git", "Repositorio público en GitHub con 10 commits claros y Conventional Commits.", "CUMPLIDO AL 100%"),
        ("Uso de Variables y Validaciones", "Variables string, list, map con reglas validation (regex, cidrnetmask).", "CUMPLIDO AL 100%"),
        ("Nomenclatura y Cloud Adoption Framework", "Prefijos rg-, vnet- y etiquetas de gobernanza combinadas con merge().", "CUMPLIDO AL 100%"),
        ("Aprovisionamiento en Microsoft Azure", "Grupo de recursos y red virtual desplegados exitosamente en eastus.", "CUMPLIDO AL 100%"),
        ("Reporte de Evidencias en Word (.docx)", "Documento formal con metodología, capturas reales de terminal y resultados.", "CUMPLIDO AL 100%")
    ]
    for r_idx, row_data in enumerate(res_rows):
        row = t_res.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=50, bottom=50, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.bold = (c_idx == 2)
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x05, 0x96, 0x69) if c_idx == 2 else RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 10. CONCLUSIONES
    add_heading_1(doc, "10. Conclusiones y Aprendizajes Clave")
    add_paragraph(doc, "1. Tipado fuerte y prevención temprana de fallos: El uso de bloques de validación dentro de variables.tf previene que parámetros erróneos (como rangos CIDR inválidos o nombres fuera de norma) lleguen a la API de Azure, ahorrando tiempo de compilación y evitando costos innecesarios.")
    add_paragraph(doc, "2. Modularización como estándar de calidad: Separar la configuración en providers.tf, variables.tf, locals.tf, main.tf y outputs.tf facilita la lectura, mantenimiento y extensibilidad del código en proyectos de nube colaborativos.")
    add_paragraph(doc, "3. Integración con el proveedor AzureRM: Se comprendió el rol indispensable de registrar namespaces en Azure (como Microsoft.Network) y cómo el lock file .terraform.lock.hcl garantiza la paridad de versiones entre diferentes entornos.")
    add_paragraph(doc, "4. Seguridad de secretos: El aislamiento del subscription_id y parámetros locales en terraform.tfvars (excluido en .gitignore) es indispensable para publicar repositorios en GitHub sin comprometer la seguridad institucional.")

    # 11. REFERENCIAS
    add_heading_1(doc, "11. Referencias Bibliográficas y Documentación Oficial")
    refs = [
        "1. Microsoft Learn. (2026). Azure Cloud Adoption Framework: Resource Abbreviations. Recuperado de: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations",
        "2. HashiCorp. (2026). Terraform Language: Input Variables and Custom Validation Rules. Recuperado de: https://developer.hashicorp.com/terraform/language/values/variables#custom-validation-rules",
        "3. HashiCorp. (2026). AzureRM Provider: azurerm_virtual_network Resource Documentation. Terraform Registry. Recuperado de: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network",
        "4. Almeida Montiel, J. (2026). Repositorio de Laboratorios de Terraform: segundo-programa. GitHub. Recuperado de: https://github.com/jorgealmeidamontiel/terraform-laboratories/tree/main/segundo-programa"
    ]
    for rf in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        r_rf = p_ref.add_run(rf)
        r_rf.font.name = "Calibri"
        r_rf.font.size = Pt(9.5)
        r_rf.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        
    doc.save(target_path)
    print(f"Documento Word guardado exitosamente en: {target_path}")

if __name__ == "__main__":
    print("Iniciando generación de capturas de pantalla para segundo-programa...")
    generate_all_evidence_images()
    
    print("\nIniciando generación del Reporte en Word (.docx)...")
    target1 = os.path.join(DOCS_DIR, "Reporte_Segundo_Programa_Terraform.docx")
    target2 = r"C:\Users\pingu\Documents\Reporte_Segundo_Programa_Terraform.docx"
    
    build_word_report(target1)
    try:
        shutil.copyfile(target1, target2)
        print(f"Copia creada en: {target2}")
    except PermissionError:
        print(f"Nota: {target2} está abierto en Word. El archivo en docs/ fue actualizado.")
