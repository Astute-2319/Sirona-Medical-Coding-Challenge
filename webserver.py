from flask import Flask, request, jsonify
import sqlite3

class myWebpage:
    def __init__(self, host="127.0.0.1", port=5000):
            self.app = Flask(__name__)
            self.host = host
            self.port = port
            self._register_routes()

    def _register_routes(self):
            # Use add_url_rule instead of @app.route decorator
            self.app.add_url_rule("/", "main", self.main, methods=["GET"])
            self.app.add_url_rule("/cases", "cases", self.cases, methods=["GET"])
            self.app.add_url_rule("/cases/<int:id>", "casesID", self.casesID, methods=["GET"])
            self.app.add_url_rule("/cases/<int:id>/claim", "claimCase", self.claimCase, methods=["POST"])
            self.app.add_url_rule("/cases/<int:id>/report", "caseReport", self.caseReport, methods=["POST"])
            self.app.add_url_rule("/employees", "GETemployees", self.GETemployees, methods=["GET"])
            self.app.add_url_rule("/employees", "POSTemployees", self.POSTemployees, methods=["POST"])
            self.app.add_url_rule("/employees/<int:id>", "PUTemployees", self.PUTemployees, methods=["PUT"])
            self.app.add_url_rule("/employees/<int:id>", "DELETEemployees", self.DELETEemployees, methods=["DELETE"])

    def main(self):
           return "This is the main page"

    # Returns a list of all cases that match the filter criteria
    # Ex: http://127.0.0.1:5000/cases?status=IN_PROGRESS&claimedBy=mpeters
    def cases(self):
        status = request.args.get('status')
        claimedBy = request.args.get('claimedBy')

        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        if not status and not claimedBy:
            cases = cursor.execute("SELECT * FROM cases ORDER BY studyDate;")
            output = jsonify(cases.fetchall())

        elif status and not claimedBy:
            cases = cursor.execute("SELECT * FROM cases WHERE status = ? ORDER BY studyDate;", (str(status),))
            output = jsonify(cases.fetchall())

        elif not status and claimedBy:
            cases = cursor.execute("SELECT * FROM cases WHERE claimedBy = ? ORDER BY studyDate;", (str(claimedBy),))
            output = jsonify(cases.fetchall())

        else:
            cases = cursor.execute("SELECT * FROM cases WHERE status = ? AND claimedBy = ? ORDER BY studyDate;", (str(status), str(claimedBy),))
            output = jsonify(cases.fetchall())

        cursor.close()
        conn.close()
        return output

    # Return an entire case based on its ID alone
    # Ex: http://127.0.0.1:5000/cases/1
    def casesID(self, id):
        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        cases = cursor.execute("SELECT * FROM cases WHERE id = ?", (int(id),))
        output = jsonify(cases.fetchall())

        if output.json == []:
            output = f"Case not found"
            return jsonify(output), 404
        else:
            return output

    # Claim a case based on its ID and the username of the employee claiming it. 
    # This will transition the case from PENDING to IN_PROGRESS
    def claimCase(self, id):
        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        try:
            data = request.get_json()
        except Exception:
            return jsonify("Unsupported media type. Input format is not supported or data is missing"), 415

        if not data or not data.get('username'):
            return jsonify("Unsupported media type. Username cannot be empty"), 415

        cursor.execute("SELECT username FROM employees")
        currentUsernames = [row[0] for row in cursor.fetchall()]

        if data['username'] not in currentUsernames:
            return jsonify("That is not a valid employee username"), 415

        cursor.execute("SELECT status FROM cases WHERE id = ?", (int(id),))
        row = cursor.fetchone()

        if row is None:
            return jsonify("Case not found"), 404

        if row[0] != 'PENDING':
            return jsonify("Case is not currently pending review"), 422

        cursor.execute(
            "UPDATE cases SET status = 'IN_PROGRESS', claimedBy = ?, claimedAt = datetime('now') WHERE id = ?",
            (data['username'], int(id))
        )
        conn.commit()

        cursor.execute("SELECT * FROM cases WHERE id = ?", (int(id),))
        updated = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(updated)

    # Submit a report on a case based on its ID and the username of the employee submitting the report. 
    # This will transition the case from IN_PROGRESS to COMPLETED
    def caseReport(self, id):
        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        try:
            data = request.get_json()
        except Exception:
            return jsonify("Unsupported media type. Input format is not supported or data is missing"), 415

        if not data or not data.get('author'):
            return jsonify("Unsupported media type. Author cannot be empty"), 415

        if not data or not data.get('report'):
            return jsonify("Unsupported media type. Report body cannot be empty"), 415

        cursor.execute("SELECT username FROM employees")
        currentUsernames = [row[0] for row in cursor.fetchall()]

        if data['author'] not in currentUsernames:
            return jsonify("Unsupported media type. That is not a valid employee username"), 415

        cursor.execute("SELECT claimedBy FROM cases WHERE id = ?", (id,))
        userClaim = [row[0] for row in cursor.fetchall()]
        if data['author'] not in userClaim:
                return jsonify("Unsupported media type. This user did not claim this case"), 415

        cursor.execute("SELECT status FROM cases WHERE id = ?", (int(id),))
        row = cursor.fetchone()

        if row is None:
            return jsonify("Case not found"), 404

        if row[0] != 'IN_PROGRESS':
            return jsonify("Case is not currently in progress"), 422

        cursor.execute(
                "UPDATE cases SET status = 'COMPLETED', report = ? WHERE id = ?",
                (data['report'], int(id))
        )
        conn.commit()

        cursor.execute("SELECT * FROM cases WHERE id = ?", (int(id),))
        updated = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(updated)

    # Returns a list of all employees in the database
    def GETemployees(self):
        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        employees = cursor.execute("SELECT * FROM employees;")
        output = jsonify(employees.fetchall())

        return output

    # Add a new employee to the database based on the provided username
    def POSTemployees(self):
        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        data = request.get_json()

        cursor.execute("INSERT INTO employees (username) VALUES (?)", (data['username'],))

        conn.commit()

        employees = cursor.execute("SELECT * FROM employees;")
        output = jsonify(employees.fetchall())
        cursor.close()
        conn.close()

        return output

    # Update an existing employee's username based on their ID and the new username provided
    def PUTemployees(self, id):
        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        try:
            data = request.get_json()
        except:
            output = f"Unsupported media type. Input format is not supported or data is missing"
            return jsonify(output), 415

        if data['username'] == '':
            output = f"Unsupported media type. Username cannot be empty"
            return jsonify(output), 415

        currentUsernames = jsonify(cursor.execute("SELECT username FROM employees").fetchall()).json
        for name in currentUsernames:
            if data['username'] == name[0]:
                output = f"Unprocessable content. Username {data['username']} is already in use"
                return jsonify(output), 422

        checkEmployee = cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))

        if jsonify(checkEmployee.fetchall()) != []:
            output = f"Unprocessable content. ID {id} is not a valid employee ID"
            return jsonify(output), 422

        cursor.execute("UPDATE employees SET username = (?) WHERE id = ?", (data['username'], id))
        conn.commit()

        employees = cursor.execute("SELECT * FROM employees;")
        output = jsonify(employees.fetchall())
        cursor.close()
        conn.close()

        return output

    # Delete an existing employee from the database based on their ID
    def DELETEemployees(self, id):
        conn = sqlite3.connect('Challenge_DB.db')
        cursor = conn.cursor()

        checkEmployee = cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))

        if jsonify(checkEmployee.fetchall()).json != []:
             cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
             conn.commit()
        else:
            output = f"Unprocessable content. ID {id} is not a valid employee ID"
            return jsonify(output), 422

        employees = cursor.execute("SELECT * FROM employees;")
        output = jsonify(employees.fetchall())
        cursor.close()
        conn.close()
        
        return output

    # Run the server on the specified host and port, with optional debug mode
    def run(self, debug=False):
            self.app.run(host=self.host, port=self.port, debug=debug)



if __name__ == "__main__":
    webpage = myWebpage()
    webpage.run(debug=False)