# Frontpage Trading Sim

A comprehensive simulated trading platform that provides real-time market data and a competitive rating system similar to Codeforces.

## Overview

Frontpage Trading Sim is a web-based trading simulation platform designed to help users practice trading strategies without financial risk. The platform features real-time market data integration, user account management, and a competitive rating system that ranks traders based on their profit percentages.

## Features

### Trading Platform Simulation
- Real-time market data integration using AngelOne API
- Virtual portfolio management
- Buy/sell order execution simulation
- Portfolio performance tracking
- Trading history and analytics
- Paper trading with realistic market conditions

### User Registration System
- **Name**: Full name registration
- **Phone**: Mobile number verification
- **Email**: Email address verification and notifications
- Secure authentication and session management
- User profile management

### Rating System (Codeforces-style)
- Performance-based rating calculation
- Profit percentage tracking
- Competitive leaderboards
- Rating categories (Newbie, Pupil, Specialist, Expert, etc.)
- Achievement system and badges
- Monthly/yearly performance reports

## Technology Stack

### Backend
- **Framework**: Python Flask
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite
- **API Integration**: AngelOne API for real-time market data
- **Authentication**: JWT tokens
- **Task Queue**: Celery for background tasks

### Frontend
- **Framework**: React.js
- **State Management**: Redux/Context API
- **UI Components**: Material-UI or Bootstrap
- **Charts**: Chart.js or D3.js for data visualization
- **Real-time Updates**: WebSocket integration

### Additional Technologies
- **Deployment**: Docker containers
- **API Documentation**: Swagger/OpenAPI
- **Testing**: PyTest (Backend), Jest (Frontend)
- **Version Control**: Git with GitHub

## API Configuration

### AngelOne API Setup

**Important**: The AngelOne API integration requires authentication credentials that must be provided by the user.

```python
# config.py
ANGELONE_API_KEY = "YOUR_API_KEY_HERE"  # Placeholder - User must provide
ANGELONE_CLIENT_CODE = "YOUR_CLIENT_CODE_HERE"  # Placeholder - User must provide
ANGELONE_PASSWORD = "YOUR_PASSWORD_HERE"  # Placeholder - User must provide
```

**Note**: These are placeholder values. Users must obtain their own API credentials from AngelOne and update the configuration file before running the application.

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- AngelOne API credentials (obtain from AngelOne broker)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nikhlesh123/frontpage-trading-sim.git
cd frontpage-trading-sim
```

2. Set up backend environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up frontend environment:
```bash
cd frontend
npm install
```

4. Configure API credentials:
   - Copy `config.example.py` to `config.py`
   - Add your AngelOne API credentials
   - Update database configuration

5. Initialize database:
```bash
flask db upgrade
```

6. Start the application:
```bash
# Backend (in backend directory)
flask run

# Frontend (in frontend directory)
npm start
```

## Project Structure

```
frontpage-trading-sim/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── README.md
├── docs/
├── tests/
└── README.md
```

## Features Roadmap

- [ ] Real-time market data integration
- [ ] User authentication system
- [ ] Portfolio management
- [ ] Trading simulation engine
- [ ] Rating calculation system
- [ ] Leaderboards and competitions
- [ ] Mobile responsive design
- [ ] Advanced charting tools
- [ ] Social trading features
- [ ] API rate limiting and caching

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is a simulation platform for educational purposes only. It does not involve real money trading. Always consult with financial advisors before making actual investment decisions.

## Support

For support and questions, please open an issue in the GitHub repository or contact the development team.

---

**Note**: Remember to obtain and configure your AngelOne API credentials before running the application. The placeholder values in the configuration file will not work without proper authentication.
