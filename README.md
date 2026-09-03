## Sirona Medical Backend Coding Challenge
## Alex Stute

Python packages/dependencies used:
- Flask
- sqlite3
- unittest

To run this project, use command `python -m unittest test_webserver.py -v; if ($LASTEXITCODE -eq 0) { python main.py; python webserver.py }` (for Windows Powershell)

This command will run the test cases, then leave the server running for further tests.

### Questions and assumptions:
Q: Should case and employee IDs be strictly integers, strictly words/letters, or a mix of the two?

Assumption: All IDs will be integers, just to keep things simple. Makes auto incrementation of primary keys simple in SQL.

Q: Should DELETE completely remove data from the database or should it just mark it as no longer valid?

Assumption: I completely removed the data from the database for simplicity. In an actual work scenario, I would likely label the data as deleted so it cannot be accessed normally, but is still saved. This way if an employee is deleted, the cases they have worked on in the past are not corrupted.

