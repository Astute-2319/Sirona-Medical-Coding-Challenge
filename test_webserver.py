import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from webserver import myWebpage


class WebserverCaseWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_directory = Path(__file__).parent
        cls.database_directory = tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True
        )
        cls.schema = (
            (cls.project_directory / "initial_data.sql")
            .read_text(encoding="utf-8")
            .replace("DROP TABLE cases;", "DROP TABLE IF EXISTS cases;")
            .replace("DROP TABLE employees;", "DROP TABLE IF EXISTS employees;")
        )
        cls.original_directory = Path.cwd()
        os.chdir(cls.database_directory.name)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.original_directory)
        cls.database_directory.cleanup()

    def setUp(self):
        with sqlite3.connect("Challenge_DB.db") as connection:
            connection.executescript(self.schema)

        self.client = myWebpage().app.test_client()

    def test_claiming_pending_case_succeeds_and_transitions_status(self):
        response = self.client.post(
            "/cases/8/claim", json={"username": "jdoe"}
        )

        self.assertEqual(response.status_code, 200)
        case = response.get_json()
        self.assertEqual(case[4], "IN_PROGRESS")
        self.assertEqual(case[7], "jdoe")

    def test_claiming_in_progress_case_returns_error(self):
        response = self.client.post(
            "/cases/7/claim", json={"username": "jdoe"}
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("not currently pending", response.get_json())

    def test_claiming_completed_case_returns_error(self):
        response = self.client.post(
            "/cases/1/claim", json={"username": "jdoe"}
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("not currently pending", response.get_json())

    def test_claiming_case_without_username_returns_error(self):
        response = self.client.post("/cases/8/claim", json={})

        self.assertEqual(response.status_code, 415)
        self.assertIn("Username cannot be empty", response.get_json())

    def test_claiming_case_with_unknown_username_returns_error(self):
        response = self.client.post(
            "/cases/8/claim", json={"username": "unknown"}
        )

        self.assertEqual(response.status_code, 415)
        self.assertIn("not a valid employee", response.get_json())

    def test_submitting_report_on_in_progress_case_succeeds(self):
        response = self.client.post(
            "/cases/7/report",
            json={"author": "mpeters", "report": "Findings documented."},
        )

        self.assertEqual(response.status_code, 200)
        case = response.get_json()
        self.assertEqual(case[4], "COMPLETED")
        self.assertEqual(case[5], "Findings documented.")

    def test_submitting_report_on_pending_case_returns_error(self):
        response = self.client.post(
            "/cases/8/report",
            json={"author": "jdoe", "report": "Findings documented."},
        )

        self.assertIn(response.status_code, (415, 422))

    def test_submitting_report_on_completed_case_returns_error(self):
        response = self.client.post(
            "/cases/1/report",
            json={"author": "jdoe", "report": "Updated findings."},
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("currently in progress", response.get_json())

    def test_submitting_report_with_empty_body_returns_validation_error(self):
        response = self.client.post(
            "/cases/7/report", json={"author": "mpeters", "report": ""}
        )

        self.assertEqual(response.status_code, 415)
        self.assertIn("Report body cannot be empty", response.get_json())

    def test_submitting_report_as_different_employee_returns_error(self):
        response = self.client.post(
            "/cases/7/report",
            json={"author": "jdoe", "report": "Findings documented."},
        )

        self.assertEqual(response.status_code, 415)
        self.assertIn("did not claim this case", response.get_json())


if __name__ == "__main__":
    unittest.main()
