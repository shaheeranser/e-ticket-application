#set page(
  paper: "a4",
  margin: (x: 2.5cm, y:2.5cm)
)

= Documentation
This project aims to develop an E ticket application for a simple event at my university. The functionalities will include:
- Generating a ticket for a student (using their SAP ID as a primary key)
- Validating the ticket at the event checkin
- Sending an email to the students with their ticket attached as a PDF (optional/non functional requirement)

= Technologies Used
#table(
  align: center,
  columns: (auto, auto),
  inset: 10pt,
  table.header(
    [*Technology*], [*Purpose*]
  ),
  [Python], [Main programming language used for the application],
  [SQLite], [Database used to store student and ticket information],
)