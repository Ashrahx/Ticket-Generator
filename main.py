import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import pymysql

def connect_to_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='*****',
        database='turns',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def generate_ticket_number():
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # Conecta a la base de datos
    connection = connect_to_database()

    try:
        # Obtiene el último número de ticket generado
        with connection.cursor() as cursor:
            cursor.execute('SELECT MAX(ticket_number) AS last_ticket_number FROM tickets')
            result = cursor.fetchone()
            last_ticket_number = result['last_ticket_number'] or 0
    
        # Incrementa el número de ticket en 1
        new_ticket_number = last_ticket_number + 1

        # Guarda el nuevo número de ticket en la base de datos
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO tickets (ticket_number) VALUES (%s)', (new_ticket_number,))
        connection.commit()

        # Crea el número de ticket con el formato adecuado
        ticket_number = f"UAL-{current_date}-{str(new_ticket_number).zfill(3)}"
      
        return ticket_number

    finally:
        # Cierra la conexión a la base de datos en caso de errores
        connection.close()

def generate_ticket_pdf(ticket_number):
    try:
        file_name = f"C:\\Users\\Elfud\\Desktop\\Ticket-Generator\\tickets\\tickets.pdf"
        pdf_file = canvas.Canvas(file_name, pagesize=letter)
        pdf_file.setFont("Helvetica", 12)
        pdf_file.setPageSize((5.65 * inch, 7.26 * inch))
        pdf_file.drawString(0.5 * inch, 1.5 * inch, "Folio:")
        pdf_file.drawString(1.5 * inch, 1.5 * inch, ticket_number)
        pdf_file.save()
        print(f"Archivo PDF del ticket {ticket_number} generado exitosamente.")
    except Exception as e:
        print(f"Error al generar el archivo PDF del ticket: {e}")

# Genera un nuevo número de ticket
ticket_number = generate_ticket_number()

# Genera el archivo PDF del ticket
generate_ticket_pdf(ticket_number)

print(f"Ticket generado con el número: {ticket_number}")
