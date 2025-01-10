import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
from datetime import date, datetime
from decimal import Decimal
import socket

# MySQL database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "Tax"  # Change this to your actual database name
}

def get_db_connection():
    """Get a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle date, datetime, and Decimal types."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()  
        if isinstance(obj, Decimal):
            return float(obj)  
        return super().default(obj)

class RequestHandler(BaseHTTPRequestHandler):
    """RequestHandler to process GET and POST requests."""
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            if self.path.startswith("/taxpayers/"):
                taxpayer_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM TaxPayers WHERE TaxPayerID = %s", (taxpayer_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/taxrates/"):
                cursor.execute("SELECT * FROM TaxRates")
                result = cursor.fetchall()
            elif self.path.startswith("/taxreturns/"):
                return_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM TaxReturns WHERE TaxReturnID = %s", (return_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/deductions/"):
                deduction_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Deductions WHERE DeductionID = %s", (deduction_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/penalties/"):
                penalty_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Penalties WHERE PenaltyID = %s", (penalty_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/taxconsultants/"):
                consultant_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM TaxConsultants WHERE ConsultantID = %s", (consultant_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/taxconsultantassignments/"):
                assignment_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM TaxConsultantAssignments WHERE AssignmentID = %s", (assignment_id,))
                result = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM TaxPayers")  # Default to fetching all taxpayers
                result = cursor.fetchall()

            response_body = json.dumps(result, cls=CustomJSONEncoder)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

    def do_POST(self):
        """Handle POST requests."""
        cursor = None
        conn = None
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            if self.path.startswith("/taxpayers/"):
                taxpayer_id = data.get("TaxPayerID")
                name = data.get("Name")
                email = data.get("Email")
                phone = data.get("Phone")
                address = data.get("Address")
                tin = data.get("TaxIdentificationNumber")

                if not all([name, email, phone, address, tin]):
                    self.send_error(400, "Missing required fields")
                    return
                
                insert_query = """
                    INSERT INTO TaxPayers (Name, Email, Phone, Address, TaxIdentificationNumber)
                    VALUES (%s, %s, %s, %s, %s)
                """
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(insert_query, (name, email, phone, address, tin))
                conn.commit()

            elif self.path.startswith("/taxrates/"):
                income_bracket = data.get("IncomeBracket")
                rate_percentage = data.get("RatePercentage")

                if not all([income_bracket, rate_percentage]):
                    self.send_error(400, "Missing required fields")
                    return
                
                insert_query = """
                    INSERT INTO TaxRates (IncomeBracket, RatePercentage)
                    VALUES (%s, %s)
                """
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(insert_query, (income_bracket, rate_percentage))
                conn.commit()

            elif self.path.startswith("/taxreturns/"):
                taxpayer_id = data.get("TaxPayerID")
                total_income = data.get("TotalIncome")
                taxable_income = data.get("TaxableIncome")
                tax_amount = data.get("TaxAmount")
                status = data.get("Status")

                if not all([taxpayer_id, total_income, taxable_income, tax_amount, status]):
                    self.send_error(400, "Missing required fields")
                    return
                
                insert_query = """
                    INSERT INTO TaxReturns (TaxPayerID, TotalIncome, TaxableIncome, TaxAmount, Status)
                    VALUES (%s, %s, %s, %s, %s)
                """
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(insert_query, (taxpayer_id, total_income, taxable_income, tax_amount, status))
                conn.commit()

            # Add similar blocks for other tables such as Deductions, Penalties, TaxConsultants, etc.

            self.send_response(201)  # Created
            self.send_header("Content-type", "application/json")
            self.end_headers()

            response = {"message": "Data added successfully"}
            self.wfile.write(json.dumps(response).encode())

        except mysql.connector.Error as db_err:
            self.send_error(500, f"Database error: {str(db_err)}")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    """Run the HTTP server."""
    
    # Check if port is available before starting the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
            s.close()
    except OSError as e:
        print(f"Port {port} is already in use. Please try a different port.")
        return

    server_address = ("", port)
    print(f"Server started at port {port}")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
