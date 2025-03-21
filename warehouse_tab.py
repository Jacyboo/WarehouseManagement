from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                           QSpinBox, QDoubleSpinBox, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette
import sqlite3
from datetime import datetime

class WarehouseTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_database()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title with modern styling
        title = QLabel("Warehouse Management")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
                padding: 10px;
                background-color: #2c3e50;
                border-radius: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Input form with modern card design
        form_card = QWidget()
        form_card.setStyleSheet("""
            QWidget {
                background-color: #34495e;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        form_layout = QHBoxLayout(form_card)
        form_layout.setSpacing(10)
        
        # Product name with modern styling
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product Name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #2980b9;
            }
        """)
        form_layout.addWidget(self.name_input)
        
        # Quantity with modern styling
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(9999)
        self.quantity_input.setValue(1)
        self.quantity_input.setStyleSheet("""
            QSpinBox {
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
        """)
        form_layout.addWidget(self.quantity_input)
        
        # Cost per unit with modern styling
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMinimum(0.01)
        self.cost_input.setMaximum(999999.99)
        self.cost_input.setValue(0.01)
        self.cost_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
        """)
        form_layout.addWidget(self.cost_input)
        
        # Arrived checkbox with modern styling
        self.arrived_checkbox = QCheckBox("Arrived")
        self.arrived_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        form_layout.addWidget(self.arrived_checkbox)
        
        # Add button with modern styling
        add_btn = QPushButton("Add Product")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        add_btn.clicked.connect(self.add_product)
        form_layout.addWidget(add_btn)
        
        layout.addWidget(form_card)
        
        # Table with modern styling
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Product Name", "Quantity", "Cost per Unit", "Total Cost", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #34495e;
                border: none;
                border-radius: 10px;
                gridline-color: #2c3e50;
                color: white;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)
        
        # Toggle button with modern styling
        self.toggle_btn = QPushButton("Toggle Arrived Status")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_arrived_status)
        layout.addWidget(self.toggle_btn)

    def setup_database(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        
        # Add has_arrived column if it doesn't exist
        try:
            c.execute('ALTER TABLE products ADD COLUMN has_arrived BOOLEAN DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        c.execute('''CREATE TABLE IF NOT EXISTS products
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     quantity INTEGER NOT NULL,
                     cost_per_unit REAL NOT NULL,
                     has_arrived BOOLEAN DEFAULT 0,
                     date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def add_product(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a product name")
            return
            
        quantity = self.quantity_input.value()
        cost_per_unit = self.cost_input.value()
        has_arrived = 1 if self.arrived_checkbox.isChecked() else 0
        
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        c.execute('''INSERT INTO products (name, quantity, cost_per_unit, has_arrived)
                    VALUES (?, ?, ?, ?)''', (name, quantity, cost_per_unit, has_arrived))
        conn.commit()
        conn.close()
        
        self.load_data()
        self.clear_inputs()
        
        # Show success message with animation
        success_msg = QMessageBox(self)
        success_msg.setIcon(QMessageBox.Icon.Information)
        success_msg.setText("Product added successfully!")
        success_msg.setStyleSheet("""
            QMessageBox {
                background-color: #34495e;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 14px;
            }
        """)
        success_msg.exec()

    def toggle_arrived_status(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Please select a product to toggle status")
            return
            
        row = selected_items[0].row()
        product_id = int(self.table.item(row, 0).text())
        
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        c.execute('UPDATE products SET has_arrived = NOT has_arrived WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        # Only show products that haven't been sold (quantity > 0)
        c.execute('''SELECT * FROM products 
                    WHERE quantity > 0 
                    ORDER BY date_added DESC''')
        products = c.fetchall()
        conn.close()
        
        self.table.setRowCount(len(products))
        for i, product in enumerate(products):
            self.table.setItem(i, 0, QTableWidgetItem(str(product[0])))
            self.table.setItem(i, 1, QTableWidgetItem(product[1]))
            self.table.setItem(i, 2, QTableWidgetItem(str(product[2])))
            self.table.setItem(i, 3, QTableWidgetItem(f"${product[3]:.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(f"${product[2] * product[3]:.2f}"))
            status = "✓ Arrived" if product[4] else "⏳ Pending"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 5, status_item)

    def clear_inputs(self):
        self.name_input.clear()
        self.quantity_input.setValue(1)
        self.cost_input.setValue(0.01)
        self.arrived_checkbox.setChecked(False) 