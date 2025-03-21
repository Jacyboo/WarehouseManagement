import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                           QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
from warehouse_tab import WarehouseTab
from sales_tab import SalesTab
from dashboard_tab import DashboardTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warehouse Management System")
        self.setMinimumSize(1200, 800)
        
        # Set dark theme for the entire application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
            }
        """)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        layout.addWidget(sidebar)
        
        # Create main content area
        self.content = QStackedWidget()
        layout.addWidget(self.content)
        
        # Add tabs
        self.warehouse_tab = WarehouseTab()
        self.sales_tab = SalesTab()
        self.dashboard_tab = DashboardTab()
        
        self.content.addWidget(self.warehouse_tab)
        self.content.addWidget(self.sales_tab)
        self.content.addWidget(self.dashboard_tab)
        
        # Set initial tab
        self.content.setCurrentWidget(self.warehouse_tab)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 0px;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Add logo/title
        title = QLabel("WMS")
        title.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: bold;
            padding: 20px;
            background-color: #34495e;
            border-radius: 10px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Add navigation buttons
        self.warehouse_btn = QPushButton("Warehouse")
        self.sales_btn = QPushButton("Sales")
        self.dashboard_btn = QPushButton("Dashboard")
        
        for btn in [self.warehouse_btn, self.sales_btn, self.dashboard_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    text-align: left;
                    padding: 15px;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
            """)
            layout.addWidget(btn)
        
        # Connect buttons to tab switching
        self.warehouse_btn.clicked.connect(lambda: self.switch_tab(0))
        self.sales_btn.clicked.connect(lambda: self.switch_tab(1))
        self.dashboard_btn.clicked.connect(lambda: self.switch_tab(2))
        
        layout.addStretch()
        return sidebar

    def switch_tab(self, index):
        # Animate the transition
        animation = QPropertyAnimation(self.content, b"pos")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Set the new widget
        self.content.setCurrentIndex(index)
        
        # Update button styles
        buttons = [self.warehouse_btn, self.sales_btn, self.dashboard_btn]
        for i, btn in enumerate(buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #34495e;
                        color: white;
                        text-align: left;
                        padding: 15px;
                        border-radius: 5px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: white;
                        text-align: left;
                        padding: 15px;
                        border-radius: 5px;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #34495e;
                    }
                """)

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')  # Use Fusion style for better dark theme support
    
    # Set application-wide dark theme
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(26, 26, 26))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(44, 62, 80))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(52, 73, 94))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(44, 62, 80))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(52, 152, 219))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    app.exec() 