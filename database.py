from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtCore import Qt

class Database:
    def __init__(self, db_name):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)
        if not self.db.open():
            raise Exception("Failed to open database")
        self.initialize_tables()
        self.model = QSqlTableModel()
        self.model.setTable("tickets")
        self.model.insertColumn(3) 
        self.model.setHeaderData(3, Qt.Horizontal, "Actions")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

    def initialize_tables(self):
        query = QSqlQuery()
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                sap_id INTEGER PRIMARY KEY UNIQUE,
                name TEXT NOT NULL,
                checked_in INTEGER NOT NULL DEFAULT 0
            )
            """
        )

    def create_ticket(self, sap_id, name, checked_in=0):
        record = self.model.record()
        record.setValue("sap_id", sap_id)
        record.setValue("name", name)
        record.setValue("checked_in", checked_in)
        if self.model.insertRecord(-1, record):
            if self.model.submitAll():
                return True
        raise Exception("Failed to create ticket: " + self.model.lastError().text())
        
    def mark_checked_in(self, sap_id):
        for row in range(self.model.rowCount()):
            if self.model.record(row).value("sap_id") == sap_id:
                if self.model.record(row).value("checked_in") == 1:
                    raise ValueError(f"SAP ID {sap_id} is already checked in.")
                self.model.setData(self.model.index(row, self.model.fieldIndex("checked_in")), 1)
                if self.model.submitAll():
                    return True
        raise KeyError(f"SAP ID {sap_id} not found in database.")
    
    def delete_ticket(self, sap_id):
        for row in range(self.model.rowCount()):
            if self.model.record(row).value("sap_id") == sap_id:
                self.model.removeRow(row)
                if self.model.submitAll():
                    return True
        raise KeyError(f"SAP ID {sap_id} not found in database.")