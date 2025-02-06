from flask import Flask, render_template, request, send_file
from fpdf import FPDF

app = Flask(__name__)

class CustomPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'DESOTO BLOCK LLC', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, '108 S Parker Ave,', 0, 1, 'L')
        self.cell(0, 5, 'Arcadia, FL 34266', 0, 1, 'L')
        self.cell(0, 5, 'Phe@desotoblock.com | 863-244-2407', 0, 1, 'L')
        self.ln(10)

    def add_order_details(self, shipper_id, sales_order_no, order_type, customer_id):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Order Details', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(50, 6, f'Shipper ID: {shipper_id}', 0, 1, 'L')
        self.cell(50, 6, f'Sales Order No.: {sales_order_no}', 0, 1, 'L')
        self.cell(50, 6, f'Order Type: {order_type}', 0, 1, 'L')
        self.cell(50, 6, f'Customer ID: {customer_id}', 0, 1, 'L')
        self.ln(10)

    def add_addresses(self, bill_to, ship_to):
        self.set_font('Arial', 'B', 12)
        self.cell(90, 8, 'Bill To:', 0, 0, 'L')
        self.cell(90, 8, 'Ship To:', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.multi_cell(90, 6, bill_to, 0, 'L')
        x, y = self.get_x(), self.get_y()
        self.set_xy(x + 90, y - (6 * (bill_to.count("\n") + 1)))
        self.multi_cell(90, 6, ship_to, 0, 'L')
        self.ln(10)

    def add_table_headers(self):
        self.set_font('Arial', 'B', 10)
        headers = ["Description", "Sales Person", "Site", "QTY Shipped", "Ship Date"]
        widths = [80, 35, 25, 25, 30]
        for header, width in zip(headers, widths):
            self.cell(width, 8, header, 1, 0, 'C')
        self.ln()

    def add_table_row(self, description, sales_person, site, qty_shipped, ship_date):
        self.set_font('Arial', '', 10)
        y_before = self.get_y()
        desc_width = 80
        line_height = 6
        self.multi_cell(desc_width, line_height, description, 1)
        y_after = self.get_y()
        row_height = y_after - y_before
        self.set_xy(self.get_x() + desc_width, y_before)
        self.cell(35, row_height, sales_person, 1)
        self.cell(25, row_height, site, 1)
        self.cell(25, row_height, qty_shipped, 1)
        self.cell(30, row_height, ship_date, 1)
        self.ln()

    def add_notes(self, order_notes):
        self.set_y(150)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Order Notes:', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, order_notes, 0, 'L')

    def footer(self):
        self.set_y(-40)
        self.set_fill_color(200, 200, 200)
        self.rect(0, self.get_y(), 210, 40, 'F')
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.cell(95, 10, 'Approved by ___________________________', 0, 0, 'L')
        self.cell(100, 10, 'Driver ___________________________', 0, 1, 'R')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
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

    pdf = CustomPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.add_order_details(shipper_id, sales_order_no, order_type, customer_id)
    pdf.add_addresses(bill_to, ship_to)
    pdf.add_table_headers()
    pdf.add_table_row(description, sales_person, site, qty_shipped, ship_date)
    pdf.add_notes(order_notes)

    pdf_file = 'comprobante.pdf'
    pdf.output(pdf_file)
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
