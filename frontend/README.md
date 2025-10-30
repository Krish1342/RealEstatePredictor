# Real Estate Price Predictor - Frontend

A modern, responsive React application for predicting Bangalore real estate prices using AI.

## 🚀 Features

- **Modern UI/UX**: Built with React 18, Tailwind CSS, and Framer Motion
- **Real-time Predictions**: Instant property valuations with comprehensive insights
- **Interactive Analytics**: Rich data visualizations using Recharts
- **Responsive Design**: Mobile-first approach, works on all devices
- **API Integration**: Seamless connection with FastAPI backend
- **Hot Reload**: Fast development with Vite

## 📋 Prerequisites

- Node.js 16.x or higher
- npm or yarn package manager
- Backend API running on http://localhost:8000

## 🛠️ Installation

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## 🏃‍♂️ Running the Application

### Development Mode

```powershell
# Start development server
npm run dev

# Or use the batch script from root directory
..\start_frontend.bat
```

The application will be available at: **http://localhost:5173**

### Production Build

```powershell
# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/     # Reusable components
│   │   ├── Navbar.jsx
│   │   ├── Footer.jsx
│   │   └── PredictionResult.jsx
│   ├── pages/         # Page components
│   │   ├── Home.jsx
│   │   ├── Predict.jsx
│   │   ├── Analytics.jsx
│   │   └── About.jsx
│   ├── services/      # API services
│   │   └── api.js
│   ├── App.jsx        # Main app component
│   ├── main.jsx       # Entry point
│   └── index.css      # Global styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 🎨 Key Components

### Pages

1. **Home** (`/`)

   - Hero section with call-to-action
   - Features showcase
   - Statistics display
   - How it works section

2. **Predict** (`/predict`)

   - Property details form
   - Real-time validation
   - Prediction results with visualizations

3. **Analytics** (`/analytics`)

   - Model performance metrics
   - Interactive charts and graphs
   - Comparative analysis

4. **About** (`/about`)
   - Technology stack
   - Model information
   - Dataset details

### Components

- **Navbar**: Navigation with API status indicator
- **Footer**: Site footer with links
- **PredictionResult**: Displays prediction results with charts

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

### API Proxy

The Vite config includes a proxy to the backend:

```javascript
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

## 🎯 Features in Detail

### Property Prediction Form

- **Basic Information**: Type, location, BHK, size, etc.
- **Floor Details**: Floor number, total floors, facing
- **Amenities**: Furnished status, parking, balcony, security
- **Nearby Facilities**: Schools, hospitals, transport

### Prediction Results

- **Main Prediction**: Ensemble prediction with confidence score
- **Price Range**: Min, max, and predicted values
- **AI Insights**: Smart recommendations based on inputs
- **Model Breakdown**: Individual model predictions
- **Feature Importance**: Top influential features
- **Interactive Charts**: Bar charts, pie charts, radar charts

### Analytics Dashboard

- **Model Metrics**: R² scores, MAE, RMSE for all models
- **Performance Comparison**: Visual comparisons
- **Ensemble Weights**: Weight distribution
- **Detailed Tables**: Complete model information

## 🎨 Styling

The application uses:

- **Tailwind CSS**: Utility-first CSS framework
- **Custom Components**: Pre-styled components in `index.css`
- **Gradient Themes**: Primary and secondary color schemes
- **Animations**: Framer Motion for smooth transitions

### Custom CSS Classes

```css
.gradient-bg
  -
  Gradient
  background
  .card
  -
  Card
  container
  .card-hover
  -
  Card
  with
  hover
  effect
  .btn-primary
  -
  Primary
  button
  .btn-secondary
  -
  Secondary
  button
  .input-field
  -
  Form
  input
  .label
  -
  Form
  label;
```

## 📊 Charts & Visualizations

Using Recharts library for:

- **Bar Charts**: Model comparisons, feature importance
- **Pie Charts**: Weight distribution
- **Radar Charts**: Multi-dimensional performance
- **Line Charts**: Trend analysis

## 🔌 API Integration

### API Service (`src/services/api.js`)

```javascript
import { predictPrice, getModelsInfo, healthCheck } from "./services/api";

// Get prediction
const result = await predictPrice(propertyData);

// Check health
const health = await healthCheck();

// Get models info
const models = await getModelsInfo();
```

## 🚨 Error Handling

- Toast notifications for user feedback
- API error interception
- Form validation
- Loading states

## 📱 Responsive Design

Breakpoints:

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔍 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🛠️ Development Tools

```powershell
# Lint code
npm run lint

# Format code (if prettier is installed)
npm run format
```

## 📦 Dependencies

### Core

- `react`: ^18.2.0
- `react-dom`: ^18.2.0
- `react-router-dom`: ^6.20.0

### UI & Visualization

- `tailwindcss`: ^3.3.6
- `framer-motion`: ^10.16.5
- `recharts`: ^2.10.3
- `lucide-react`: ^0.294.0

### Utilities

- `axios`: ^1.6.2
- `react-hot-toast`: ^2.4.1

### Dev Tools

- `vite`: ^5.0.8
- `@vitejs/plugin-react`: ^4.2.1
- `autoprefixer`: ^10.4.16
- `postcss`: ^8.4.32

## 🐛 Troubleshooting

### Port already in use

```powershell
# Change port in vite.config.js
server: {
  port: 3000  # or any other port
}
```

### API connection failed

- Ensure backend is running on port 8000
- Check CORS configuration in backend
- Verify API URL in .env file

### Build fails

```powershell
# Clear node_modules and reinstall
rm -rf node_modules
npm install
```

## 🚀 Deployment

### Build for Production

```powershell
npm run build
```

Output will be in `dist/` directory.

### Deploy to Static Hosting

The built files can be deployed to:

- Vercel
- Netlify
- GitHub Pages
- AWS S3
- Any static hosting service

## 📝 License

MIT License

## 👥 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions:

- Check the documentation
- Review API documentation at http://localhost:8000/docs
- Open an issue on GitHub
