# e-ticket-application

A desktop application for creating and validating event e-tickets. It generates a QR-coded PDF ticket per attendee and scans those tickets at check-in using a webcam, backed by a local SQLite database.

## Features

- Create a ticket from an attendee's SAP ID and name — generates a QR code and a printable PDF ticket (100 × 200 mm)
- Scan tickets at check-in with a webcam; each ticket can only be checked in once
- Browse, sort, and delete tickets in a table view
- Data persisted locally in SQLite

## Stack

- Python + PySide6 (Qt for Python)
- `segno` — QR generation
- OpenCV (`wechat_qrcode` detector) — webcam scanning
- SQLite via QtSql

## Getting started

Requirements: Python 3.10+ and a webcam (for scanning).

```bash
pip install -r requirements.txt
python main.py
```

The app creates `app_database.db` and a `generated_tickets/` folder in the working directory.

## Project structure

```
main.py            App entry point and navigation
create_ticket.py   Ticket form + PDF/QR generation
scan_ticket.py     Webcam check-in view
view_tickets.py    Ticket table view
database.py        SQLite schema and operations
qr_code.py         QR generation + camera scanner thread
template.html      Ticket PDF template
docs.typ           Project documentation (Typst)
requirements.txt
```

## How it works

- Tickets live in a `tickets` table (`sap_id` primary key, `name`, `checked_in`)
- Creating a ticket writes a row and renders a PDF from `template.html`, filling in `{{ sap_id }}`, `{{ name }}`, and `{{ qr_path }}`
- The QR payload is `SAP ID: <id>, Name: <name>`; the scanner parses the SAP ID and marks the row checked in
