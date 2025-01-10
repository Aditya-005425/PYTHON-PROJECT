import os
import oracledb
from flask import Flask, jsonify, request

app = Flask(__name__)

dsn = os.getenv('DB_DSN', oracledb.makedsn("172.14.7.160", 1521, service_name="XE"))
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'root')

def create_connection():
    try:
        connection = oracledb.connect(user=db_user, password=db_password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        print(f"Error connecting to Oracle DB: {error_obj.message}")
        return None

@app.route('/api/taxpayers', methods=['GET'])
def get_taxpayers():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT TaxPayerID, Name, Email, Phone, Address, TaxIdentificationNumber FROM TaxPayers")
        
        taxpayers = [{'TaxPayerID': row[0], 'Name': row[1], 'Email': row[2], 'Phone': row[3], 'Address': row[4], 'TaxIdentificationNumber': row[5]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"taxpayers": taxpayers})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

@app.route('/api/taxreturns', methods=['GET'])
def get_tax_returns():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT tr.ReturnID, tp.Name, tr.TotalIncome, tr.TaxableIncome, tr.TaxAmount, tr.Status 
            FROM TaxReturns tr
            JOIN TaxPayers tp ON tr.TaxPayerID = tp.TaxPayerID
        """)
        
        tax_returns = [{'ReturnID': row[0], 'TaxPayerName': row[1], 'TotalIncome': row[2], 'TaxableIncome': row[3], 'TaxAmount': row[4], 'Status': row[5]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"tax_returns": tax_returns})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

@app.route('/api/taxreturn', methods=['POST'])
def file_tax_return():
    data = request.get_json()
    tax_payer_id = data.get('tax_payer_id')
    total_income = data.get('total_income')

    if not tax_payer_id or not total_income:
        return jsonify({"error": "TaxPayerID and TotalIncome are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()

        cursor.callproc("FileTaxReturn", [tax_payer_id, total_income])
        connection.commit()

        return jsonify({"message": "Tax return filed successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/taxconsultants', methods=['GET'])
def get_tax_consultants():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT ConsultantID, Name, Email, Phone, Expertise FROM TaxConsultants")
        
        consultants = [{'ConsultantID': row[0], 'Name': row[1], 'Email': row[2], 'Phone': row[3], 'Expertise': row[4]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"consultants": consultants})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

@app.route('/api/assignconsultant', methods=['POST'])
def assign_tax_consultant():
    data = request.get_json()
    tax_payer_id = data.get('tax_payer_id')
    consultant_id = data.get('consultant_id')

    if not tax_payer_id or not consultant_id:
        return jsonify({"error": "TaxPayerID and ConsultantID are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO TaxConsultantAssignments (TaxPayerID, ConsultantID, AssignedDate, Status)
            VALUES (:tax_payer_id, :consultant_id, SYSDATE, 'Active')
        """, [tax_payer_id, consultant_id])
        connection.commit()

        return jsonify({"message": "Consultant assigned successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/taxstatistics', methods=['GET'])
def show_tax_statistics():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.callproc("ShowTaxStatistics")

        return jsonify({"message": "Tax statistics shown in DBMS Output"}), 200
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
