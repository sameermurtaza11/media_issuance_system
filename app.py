from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import mysql.connector
import pandas as pd
from io import BytesIO

app = Flask(__name__)
CORS(app)

# DB Config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'media_issuance'
}

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

# Issuance Data Handling Route
@app.route("/api/issuance", methods=["POST"])
def handle_issuance():
    try:
        data = request.get_json()

        required_fields = ['mediaType', 'mediaId', 'recipientName', 'recipientPin',
                           'issueDate', 'issuedByName', 'issuedByPin', 'mediaCategory']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        media_prefix = f"ABC-{data['mediaType']}-"
        formatted_media_id = media_prefix + data['mediaId']

        # Check for existing media_id
        check_query = "SELECT * FROM media_issuance_records WHERE media_id = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(check_query, (formatted_media_id,))
        existing = cursor.fetchone()

        if existing:
            return jsonify({
                'exists': True,
                'message': 'Media already issued. Transfer to new receiver?',
                'existing_id': existing['id'] # type: ignore
            }), 200

        # Insert new record (if not duplicate)
        insert_query = """
            INSERT INTO media_issuance_records 
            (media_type, media_id, recipient_name, recipient_pin, issue_date, 
             issued_by_name, issued_by_pin, media_category, remarks) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            data['mediaType'],
            formatted_media_id,
            data['recipientName'],
            data['recipientPin'],
            data['issueDate'],
            data['issuedByName'],
            data['issuedByPin'],
            data['mediaCategory'],
            data.get('remarks', '')
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/api/transfer", methods=["POST"])
def handle_transfer():
    try:
        data = request.get_json()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        formatted_media_id = f"ABC-{data['mediaType']}-{data['mediaId']}"

        # Update old record's remarks
        update_query = """
            UPDATE media_issuance_records
            SET remarks = CONCAT(IFNULL(remarks, ''), ' | Transferred to new receiver (' , %s, ', ', %s, ')')
            WHERE id = %s
        """
        
        
        cursor.execute(update_query, (
            data['recipientName'],
            data['recipientPin'],
            data['existing_id']
        ))

        # Insert new row for new receiver
        insert_query = """
            INSERT INTO media_issuance_records 
            (media_type, media_id, recipient_name, recipient_pin, issue_date, 
             issued_by_name, issued_by_pin, media_category, remarks) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data['mediaType'],
            formatted_media_id,
            data['recipientName'],
            data['recipientPin'],
            data['issueDate'],
            data['issuedByName'],
            data['issuedByPin'],
            data['mediaCategory'],
            data.get('remarks', '')
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Export to Excel Route
@app.route('/export', methods=['POST', 'OPTIONS'])
def export_data():
    if request.method == "OPTIONS":
        return '', 200  # preflight request allowed

    try:
        data = request.get_json()
        if data.get('username') != ADMIN_USERNAME or data.get('password') != ADMIN_PASSWORD:
            return "Unauthorized: Incorrect credentials", 401

        from_date = data.get('fromDate')
        to_date = data.get('toDate')

        query = "SELECT * FROM media_issuance_records"
        params = []

        if from_date and to_date:
            query += " WHERE issue_date BETWEEN %s AND %s"
            params = [from_date, to_date]

        conn = mysql.connector.connect(**db_config)
        df = pd.read_sql(query, conn, params=params)
        conn.close()

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='media_data.xlsx'
        )
    except Exception as e:
        return str(e), 500


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
