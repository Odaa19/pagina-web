from fpdf import FPDF
from pdfrw import PageMerge, PdfReader, PdfWriter

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Comprobante Editable', border=0, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), align='C')

def create_pdf_template(output_path):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Arial', '', 12)

    # Campos del formulario
    pdf.cell(50, 10, 'Bill To:', border=0)
    pdf.cell(0, 10, '', border=1, ln=1)

    pdf.cell(50, 10, 'Ship To:', border=0)
    pdf.cell(0, 10, '', border=1, ln=1)

    pdf.ln(10)

    pdf.cell(20, 10, 'Qty', border=1, align='C')
    pdf.cell(80, 10, 'Description', border=1, align='C')
    pdf.cell(40, 10, 'Cubes', border=1, align='C')
    pdf.cell(50, 10, 'Dimensions', border=1, ln=1, align='C')

    pdf.cell(20, 10, '', border=1)  # Qty (editable)
    pdf.cell(80, 10, '', border=1)  # Description (editable)
    pdf.cell(40, 10, '', border=1)  # Cubes (editable)
    pdf.cell(50, 10, '', border=1, ln=1)  # Dimensions (editable)

    pdf.output(output_path)

def add_form_fields(input_pdf, output_pdf):
    template = PdfReader(input_pdf)
    annotations = [
        {'field_name': 'bill_to', 'rect': [80, 760, 300, 780]},
        {'field_name': 'ship_to', 'rect': [80, 740, 300, 760]},
        {'field_name': 'qty', 'rect': [50, 700, 70, 720]},
        {'field_name': 'description', 'rect': [100, 700, 250, 720]},
        {'field_name': 'cubes', 'rect': [260, 700, 320, 720]},
        {'field_name': 'dimensions', 'rect': [340, 700, 400, 720]},
    ]

    for annotation in annotations:
        page = template.pages[0]
        widget = PageMerge().add(page, viewrect=annotation['rect'])[0]
        widget.AA = annotation['field_name']

    PdfWriter(output_pdf, trailer=template).write()

if __name__ == '__main__':
    create_pdf_template('template.pdf')
    add_form_fields('template.pdf', 'comprobante_editable.pdf')
