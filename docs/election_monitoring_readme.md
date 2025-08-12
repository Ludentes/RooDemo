# Election Monitoring System

A real-time monitoring and anomaly detection system for blockchain-based electronic voting. Designed for election observers to track multiple constituencies, detect irregularities, and ensure election integrity.

## 🎯 Overview

This system processes blockchain transaction logs from electronic voting conducted via mobile applications. It monitors multiple concurrent elections across various constituencies during a 3-day voting period, providing real-time insights and automated anomaly detection.

### Key Features

- **Real-time Dashboard**: Live monitoring of all constituencies with participation metrics
- **Anomaly Detection**: Automated detection of voting irregularities and suspicious patterns
- **Alert Management**: Categorized alerts with investigation workflow
- **Constituency Analysis**: Detailed view of individual constituency performance
- **File Processing**: Automated ingestion of hourly CSV transaction logs
- **WebSocket Updates**: Real-time data streaming for live dashboard updates

## 🏗️ Architecture

### Tech Stack

**Backend:**
- FastAPI (Python) - REST API and WebSocket server
- SQLAlchemy - ORM and database management
- SQLite - Database (easily upgradeable to PostgreSQL)
- Watchdog - File system monitoring
- Pandas - Data processing and analysis

**Frontend:**
- React 18 - UI framework
- TypeScript - Type safety
- Vite - Build tool and development server
- Zustand - State management
- Tailwind CSS - Styling
- Recharts - Data visualization

### System Components

```
CSV Files → File Watcher → Transaction Parser → Database
                                                    ↓
WebSocket ← Background Jobs ← Anomaly Detection ← Metrics Calculator
    ↓
React Dashboard ← REST API ← Services Layer ← Database
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd election-monitoring
```

2. **Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
```

4. **Environment Configuration:**
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

5. **Database Setup:**
```bash
cd backend
alembic upgrade head
```

### Running the Application

**Development Mode:**

1. **Start Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start Frontend:**
```bash
cd frontend
npm run dev
```

3. **Access Application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

**Production Mode:**
```bash
# Build frontend
cd frontend && npm run build

# Start with docker-compose
docker-compose up -d
```

## 📁 Project Structure

```
election-monitoring/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   ├── core/         # Background tasks & WebSocket
│   │   └── utils/        # Utilities
│   ├── data/             # CSV file processing
│   │   ├── input/        # Drop CSV files here
│   │   ├── processed/    # Processed files
│   │   └── backups/      # File backups
│   └── tests/            # Backend tests
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── stores/       # Zustand state management
│   │   ├── services/     # API services
│   │   └── pages/        # Page components
│   └── public/           # Static assets
└── docker-compose.yml    # Container orchestration
```

## 🔧 Configuration

### Backend Configuration (.env)

```bash
# Database
DATABASE_URL=sqlite:///./election_monitoring.db

# File Processing
INPUT_DIRECTORY=./data/input
PROCESSED_DIRECTORY=./data/processed
BACKUP_DIRECTORY=./data/backups

# Monitoring
CHECK_INTERVAL_SECONDS=30
ALERT_THRESHOLDS_MAX_RATIO=1.0
ALERT_THRESHOLDS_MIN_PARTICIPATION=0.3

# WebSocket
WEBSOCKET_HEARTBEAT_INTERVAL=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/application.log
```

### Frontend Configuration

The frontend automatically connects to `http://localhost:8000` in development. For production, update the API base URL in `src/services/apiClient.ts`.

## 📊 Data Processing

### CSV File Format

The system expects CSV files with the following structure:
- Filename: `{contractId}_{timestamp}.csv`
- Semicolon-separated values
- Contains blockchain transaction data with operation types

### File Processing Workflow

1. **File Detection**: Watchdog monitors `data/input/` directory
2. **Parsing**: CSV parser extracts transaction data
3. **Validation**: Data integrity checks and validation
4. **Storage**: Transactions stored in database
5. **Analysis**: Metrics calculation and anomaly detection
6. **Alerts**: Automated alert generation for detected anomalies
7. **Cleanup**: Processed files moved to `data/processed/`

### Supported Transaction Types

- `blindSigIssue`: Electronic bulletin issuance
- `vote`: Vote casting transaction

## 🚨 Anomaly Detection

### Detection Rules

1. **Votes Exceed Bulletins**: More votes than issued bulletins
2. **Unusual Voting Spike**: Abnormal increase in voting velocity
3. **Low Participation**: Below-threshold participation rates
4. **Timing Anomalies**: Voting during unusual hours
5. **System Offline**: Missing data or connectivity issues

### Alert Severity Levels

- **🔴 Critical**: Immediate attention required (e.g., votes > bulletins)
- **🟡 Warning**: Unusual patterns requiring investigation
- **🔵 Info**: Informational notifications (e.g., milestones)

## 🔌 API Reference

### Dashboard Endpoints

```http
GET /api/dashboard
GET /api/dashboard/activity
WS  /api/dashboard/ws
```

### Constituency Endpoints

```http
GET /api/constituencies
GET /api/constituencies/{id}
GET /api/constituencies/{id}/transactions
GET /api/constituencies/{id}/stats
```

### Alert Endpoints

```http
GET /api/alerts
GET /api/alerts/{id}
PUT /api/alerts/{id}/status
POST /api/alerts/{id}/notes
```

### File Processing

```http
POST /api/files/upload
GET  /api/files/status/{job_id}
```

For detailed API documentation, visit http://localhost:8000/docs when running the backend.

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests

```bash
# Start backend in test mode
cd backend
pytest tests/integration/

# Test file processing
cp tests/fixtures/sample.csv data/input/
# Monitor logs for processing results
```

## 🐳 Docker Deployment

### Development

```bash
docker-compose -f docker-compose.dev.yml up
```

### Production

```bash
docker-compose up -d
```

### Custom Configuration

Create `docker-compose.override.yml` for environment-specific settings:

```yaml
version: '3.8'
services:
  backend:
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/election_db
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: election_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

## 📈 Monitoring & Maintenance

### Health Checks

- Backend health: `GET /api/health`
- WebSocket connection status in frontend
- Database connectivity monitoring

### Log Files

- Application logs: `backend/logs/application.log`
- File processing logs: Monitor console output
- Error tracking: Check FastAPI error logs

### Performance Monitoring

- Transaction processing rate
- Database query performance
- WebSocket connection stability
- Memory usage for large CSV files

## 🔒 Security Considerations

### Data Protection

- No sensitive voter information stored
- Transaction data anonymized
- Secure file processing pipeline
- Input validation and sanitization

### Network Security

- CORS properly configured
- WebSocket connection security
- API rate limiting (configurable)
- Environment variable protection

## 🛠️ Development

### Adding New Features

1. **Backend**: Add service → API endpoint → tests
2. **Frontend**: Add store → service → component
3. **Database**: Create migration with Alembic

### Code Style

- Backend: Follow PEP 8, use Black formatter
- Frontend: ESLint + Prettier configuration
- Type hints required for Python
- TypeScript strict mode enabled

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 🐛 Troubleshooting

### Common Issues

**File Processing Not Working:**
- Check `data/input/` directory permissions
- Verify CSV file format
- Monitor backend logs for errors

**WebSocket Connection Failed:**
- Ensure backend is running on port 8000
- Check firewall settings
- Verify CORS configuration

**Database Errors:**
- Run `alembic upgrade head`
- Check database file permissions
- Verify SQLite installation

**High Memory Usage:**
- Large CSV files may require streaming processing
- Monitor background job performance
- Consider pagination for large datasets

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Zustand State Management](https://github.com/pmndrs/zustand)
- [SQLAlchemy ORM](https://sqlalchemy.org/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create GitHub issue for bugs
- Check troubleshooting section above
- Review API documentation at `/docs`

---

**Election Monitoring System v1.0.0**  
Built for transparent and secure election observation.