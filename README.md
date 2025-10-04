# Edu-Ride - Student Transportation Platform

A comprehensive ride-sharing platform specifically designed for the Sion-Somaiya route, connecting students with local auto-rickshaw drivers for safe, affordable, and convenient transportation.

## 🚀 Features

### For Students
- **Real-time Ride Booking**: Find and book available rides instantly
- **Group Rides**: Join group rides to split costs and save money
- **Live Tracking**: Track your ride in real-time
- **Secure Payments**: Pay with UPI, QR codes, or cash
- **Transparent Pricing**: No hidden charges, clear fare structure

### For Drivers
- **Driver Onboarding**: Easy registration and verification process
- **Ride Management**: Create, manage, and track your rides
- **Digital Payments**: Receive payments digitally with transaction history
- **Bonus System**: Earn points and bonuses for completed trips
- **Flexible Schedule**: Set your own working hours

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **QR Code Generation**: qrcode library
- **Real-time Updates**: JavaScript polling

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Edu-Ride
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Register as a student or driver
   - Start using the platform!

## 📱 Usage Guide

### For Students
1. **Register**: Create an account with your university details
2. **Find Rides**: Browse available rides on your dashboard
3. **Book Rides**: Click "Book Ride" on any available ride
4. **Group Rides**: Look for group rides to save money
5. **Pay**: Use UPI, QR codes, or cash for payment

### For Drivers
1. **Register**: Create an account with your license and vehicle details
2. **Create Rides**: Set pickup/drop-off locations, time, and fare
3. **Manage Rides**: Start, track, and complete rides
4. **Generate QR**: Create QR codes for easy payments
5. **Track Earnings**: Monitor your daily, weekly, and monthly earnings

## 🗂️ Project Structure

```
Edu-Ride/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── student_dashboard.html
│   ├── driver_dashboard.html
│   ├── create_ride.html
│   └── qr_payment.html
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── main.js       # JavaScript functionality
```

## 🔧 Configuration

### Database
The application uses SQLite by default. To use a different database:

1. Update the `SQLALCHEMY_DATABASE_URI` in `app.py`
2. Install the appropriate database driver
3. Update the connection string

### Security
- Change the `SECRET_KEY` in `app.py` for production
- Use environment variables for sensitive configuration
- Implement HTTPS in production

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production WSGI server (Gunicorn, uWSGI)
2. Use a reverse proxy (Nginx)
3. Set up a production database (PostgreSQL recommended)
4. Configure environment variables
5. Set up SSL certificates

## 🔮 Future Enhancements

- **Mobile App**: React Native/Flutter mobile applications
- **Real-time Notifications**: WebSocket integration for live updates
- **Maps Integration**: Google Maps API for route optimization
- **Advanced Analytics**: Driver and student analytics dashboard
- **Rating System**: Rate and review system for drivers and students
- **Push Notifications**: Mobile push notifications for ride updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, email support@edu-ride.com or create an issue in the repository.

## 🙏 Acknowledgments

- Bootstrap for the responsive UI framework
- Font Awesome for the beautiful icons
- Flask community for the excellent web framework
- All contributors and testers

---

**Edu-Ride** - Making student transportation safe, affordable, and convenient! 🚗💨
