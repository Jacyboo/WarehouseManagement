from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                           QSpinBox, QDoubleSpinBox, QMessageBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette
import sqlite3
from datetime import datetime

class SalesTab(QWidget):
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
        title = QLabel("Sales Management")
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
        
        # Product selection with modern styling
        product_label = QLabel("Select Product:")
        product_label.setStyleSheet("color: white; font-size: 14px;")
        form_layout.addWidget(product_label)
        
        self.product_combo = QComboBox()
        self.product_combo.setMinimumWidth(300)
        self.product_combo.setStyleSheet("""
            QComboBox {
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """)
        form_layout.addWidget(self.product_combo)
        
        # Quantity with modern styling
        quantity_label = QLabel("Quantity:")
        quantity_label.setStyleSheet("color: white; font-size: 14px;")
        form_layout.addWidget(quantity_label)
        
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
        
        # Sale price with modern styling
        price_label = QLabel("Sale Price ($):")
        price_label.setStyleSheet("color: white; font-size: 14px;")
        form_layout.addWidget(price_label)
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0.01)
        self.price_input.setMaximum(999999.99)
        self.price_input.setValue(0.01)
        self.price_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
        """)
        form_layout.addWidget(self.price_input)
        
        # Record Sale button with modern styling
        add_btn = QPushButton("Record Sale")
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
        add_btn.clicked.connect(self.record_sale)
        form_layout.addWidget(add_btn)
        
        # Refresh button with modern styling
        refresh_btn = QPushButton("Refresh Products")
        refresh_btn.setStyleSheet("""
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
        refresh_btn.clicked.connect(self.update_product_list)
        form_layout.addWidget(refresh_btn)
        
        layout.addWidget(form_card)
        
        # Table with modern styling
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Product Name", "Quantity", "Sale Price", "Total Revenue", "Profit"])
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
        
        # Update product list
        self.update_product_list()

    def setup_database(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sales
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     product_id INTEGER NOT NULL,
                     quantity INTEGER NOT NULL,
                     sale_price REAL NOT NULL,
                     date_sold TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     FOREIGN KEY (product_id) REFERENCES products (id))''')
        conn.commit()
        conn.close()

    def update_product_list(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        
        # Debug: Print all products first
        c.execute('SELECT id, name, quantity, has_arrived FROM products')
        all_products = c.fetchall()
        print("All products in database:", all_products)
        
        # Now get only available products
        c.execute('''SELECT id, name, quantity, cost_per_unit 
                    FROM products 
                    WHERE quantity > 0 AND has_arrived = 1''')
        products = c.fetchall()
        print("Available products for sale:", products)
        
        conn.close()
        
        self.product_combo.clear()
        if not products:
            self.product_combo.addItem("No products available")
            self.product_combo.setEnabled(False)
            return
            
        self.product_combo.setEnabled(True)
        self.product_data = {}
        for p in products:
            display_text = f"{p[1]} (Stock: {p[2]}, Cost: ${p[3]:.2f})"
            self.product_data[display_text] = p
            self.product_combo.addItem(display_text)

    def record_sale(self):
        if not self.product_combo.isEnabled() or self.product_combo.currentText() == "No products available":
            QMessageBox.warning(self, "Error", "No products available for sale")
            return
            
        product_key = self.product_combo.currentText()
        if product_key not in self.product_data:
            QMessageBox.warning(self, "Error", "Please select a valid product")
            return
            
        product = self.product_data[product_key]
        quantity = self.quantity_input.value()
        
        # Verify stock again
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        c.execute('SELECT quantity FROM products WHERE id = ?', (product[0],))
        current_stock = c.fetchone()[0]
        
        if quantity > current_stock:
            conn.close()
            QMessageBox.warning(self, "Error", f"Not enough stock available. Current stock: {current_stock}")
            return
            
        sale_price = self.price_input.value()
        
        # Record the sale
        c.execute('''INSERT INTO sales (product_id, quantity, sale_price)
                    VALUES (?, ?, ?)''', (product[0], quantity, sale_price))
        
        # Update product quantity
        c.execute('''UPDATE products 
                    SET quantity = quantity - ? 
                    WHERE id = ?''', (quantity, product[0]))
        
        conn.commit()
        conn.close()
        
        self.load_data()
        self.update_product_list()
        self.clear_inputs()
        
        QMessageBox.information(self, "Success", "Sale recorded successfully!")

    def load_data(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        c.execute('''
            SELECT s.id, p.name, s.quantity, s.sale_price, p.cost_per_unit
            FROM sales s
            JOIN products p ON s.product_id = p.id
            ORDER BY s.date_sold DESC
        ''')
        sales = c.fetchall()
        conn.close()
        
        self.table.setRowCount(len(sales))
        for i, sale in enumerate(sales):
            self.table.setItem(i, 0, QTableWidgetItem(str(sale[0])))
            self.table.setItem(i, 1, QTableWidgetItem(sale[1]))
            self.table.setItem(i, 2, QTableWidgetItem(str(sale[2])))
            self.table.setItem(i, 3, QTableWidgetItem(f"${sale[3]:.2f}"))
            total_revenue = sale[2] * sale[3]
            self.table.setItem(i, 4, QTableWidgetItem(f"${total_revenue:.2f}"))
            profit = total_revenue - (sale[2] * sale[4])
            self.table.setItem(i, 5, QTableWidgetItem(f"${profit:.2f}"))

    def clear_inputs(self):
        self.quantity_input.setValue(1)
        self.price_input.setValue(0.01) 