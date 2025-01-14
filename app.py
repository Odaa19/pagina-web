from flask import Flask, render_template, request, send_file
from fpdf import FPDF

app = Flask(__name__)

class CustomPDF(FPDF):
    def header(self):
        # Encabezado con el nombre de la empresa
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'DESOTO BLOCK LLC', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, '108 S Parker Ave,', 0, 1, 'L')
        self.cell(0, 5, 'Arcadia, FL 34266', 0, 1, 'L')
        self.cell(0, 5, 'Phe@desotoblock.com | 863-244-2407', 0, 1, 'L')
        self.ln(10)

    def add_order_details(self, shipper_id, sales_order_no, order_type, customer_id):
        # Sección de detalles del pedido
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Order Details', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(50, 6, f'Shipper ID: {shipper_id}', 0, 1, 'L')
        self.cell(50, 6, f'Sales Order No.: {sales_order_no}', 0, 1, 'L')
        self.cell(50, 6, f'Order Type: {order_type}', 0, 1, 'L')
        self.cell(50, 6, f'Customer ID: {customer_id}', 0, 1, 'L')
        self.ln(10)

    def add_addresses(self, bill_to, ship_to):
        # Secciones "Bill To" y "Ship To"
        self.set_font('Arial', 'B', 12)
        self.cell(90, 8, 'Bill To:', 0, 0, 'L')
        self.cell(90, 8, 'Ship To:', 0, 1, 'L')

        self.set_font('Arial', '', 10)
        self.multi_cell(90, 6, bill_to, 0, 'L')
        x, y = self.get_x(), self.get_y()
        self.set_xy(x + 90, y - (6 * (bill_to.count("\n") + 1)))  # Ajuste de posición para "Ship To"
        self.multi_cell(90, 6, ship_to, 0, 'L')
        self.ln(10)

    def add_table_headers(self):
        # Encabezados de la tabla
        self.set_font('Arial', 'B', 10)
        headers = ["Description", "Sales Person", "Site", "QTY Shipped", "Ship Date", "Ship VIA"]
        widths = [60, 30, 30, 25, 25, 25]
        for header, width in zip(headers, widths):
            self.cell(width, 8, header, 1, 0, 'C')
        self.ln()

    def add_table_row(self, description, sales_person, site, qty_shipped, ship_date, ship_via):
        # Fila de la tabla
        self.set_font('Arial', '', 10)
        self.cell(60, 8, description, 1)
        self.cell(30, 8, sales_person, 1)
        self.cell(30, 8, site, 1)
        self.cell(25, 8, qty_shipped, 1)
        self.cell(25, 8, ship_date, 1)
        self.cell(25, 8, ship_via, 1)
        self.ln()

    def add_notes(self, order_notes):
        # Notas y detalles adicionales
        self.set_y(150)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Order Notes:', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, order_notes, 0, 'L')

    def footer(self):
        # Pie de página con color gris translúcido
        self.set_y(-20)
        self.set_fill_color(200, 200, 200)  # Fondo gris claro
        self.rect(0, self.get_y(), 210, 20, 'DF')  # Usar 'DF' para aplicar relleno y borde
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)  # Texto negro
        self.cell(0, 10, 'Approved by ___________________________', 0, 1, 'L')
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # Datos del formulario
    shipper_id = request.form['shipper_id']
    sales_order_no = request.form['sales_order_no']
    order_type = request.form['order_type']
    customer_id = request.form['customer_id']
    bill_to = request.form['bill_to']
    ship_to = request.form['ship_to']
    order_notes = request.form['order_notes']
    description = request.form['description']
    sales_person = request.form['sales_person']
    site = request.form['site']
    qty_shipped = request.form['qty_shipped']
    ship_date = request.form['ship_date']
    ship_via = request.form['ship_via']

    # Crear el PDF
    pdf = CustomPDF('P', 'mm', 'A4')
    pdf.add_page()

    # Detalles del pedido
    pdf.add_order_details(shipper_id, sales_order_no, order_type, customer_id)

    # Direcciones
    pdf.add_addresses(bill_to, ship_to)

    # Tabla
    pdf.add_table_headers()
    pdf.add_table_row(description, sales_person, site, qty_shipped, ship_date, ship_via)

    # Notas
    pdf.add_notes(order_notes)

    # Guardar el archivo PDF
    pdf_file = 'comprobante.pdf'
    pdf.output(pdf_file)

    # Retornar el archivo para su descarga
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
