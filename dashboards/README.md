# TForce Dashboards - Frontend Development

Complete dashboard solution for TForce Logistics AI-Powered Delivery Quality system.

## 📁 What's Inside

```
dashboards/
├── wireframes/                          # Detailed dashboard wireframes
│   ├── operations-manager-dashboard.md  # Fleet oversight dashboard
│   ├── delivery-driver-dashboard.md     # Driver performance dashboard
│   ├── customer-service-dashboard.md    # Proactive CS dashboard
│   ├── DASHBOARD-COMPARISON.md          # Side-by-side comparison
│   └── README.md                        # Wireframes overview
│
├── FRONTEND-DEVELOPMENT-GUIDE.md        # Comprehensive dev guide
├── package.json.template                # NPM dependencies template
├── bootstrap.sh                         # Quick setup script
└── README.md                            # This file
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

Run the bootstrap script to automatically set up your development environment:

```bash
cd /Users/zhizhyan/Desktop/Codex/dashboards
./bootstrap.sh
```

This script will:
- ✅ Create a Vite + React + TypeScript project
- ✅ Install all dependencies (React Query, Zustand, Tailwind, etc.)
- ✅ Set up shadcn/ui with common components
- ✅ Create complete project structure
- ✅ Generate configuration files (.env, tsconfig, vite.config)
- ✅ Create starter files (API client, configs, routes)

**Time: ~5 minutes** ⏱️

### Option 2: Manual Setup

Follow the step-by-step guide in `FRONTEND-DEVELOPMENT-GUIDE.md`.

---

## 📊 Dashboard Overview

### 1. Operations Manager Dashboard
**Business Impact**: $2-5M annual savings

**Key Features**:
- Daily fleet quality summary
- Real-time critical alerts
- Driver performance rankings
- Geographic problem areas
- Action queue management

**Tech Stack**: React + React Query + WebSocket + Recharts

---

### 2. Delivery Driver Dashboard  
**Business Impact**: 20-30% performance improvement

**Key Features**:
- Personal quality score
- AI-powered delivery feedback
- Weekly progress tracking
- Achievement badges (gamification)
- Learning center

**Tech Stack**: React PWA + React Query + Service Workers

---

### 3. Customer Service Dashboard
**Business Impact**: 15-25% complaint reduction

**Key Features**:
- At-risk delivery detection
- Proactive customer outreach
- Prevention rate analytics
- Communication activity log

**Tech Stack**: React + React Query + WebSocket + Communication APIs

---

## 🛠️ Technology Stack

### Core
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **Routing**: React Router v6

### State Management
- **Server State**: TanStack React Query (data fetching, caching)
- **Client State**: Zustand (UI state, alerts)

### UI & Styling
- **CSS Framework**: Tailwind CSS 3
- **Component Library**: shadcn/ui (Radix UI primitives)
- **Icons**: Heroicons + Lucide React

### Data Visualization
- **Charts**: Recharts (primary) + D3.js (complex visualizations)

### Real-time
- **WebSocket**: Socket.IO Client (real-time alerts)

### Mobile (Driver Dashboard)
- **PWA**: Vite PWA Plugin
- **Offline**: Service Workers + IndexedDB

### Testing
- **Test Runner**: Vitest
- **Testing Library**: React Testing Library

---

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm 9+

### Setup Steps

```bash
# 1. Run bootstrap script
cd /Users/zhizhyan/Desktop/Codex/dashboards
./bootstrap.sh

# 2. Navigate to project
cd frontend

# 3. Configure environment
cp .env.example .env.local
# Edit .env.local with your API endpoints

# 4. Start development server
npm run dev

# 5. Open browser
# http://localhost:5173
```

---

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── pages/                    # Dashboard pages
│   │   ├── OperationsManager/    # Ops Manager dashboard
│   │   ├── Driver/               # Driver dashboard
│   │   └── CustomerService/      # CS dashboard
│   │
│   ├── components/               # Shared components
│   │   ├── ui/                   # shadcn/ui components
│   │   ├── charts/               # Chart components
│   │   ├── metrics/              # Metric cards
│   │   └── alerts/               # Alert components
│   │
│   ├── hooks/                    # Custom React hooks
│   │   ├── useFleetData.ts       # Fleet data fetching
│   │   ├── useDriverData.ts      # Driver data fetching
│   │   └── useRealtimeAlerts.ts  # WebSocket alerts
│   │
│   ├── services/                 # API & external services
│   │   ├── api/                  # REST API clients
│   │   ├── websocket/            # WebSocket client
│   │   └── storage/              # Local storage
│   │
│   ├── store/                    # Zustand stores
│   ├── types/                    # TypeScript types
│   ├── utils/                    # Utility functions
│   └── config/                   # Configuration
│
├── public/                       # Static assets
├── .env.local                    # Environment variables
└── vite.config.ts                # Vite configuration
```

---

## 🧪 Development Commands

```bash
# Start dev server
npm run dev

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

---

## 📱 Progressive Web App (Driver Dashboard)

The Driver dashboard is built as a PWA for optimal mobile experience:

**Features**:
- ✅ Install to home screen
- ✅ Offline access (cached data)
- ✅ Push notifications
- ✅ Fast load times
- ✅ Mobile-optimized UI

**Testing PWA**:
```bash
# Build production version
npm run build

# Preview with PWA features
npm run preview

# Open in mobile browser or use Chrome DevTools mobile emulation
```

---

## 🔌 API Integration

### Environment Variables

Configure your API endpoints in `.env.local`:

```bash
VITE_API_BASE_URL=https://api.tforce.com/v1
VITE_WEBSOCKET_URL=wss://api.tforce.com
VITE_PHOTO_BUCKET_URL=https://objectstorage...
```

### API Endpoints

The frontend expects these backend endpoints:

**Fleet (Operations Manager)**:
- `GET /fleet/daily-summary?date=YYYY-MM-DD`
- `GET /fleet/quality-distribution?date=YYYY-MM-DD`
- `GET /fleet/top-performers?date=YYYY-MM-DD`
- `GET /fleet/problem-areas?date=YYYY-MM-DD`
- `GET /fleet/action-queue`

**Driver**:
- `GET /driver/:id/daily-performance?date=YYYY-MM-DD`
- `GET /driver/:id/weekly-trend?end_date=YYYY-MM-DD`
- `GET /driver/:id/achievements`
- `GET /driver/:id/goals`

**Customer Service**:
- `GET /cs/prevention-summary?date=YYYY-MM-DD`
- `GET /cs/at-risk-deliveries?priority=high&status=new`
- `GET /cs/prevention-trend?days=28`
- `POST /cs/contact/:delivery_id`

**WebSocket**:
- `/alerts/critical` - Real-time critical alerts
- `/cs/at-risk-stream` - At-risk delivery stream

---

## 🎨 Customization

### Branding

Update brand colors in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      tforce: {
        primary: '#0ea5e9',    // Your primary brand color
        secondary: '#64748b',  // Secondary color
      }
    }
  }
}
```

### Features

Toggle features via environment variables:

```bash
VITE_ENABLE_REALTIME_ALERTS=true   # Enable/disable WebSocket alerts
VITE_ENABLE_OFFLINE_MODE=true      # Enable/disable PWA offline mode
```

---

## 📈 Performance Optimization

### Code Splitting
- Lazy load dashboard pages
- Dynamic imports for heavy components

### Image Optimization
- Use WebP format
- Lazy loading for delivery photos
- Signed URLs from OCI Object Storage

### Caching Strategy
- React Query: 24-hour cache for batch data
- Service Worker: 7-day cache for photos
- IndexedDB: Offline data storage

---

## 🚀 Deployment

### Build

```bash
npm run build
```

Output in `dist/` directory.

### Deploy to OCI Object Storage (Static Hosting)

```bash
# Install OCI CLI
brew install oci-cli  # macOS

# Configure OCI CLI
oci setup config

# Upload to Object Storage
oci os object bulk-upload \
  --bucket-name tforce-dashboards-prod \
  --src-dir ./dist \
  --content-type-overrides '{"html":"text/html","js":"application/javascript","css":"text/css"}'

# Set bucket to public (if needed)
oci os bucket update \
  --bucket-name tforce-dashboards-prod \
  --public-access-type ObjectRead
```

### Deploy to OCI Container Instances

```bash
# Build Docker image
docker build -t tforce-dashboards .

# Tag for OCI Registry
docker tag tforce-dashboards:latest \
  <region>.ocir.io/<namespace>/tforce-dashboards:latest

# Push to OCI Registry
docker push <region>.ocir.io/<namespace>/tforce-dashboards:latest

# Deploy container instance
oci container-instances container-instance create \
  --compartment-id <compartment-ocid> \
  --availability-domain <AD> \
  --shape CI.Standard.E4.Flex \
  --containers file://container-config.json
```

---

## 📚 Documentation

- **Wireframes**: See `wireframes/` directory for detailed dashboard specs
- **Development Guide**: `FRONTEND-DEVELOPMENT-GUIDE.md` for comprehensive guide
- **API Reference**: Backend API documentation (link to be added)
- **Component Library**: shadcn/ui docs - https://ui.shadcn.com

---

## 🐛 Troubleshooting

### Common Issues

**1. Module not found: Can't resolve '@/...'**
```bash
# Restart dev server after installing new packages
npm run dev
```

**2. WebSocket connection failed**
```bash
# Check VITE_WEBSOCKET_URL in .env.local
# Ensure backend WebSocket server is running
```

**3. Photos not loading**
```bash
# Verify VITE_PHOTO_BUCKET_URL is correct
# Check OCI Object Storage permissions
# Ensure signed URL generation is working
```

**4. PWA not updating**
```bash
# Clear cache in browser
# Rebuild: npm run build
# Hard refresh: Cmd+Shift+R (Mac) / Ctrl+Shift+R (Windows)
```

---

## 🤝 Contributing

### Code Style

- Use TypeScript for type safety
- Follow Prettier formatting (auto-format on save)
- Use ESLint rules (no warnings)
- Write tests for critical components

### Commit Guidelines

```bash
# Format: <type>: <description>

feat: add weekly trend chart to driver dashboard
fix: correct quality score calculation
docs: update API integration guide
style: format code with prettier
test: add tests for MetricCard component
```

---

## 📊 Success Metrics

### Performance Targets
- Load time: < 2 seconds (first contentful paint)
- Time to Interactive: < 3 seconds
- Lighthouse Score: > 90

### Business Targets
- Dashboard adoption: > 80% (Ops), > 75% (Drivers), > 85% (CS)
- User satisfaction: > 4.5/5.0
- Bug rate: < 1% of users affected

---

## 🎯 Roadmap

### Phase 1: MVP (Completed via bootstrap.sh)
- ✅ Project setup
- ✅ Component library
- ✅ API integration
- ✅ Basic routing

### Phase 2: Core Dashboards (4 weeks)
- [ ] Operations Manager dashboard
- [ ] Driver dashboard
- [ ] Customer Service dashboard

### Phase 3: Real-time Features (2 weeks)
- [ ] WebSocket integration
- [ ] Alert notifications
- [ ] Live updates

### Phase 4: PWA & Mobile (2 weeks)
- [ ] Service Worker setup
- [ ] Offline support
- [ ] Push notifications

### Phase 5: Polish & Launch (2 weeks)
- [ ] Performance optimization
- [ ] User testing
- [ ] Documentation
- [ ] Production deployment

---

## 📞 Support

- **Documentation**: `FRONTEND-DEVELOPMENT-GUIDE.md`
- **Wireframes**: `wireframes/README.md`
- **Issues**: Create GitHub issue (if using version control)

---

## 📄 License

Proprietary - TForce Logistics © 2025

---

**Ready to build amazing dashboards! 🚀**

