# 📀 Media(CD/DVD) Issuance System

A secure and user-friendly web-based application designed for managing the issuance and transfer of physical media like CDs and DVDs. This system streamlines the recording of issuance records, ensures accountability, and provides export functionality for administrative review.

## ✅ Features

- Add new issuance records with full recipient and issuer details
- Automatically checks for duplicate Media IDs
- Prompt for transfer when media is already issued
- Updates previous owner's record with transfer remarks
- Adds new entry for the new recipient with proper transfer history
- Export records to Excel with date-range filtering
- Admin authentication for data export
- Fully responsive UI using Tailwind CSS
- Secure backend powered by Flask & MySQL

## 🛠️ Technologies Used

- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Export Tool**: Pandas + openpyxl
- **Environment**: XAMPP (for MySQL) + Python virtual environment (venv)
