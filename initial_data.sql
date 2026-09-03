DROP TABLE cases;
DROP TABLE employees;

CREATE TABLE cases (
    "id"    INTEGER PRIMARY KEY,
    "patientName"    TEXT,
    "modality"    TEXT,
    "studyDate"    DATE,
    "status"    TEXT,
    "report"    VARCHAR,
    "claimedAt"    VARCHAR,
    "claimedBy"    VARCHAR
);

CREATE TABLE employees (
    "id" INTEGER PRIMARY KEY,
    "username" TEXT
);

INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy) 
    VALUES ('Jane Smith', 'CT', '2024-11-01', 'COMPLETED', 'Report text', '2024-11-05 10:03:02', 'jdoe');
INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy)
    VALUES ('Jane Smith', 'MRI', '2024-12-07', 'COMPLETED', 'Report text 2', '2024-12-10 15:27:36', 'jdoe');
INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy)
    VALUES ('Harry Locke', 'XR', '2025-02-20', 'COMPLETED', 'Report text 3', '2025-02-28 09:44:02', 'mpeters');
INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy)
    VALUES ('Leah Horne', 'US', '2025-03-05', 'COMPLETED', 'Report text 4', '2025-03-20 13:45:12', 'wtravis');
INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy)
    VALUES ('Leon Trejo', 'CT', '2025-07-18', 'COMPLETED', 'Report text 5', '2025-07-18 16:49:56', 'mpeters');
INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy)
    VALUES ('Ryan Crane', 'MRI', '2026-04-23', 'COMPLETED', 'Report text 6', '2026-04-23 09:36:27', 'jdoe');
INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy)
    VALUES ('Ana Hardin', 'XR', '2026-09-01', 'IN_PROGRESS', NULL, '2026-09-03 12:05:02', 'mpeters');
INSERT INTO cases (patientName, modality, studyDate, status, report, claimedAt, claimedBy)
    VALUES ('Ellis Brennan', 'US', '2026-09-01', 'PENDING', NULL, NULL, NULL);


INSERT INTO employees (username) VALUES ('jdoe');
INSERT INTO employees (username) VALUES ('mpeters');
INSERT INTO employees (username) VALUES ('wtravis');