# Trading Simulator Frontend

This is the frontend application for the Frontpage Trading Simulator, built with React.js.

## Features

- Real-time trading simulation interface
- Portfolio management dashboard
- User authentication and registration
- Interactive charts and data visualization
- Responsive design with Material-UI components
- Real-time market data display
- Trading history and analytics
- Leaderboard and rating system

## Technology Stack

- **React 18+** - Modern React with hooks and functional components
- **Material-UI (MUI)** - Component library for consistent UI design
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **Chart.js** - Interactive charts and data visualization
- **React Context API** - State management
- **WebSocket** - Real-time updates

## Getting Started

### Prerequisites

- Node.js 14 or higher
- npm or yarn package manager

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── services/      # API services and utilities
├── utils/         # Helper functions
├── App.js         # Main application component
└── index.js       # Application entry point
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (use with caution)

## Backend Integration

The frontend communicates with the Flask backend through REST APIs. The proxy configuration in `package.json` forwards API requests to `http://localhost:5000` during development.

## Contributing

Please follow the existing code structure and naming conventions when contributing to this project.
