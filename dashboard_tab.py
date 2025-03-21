from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()
        
        # Set up auto-refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(30000)  # Refresh every 30 seconds

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Revenue Card
        self.revenue_card = self.create_stat_card("Total Revenue", "$0.00")
        stats_layout.addWidget(self.revenue_card)
        
        # Total Cost Card
        self.cost_card = self.create_stat_card("Total Cost", "$0.00")
        stats_layout.addWidget(self.cost_card)
        
        # Total Profit Card
        self.profit_card = self.create_stat_card("Total Profit", "$0.00")
        stats_layout.addWidget(self.profit_card)
        
        # Profit Margin Card
        self.margin_card = self.create_stat_card("Profit Margin", "0%")
        stats_layout.addWidget(self.margin_card)
        
        layout.addLayout(stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Profit over time chart
        self.profit_chart = self.create_chart("Profit Over Time")
        charts_layout.addWidget(self.profit_chart)
        
        # Top products chart
        self.products_chart = self.create_chart("Top Products by Profit")
        charts_layout.addWidget(self.products_chart)
        
        layout.addLayout(charts_layout)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)

    def create_stat_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #333; font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)
        
        return card

    def create_chart(self, title):
        chart = QFrame()
        chart.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(chart)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333; font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        return chart

    def load_data(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        
        # Calculate total revenue
        c.execute('''
            SELECT SUM(quantity * sale_price)
            FROM sales
        ''')
        total_revenue = c.fetchone()[0] or 0
        
        # Calculate total cost
        c.execute('''
            SELECT SUM(s.quantity * p.cost_per_unit)
            FROM sales s
            JOIN products p ON s.product_id = p.id
        ''')
        total_cost = c.fetchone()[0] or 0
        
        # Calculate total profit
        total_profit = total_revenue - total_cost
        
        # Calculate profit margin
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Update stat cards
        labels = self.revenue_card.findChildren(QLabel)
        labels[1].setText(f"${total_revenue:,.2f}")
        
        labels = self.cost_card.findChildren(QLabel)
        labels[1].setText(f"${total_cost:,.2f}")
        
        labels = self.profit_card.findChildren(QLabel)
        labels[1].setText(f"${total_profit:,.2f}")
        
        labels = self.margin_card.findChildren(QLabel)
        labels[1].setText(f"{profit_margin:.1f}%")
        
        # Update profit over time chart
        self.update_profit_chart()
        
        # Update top products chart
        self.update_products_chart()
        
        conn.close()

    def update_profit_chart(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        
        # Get last 30 days of sales
        c.execute('''
            SELECT date(s.date_sold) as date,
                   SUM(s.quantity * s.sale_price) as revenue,
                   SUM(s.quantity * p.cost_per_unit) as cost
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.date_sold >= date('now', '-30 days')
            GROUP BY date(s.date_sold)
            ORDER BY date
        ''')
        data = c.fetchall()
        
        if data:
            dates = [row[0] for row in data]
            profits = [row[1] - row[2] for row in data]
            
            # Clear previous plot
            self.profit_chart.findChild(FigureCanvas).figure.clear()
            ax = self.profit_chart.findChild(FigureCanvas).figure.add_subplot(111)
            
            # Plot new data
            ax.plot(dates, profits, marker='o')
            ax.set_title('Daily Profit')
            ax.set_xlabel('Date')
            ax.set_ylabel('Profit ($)')
            plt.xticks(rotation=45)
            self.profit_chart.findChild(FigureCanvas).figure.tight_layout()
            self.profit_chart.findChild(FigureCanvas).draw()
        
        conn.close()

    def update_products_chart(self):
        conn = sqlite3.connect('warehouse.db')
        c = conn.cursor()
        
        # Get top 5 products by profit
        c.execute('''
            SELECT p.name,
                   SUM(s.quantity * s.sale_price) as revenue,
                   SUM(s.quantity * p.cost_per_unit) as cost
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.id
            ORDER BY (revenue - cost) DESC
            LIMIT 5
        ''')
        data = c.fetchall()
        
        if data:
            products = [row[0] for row in data]
            profits = [row[1] - row[2] for row in data]
            
            # Clear previous plot
            self.products_chart.findChild(FigureCanvas).figure.clear()
            ax = self.products_chart.findChild(FigureCanvas).figure.add_subplot(111)
            
            # Plot new data
            ax.bar(products, profits)
            ax.set_title('Top Products by Profit')
            ax.set_xlabel('Product')
            ax.set_ylabel('Profit ($)')
            plt.xticks(rotation=45)
            self.products_chart.findChild(FigureCanvas).figure.tight_layout()
            self.products_chart.findChild(FigureCanvas).draw()
        
        conn.close() 