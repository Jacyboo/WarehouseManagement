# Warehouse Management System

A modern, dark-themed warehouse management system built with PyQt6. This application helps you track inventory, manage sales, and monitor business performance with a beautiful and intuitive interface.

## Features

- **Modern Dark Theme UI**: Beautiful and eye-friendly interface
- **Warehouse Management**:
  - Add new products with quantity and cost
  - Track product arrival status
  - Monitor current inventory levels
- **Sales Management**:
  - Record sales transactions
  - Track revenue and profit
  - Automatic inventory updates
- **Dashboard**:
  - Real-time statistics
  - Profit charts
  - Top performing products

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/warehouse-management-system.git
cd warehouse-management-system
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Adding Products**:
   - Go to the Warehouse tab
   - Enter product details (name, quantity, cost)
   - Check "Arrived" if the product is in stock
   - Click "Add Product"

2. **Recording Sales**:
   - Switch to the Sales tab
   - Select a product from the dropdown
   - Enter quantity and sale price
   - Click "Record Sale"

3. **Viewing Statistics**:
   - Navigate to the Dashboard tab
   - View total revenue, cost, and profit
   - Check profit charts and top products

## Requirements

- Python 3.8+
- PyQt6
- Matplotlib
- Pandas

## Database

The application uses SQLite for data storage. The database file (`warehouse.db`) will be created automatically when you first run the application.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created by Jacx 