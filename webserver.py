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

    def main(self):
           return "This is the main page"

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

    def run(self, debug=False):
            self.app.run(host=self.host, port=self.port, debug=debug)



if __name__ == "__main__":
    webpage = myWebpage()
    webpage.run(debug=False)