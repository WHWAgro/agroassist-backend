from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import json

# Create a PDF document
doc = SimpleDocTemplate("orden_de_compra.pdf", pagesize=letter)

# Create a list to hold the content of the PDF
pdf_content = []

# Section 1: Title
title_style = getSampleStyleSheet()["Title"]
title = Paragraph("Orden de Compra", title_style)
pdf_content.append(title)

# Section 2: Information in Two Columns
# Load JSON data (replace this with your actual JSON data)
json_data = {
    "rut": "123456789",
    "direccion": "123 Main Street",
    "comuna": "City",
    "telefono": "555-555-5555",
    "enviar_a": "John Doe"
}

# Create a table with two columns
info_table_data = [
    ["RUT:", json_data["rut"], "Teléfono:", json_data["telefono"]],
    ["Dirección:", json_data["direccion"], "Enviar a:", json_data["enviar_a"]],
    ["Comuna:", json_data["comuna"]]
]

info_table = Table(info_table_data, colWidths=[80, 150, 80, 150])
info_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                               ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
info_table.setStyle(info_table_style)
pdf_content.append(info_table)

# Section 3: Table with Product Names and Prices
# Replace this with your actual product data (a list of dictionaries)
product_data = [
    {"name": "Product 1", "price": 100},
    {"name": "Product 2", "price": 200},
    {"name": "Product 3", "price": 150}
]

# Create a table for product data
product_table_data = [["Product Name", "Price"]]
total_price = 0
for product in product_data:
    product_table_data.append([product["name"], f"${product['price']}"])
    total_price += product["price"]

product_table = Table(product_table_data, colWidths=[300, 80])
pdf_content.append(product_table)

# Add the total price
pdf_content.append(Paragraph(f"Total: ${total_price}", title_style))

# Build the PDF document
doc.build(pdf_content)