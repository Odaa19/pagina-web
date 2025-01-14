from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Agregar encabezado con bordes
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'TREMORN ARCADIA', border=0, ln=1, align='C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'WE MAKE IT EASY', border=0, ln=1, align='C')
        self.ln(5)  # Salto de línea

    def footer(self):
        # Pie de página con número de página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), align='C')

# Crear el PDF
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Título principal
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, "DRIVER'S COPY", align='C', ln=1)
pdf.ln(5)

# Tabla de información general
pdf.set_font('Arial', '', 10)

# Sección "Bill To" y "Ship To"
pdf.cell(95, 10, 'Bill To:', border=1, ln=0)
pdf.cell(95, 10, 'Ship To:', border=1, ln=1)

pdf.cell(95, 10, 'Windward Building Group', border=1, ln=0)
pdf.cell(95, 10, 'Windward Building Group', border=1, ln=1)

pdf.cell(95, 10, '650 2nd Ave S', border=1, ln=0)
pdf.cell(95, 10, '11465 Brightmore Blvd.', border=1, ln=1)

pdf.cell(95, 10, 'St Petersburg FL 33701', border=1, ln=0)
pdf.cell(95, 10, 'North Port FL 34293', border=1, ln=1)
pdf.ln(10)

# Detalles adicionales
pdf.cell(95, 10, 'Contact: Scott Carpenter', border=1, ln=0)
pdf.cell(95, 10, 'Total Weight: 34,299 LB', border=1, ln=1)
pdf.ln(5)

# Tabla de productos
pdf.set_font('Arial', 'B', 10)
pdf.cell(20, 10, 'Qty', border=1, align='C')
pdf.cell(80, 10, 'Description', border=1, align='C')
pdf.cell(40, 10, 'Cubes', border=1, align='C')
pdf.cell(50, 10, 'Dimensions', border=1, ln=1, align='C')

# Productos (puedes añadir más filas)
pdf.set_font('Arial', '', 10)
pdf.cell(20, 10, '15', border=1, align='C')
pdf.cell(80, 10, 'Park Plaza 12x12 2 3/8"', border=1)
pdf.cell(40, 10, '11.00', border=1, align='C')
pdf.cell(50, 10, '1320 SF', border=1, ln=1, align='C')

pdf.ln(10)

# Información de envío
pdf.cell(95, 10, 'Freight Charge: 0060', border=1, ln=0)
pdf.cell(95, 10, 'Ship Date: 12/16/24', border=1, ln=1)

# Guardar el archivo PDF
pdf.output('comprobante_actualizado.pdf')
