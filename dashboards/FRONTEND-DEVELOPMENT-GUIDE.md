# Frontend Development Guide - TForce Dashboards

This guide provides a practical roadmap for developing the three priority dashboards with modern, maintainable, and scalable architecture.

## 🎯 Recommended Technology Stack

### Core Framework
**React 18+ with TypeScript**

**Why?**
- Component reusability across all three dashboards
- Strong typing reduces bugs in complex data flows
- Excellent ecosystem for charts, real-time updates, and PWA
- Team familiarity and strong community support

### State Management
**React Query (TanStack Query) + Zustand**

**Why?**
- **React Query**: Perfect for server state (batch data, API calls)
  - Built-in caching (perfect for daily batch data)
  - Automatic refetching and background updates
  - Optimistic updates for real-time feel
- **Zustand**: Lightweight client state (UI state, filters, alerts)
  - Simpler than Redux for smaller state needs
  - Great for real-time alert management

### Styling
**Tailwind CSS + shadcn/ui Components**

**Why?**
- Rapid development with utility-first CSS
- Consistent design system out of the box
- shadcn/ui provides beautiful, accessible components
- Easy to customize for TForce branding
- Responsive design built-in

### Charts & Visualization
**Recharts + D3.js (selectively)**

**Why?**
- **Recharts**: React-native charts, easy to use, covers 80% of needs
  - Line charts, bar charts, pie charts
  - Responsive and customizable
- **D3.js**: For complex visualizations (geographic maps, custom charts)
  - Use sparingly (steeper learning curve)
  - Better for custom geographic heatmaps

### Real-time Updates
**WebSocket (native) or Socket.IO**

**Why?**
- Native WebSocket for simplicity if backend supports
- Socket.IO for fallback support (long polling)
- React Query integrates well with real-time data

### Mobile (Driver Dashboard)
**Progressive Web App (PWA) with Vite PWA Plugin**

**Why?**
- Single codebase (same React app)
- Offline support via Service Workers
- Push notifications
- Install on home screen
- No app store approval needed

---

## 📁 Recommended Project Structure

```
tforce-dashboards/
├── .env.example                    # Environment variables template
├── .env.local                      # Local development env vars
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts                  # Vite configuration
├── tailwind.config.js
├── index.html
│
├── public/
│   ├── icons/                      # PWA icons
│   ├── manifest.json               # PWA manifest
│   └── service-worker.js           # Service worker (auto-generated)
│
└── src/
    ├── main.tsx                    # Application entry point
    ├── App.tsx                     # Root component with routing
    │
    ├── pages/                      # Page-level components
    │   ├── OperationsManager/
    │   │   ├── index.tsx           # Operations Manager dashboard
    │   │   └── components/         # Page-specific components
    │   │       ├── DailySummary.tsx
    │   │       ├── CriticalAlerts.tsx
    │   │       ├── QualityDistribution.tsx
    │   │       ├── TopPerformers.tsx
    │   │       ├── DamagePrevention.tsx
    │   │       ├── ProblemAreas.tsx
    │   │       └── ActionQueue.tsx
    │   │
    │   ├── Driver/
    │   │   ├── index.tsx           # Driver dashboard
    │   │   └── components/
    │   │       ├── PerformanceCard.tsx
    │   │       ├── ScoreBreakdown.tsx
    │   │       ├── BestDelivery.tsx
    │   │       ├── ImprovementArea.tsx
    │   │       ├── WeeklyProgress.tsx
    │   │       ├── Achievements.tsx
    │   │       ├── TodaysGoals.tsx
    │   │       └── LearningCenter.tsx
    │   │
    │   └── CustomerService/
    │       ├── index.tsx           # CS dashboard
    │       └── components/
    │           ├── PreventionMetrics.tsx
    │           ├── AtRiskQueue.tsx
    │           ├── AtRiskCard.tsx
    │           ├── PreventionAnalytics.tsx
    │           ├── ImpactMetrics.tsx
    │           ├── QualityCorrelation.tsx
    │           ├── ActivityFeed.tsx
    │           └── CommunicationLog.tsx
    │
    ├── components/                 # Shared components
    │   ├── ui/                     # shadcn/ui components
    │   │   ├── button.tsx
    │   │   ├── card.tsx
    │   │   ├── badge.tsx
    │   │   ├── dialog.tsx
    │   │   ├── dropdown-menu.tsx
    │   │   └── ...
    │   │
    │   ├── layout/
    │   │   ├── Header.tsx
    │   │   ├── Sidebar.tsx
    │   │   └── Layout.tsx
    │   │
    │   ├── charts/                 # Reusable chart components
    │   │   ├── LineChart.tsx
    │   │   ├── BarChart.tsx
    │   │   ├── TrendChart.tsx
    │   │   └── GeographicMap.tsx
    │   │
    │   ├── metrics/                # Metric display components
    │   │   ├── MetricCard.tsx
    │   │   ├── TrendIndicator.tsx
    │   │   └── ProgressBar.tsx
    │   │
    │   ├── alerts/
    │   │   ├── AlertCard.tsx
    │   │   ├── AlertBadge.tsx
    │   │   └── AlertNotification.tsx
    │   │
    │   └── common/
    │       ├── Loading.tsx
    │       ├── ErrorBoundary.tsx
    │       ├── EmptyState.tsx
    │       └── PhotoViewer.tsx
    │
    ├── hooks/                      # Custom React hooks
    │   ├── useFleetData.ts         # Ops Manager data
    │   ├── useDriverData.ts        # Driver data
    │   ├── useCustomerServiceData.ts # CS data
    │   ├── useRealtimeAlerts.ts    # WebSocket hook
    │   ├── usePhotoLoader.ts       # Photo loading logic
    │   └── useOfflineSync.ts       # PWA offline sync
    │
    ├── services/                   # API and external services
    │   ├── api/
    │   │   ├── client.ts           # Axios/Fetch wrapper
    │   │   ├── fleet.ts            # Fleet API endpoints
    │   │   ├── driver.ts           # Driver API endpoints
    │   │   ├── customerService.ts  # CS API endpoints
    │   │   └── photos.ts           # Photo URL signing
    │   │
    │   ├── websocket/
    │   │   ├── client.ts           # WebSocket client
    │   │   ├── alerts.ts           # Alert stream handlers
    │   │   └── reconnect.ts        # Reconnection logic
    │   │
    │   └── storage/
    │       ├── cache.ts            # IndexedDB for offline
    │       └── preferences.ts      # User preferences
    │
    ├── store/                      # Zustand stores
    │   ├── alertStore.ts           # Real-time alerts state
    │   ├── uiStore.ts              # UI state (filters, modals)
    │   └── authStore.ts            # User authentication state
    │
    ├── types/                      # TypeScript type definitions
    │   ├── fleet.types.ts
    │   ├── driver.types.ts
    │   ├── customerService.types.ts
    │   ├── alerts.types.ts
    │   └── api.types.ts
    │
    ├── utils/                      # Utility functions
    │   ├── formatters.ts           # Date, number formatting
    │   ├── calculations.ts         # Quality score calculations
    │   ├── validators.ts           # Data validation
    │   └── constants.ts            # App-wide constants
    │
    ├── config/                     # Configuration files
    │   ├── api.config.ts           # API endpoints
    │   ├── charts.config.ts        # Chart default configs
    │   └── theme.config.ts         # Theme customization
    │
    └── assets/                     # Static assets
        ├── icons/
        ├── images/
        └── fonts/
```

---

## 🚀 Getting Started - Step by Step

### Step 1: Initialize Project

```bash
# Create Vite + React + TypeScript project
npm create vite@latest tforce-dashboards -- --template react-ts

cd tforce-dashboards

# Install core dependencies
npm install

# Install additional dependencies
npm install @tanstack/react-query zustand
npm install recharts d3 @types/d3
npm install tailwindcss postcss autoprefixer
npm install axios date-fns clsx tailwind-merge
npm install socket.io-client
npm install vite-plugin-pwa workbox-window

# Install shadcn/ui
npx shadcn-ui@latest init

# Install dev dependencies
npm install -D @types/node
```

### Step 2: Configure Tailwind CSS

```bash
npx tailwindcss init -p
```

**tailwind.config.js**:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // TForce brand colors
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
        // Add more custom colors
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

### Step 3: Set Up Environment Variables

**.env.example**:
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:3000/api/v1
VITE_WEBSOCKET_URL=ws://localhost:3000

# OCI Object Storage
VITE_PHOTO_BUCKET_URL=https://objectstorage.us-phoenix-1.oraclecloud.com/...

# Feature Flags
VITE_ENABLE_REALTIME_ALERTS=true
VITE_ENABLE_OFFLINE_MODE=true

# Analytics (optional)
VITE_ANALYTICS_ID=UA-XXXXXXXX-X
```

### Step 4: Create Base Configuration

**src/config/api.config.ts**:
```typescript
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

export const WS_CONFIG = {
  url: import.meta.env.VITE_WEBSOCKET_URL,
  reconnectDelay: 3000,
  maxReconnectAttempts: 5,
};

export const ENDPOINTS = {
  // Operations Manager
  fleet: {
    dailySummary: '/fleet/daily-summary',
    qualityDistribution: '/fleet/quality-distribution',
    topPerformers: '/fleet/top-performers',
    problemAreas: '/fleet/problem-areas',
    actionQueue: '/fleet/action-queue',
  },
  
  // Driver
  driver: {
    dailyPerformance: (driverId: string) => `/driver/${driverId}/daily-performance`,
    weeklyTrend: (driverId: string) => `/driver/${driverId}/weekly-trend`,
    achievements: (driverId: string) => `/driver/${driverId}/achievements`,
    goals: (driverId: string) => `/driver/${driverId}/goals`,
  },
  
  // Customer Service
  cs: {
    preventionSummary: '/cs/prevention-summary',
    atRiskDeliveries: '/cs/at-risk-deliveries',
    preventionTrend: '/cs/prevention-trend',
    communicationLog: '/cs/communication-log',
    contact: (deliveryId: string) => `/cs/contact/${deliveryId}`,
  },
  
  // Shared
  photos: {
    signedUrl: (deliveryId: string) => `/photos/${deliveryId}/signed-url`,
  },
  
  // WebSocket
  ws: {
    criticalAlerts: '/alerts/critical',
    atRiskStream: '/cs/at-risk-stream',
  },
};
```

---

## 🛠️ Development Workflow

### Phase 1: Foundation (Week 1)

**1. Set up project structure**
```bash
# Create all directories
mkdir -p src/{pages,components,hooks,services,store,types,utils,config,assets}
mkdir -p src/components/{ui,layout,charts,metrics,alerts,common}
mkdir -p src/pages/{OperationsManager,Driver,CustomerService}
```

**2. Install shadcn/ui components**
```bash
# Install commonly used components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add table
npx shadcn-ui@latest add alert
```

**3. Create type definitions**

**src/types/fleet.types.ts**:
```typescript
export interface FleetDailySummary {
  date: string;
  totalDeliveries: number;
  qualityPassRate: number;
  costSavings: number;
  totalIssues: number;
  weekOverWeek: {
    deliveries: number;
    qualityPass: number;
    costSavings: number;
    issues: number;
  };
}

export interface QualityDistribution {
  excellent: { count: number; percentage: number };
  good: { count: number; percentage: number };
  review: { count: number; percentage: number };
  poor: { count: number; percentage: number };
}

export interface TopPerformer {
  driverId: string;
  score: number;
  deliveries: number;
}

// ... more types
```

**4. Set up API client**

**src/services/api/client.ts**:
```typescript
import axios from 'axios';
import { API_CONFIG } from '@/config/api.config';

export const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: API_CONFIG.headers,
});

// Request interceptor (add auth token)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (handle errors)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### Phase 2: Shared Components (Week 2)

**1. Create MetricCard component**

**src/components/metrics/MetricCard.tsx**:
```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendIndicator } from './TrendIndicator';

interface MetricCardProps {
  title: string;
  value: string | number;
  trend?: {
    value: number;
    direction: 'up' | 'down';
    isPositive: boolean;
  };
  icon?: React.ReactNode;
  className?: string;
}

export function MetricCard({ title, value, trend, icon, className }: MetricCardProps) {
  return (
    <Card className={className}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">
          {title}
        </CardTitle>
        {icon && <div className="text-gray-400">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">{value}</div>
        {trend && (
          <TrendIndicator
            value={trend.value}
            direction={trend.direction}
            isPositive={trend.isPositive}
          />
        )}
      </CardContent>
    </Card>
  );
}
```

**2. Create chart components**

**src/components/charts/TrendChart.tsx**:
```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface TrendChartProps {
  data: Array<{ date: string; value: number }>;
  color?: string;
  height?: number;
}

export function TrendChart({ data, color = '#0ea5e9', height = 300 }: TrendChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis 
          dataKey="date" 
          stroke="#6b7280"
          fontSize={12}
        />
        <YAxis 
          stroke="#6b7280"
          fontSize={12}
        />
        <Tooltip 
          contentStyle={{
            backgroundColor: '#fff',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
          }}
        />
        <Line 
          type="monotone" 
          dataKey="value" 
          stroke={color} 
          strokeWidth={2}
          dot={{ fill: color, r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Phase 3: Data Fetching with React Query (Week 2)

**1. Set up React Query**

**src/main.tsx**:
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import App from './App';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>
);
```

**2. Create custom hooks**

**src/hooks/useFleetData.ts**:
```typescript
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { getFleetDailySummary, getQualityDistribution } from '@/services/api/fleet';
import type { FleetDailySummary, QualityDistribution } from '@/types/fleet.types';

export function useFleetDailySummary(date: Date = new Date()) {
  const dateStr = format(date, 'yyyy-MM-dd');
  
  return useQuery<FleetDailySummary>({
    queryKey: ['fleet', 'daily-summary', dateStr],
    queryFn: () => getFleetDailySummary(dateStr),
    // Refresh data every 24 hours (since it's batch processed)
    staleTime: 24 * 60 * 60 * 1000,
  });
}

export function useQualityDistribution(date: Date = new Date()) {
  const dateStr = format(date, 'yyyy-MM-dd');
  
  return useQuery<QualityDistribution>({
    queryKey: ['fleet', 'quality-distribution', dateStr],
    queryFn: () => getQualityDistribution(dateStr),
    staleTime: 24 * 60 * 60 * 1000,
  });
}
```

**src/services/api/fleet.ts**:
```typescript
import { apiClient } from './client';
import { ENDPOINTS } from '@/config/api.config';
import type { FleetDailySummary, QualityDistribution } from '@/types/fleet.types';

export async function getFleetDailySummary(date: string): Promise<FleetDailySummary> {
  const response = await apiClient.get(ENDPOINTS.fleet.dailySummary, {
    params: { date },
  });
  return response.data;
}

export async function getQualityDistribution(date: string): Promise<QualityDistribution> {
  const response = await apiClient.get(ENDPOINTS.fleet.qualityDistribution, {
    params: { date },
  });
  return response.data;
}
```

### Phase 4: Real-time Alerts (Week 3)

**1. Create WebSocket hook**

**src/hooks/useRealtimeAlerts.ts**:
```typescript
import { useEffect, useState } from 'react';
import { useAlertStore } from '@/store/alertStore';
import { createWebSocketClient } from '@/services/websocket/client';
import type { Alert } from '@/types/alerts.types';

export function useRealtimeAlerts(endpoint: string) {
  const [isConnected, setIsConnected] = useState(false);
  const addAlert = useAlertStore((state) => state.addAlert);

  useEffect(() => {
    const ws = createWebSocketClient(endpoint);

    ws.on('connect', () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    });

    ws.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    });

    ws.on('alert', (alert: Alert) => {
      console.log('New alert received:', alert);
      addAlert(alert);
      
      // Play sound for critical alerts
      if (alert.severity === 'critical') {
        playAlertSound();
      }
      
      // Show browser notification
      if (Notification.permission === 'granted') {
        new Notification('TForce Alert', {
          body: alert.details.message,
          icon: '/icons/alert.png',
        });
      }
    });

    return () => {
      ws.disconnect();
    };
  }, [endpoint, addAlert]);

  return { isConnected };
}

function playAlertSound() {
  const audio = new Audio('/sounds/alert.mp3');
  audio.play().catch(console.error);
}
```

**2. Create Zustand store for alerts**

**src/store/alertStore.ts**:
```typescript
import { create } from 'zustand';
import type { Alert } from '@/types/alerts.types';

interface AlertStore {
  alerts: Alert[];
  addAlert: (alert: Alert) => void;
  removeAlert: (alertId: string) => void;
  clearAlerts: () => void;
}

export const useAlertStore = create<AlertStore>((set) => ({
  alerts: [],
  
  addAlert: (alert) =>
    set((state) => ({
      alerts: [alert, ...state.alerts],
    })),
  
  removeAlert: (alertId) =>
    set((state) => ({
      alerts: state.alerts.filter((a) => a.alertId !== alertId),
    })),
  
  clearAlerts: () => set({ alerts: [] }),
}));
```

### Phase 5: Build Pages (Weeks 4-6)

**Example: Operations Manager Dashboard**

**src/pages/OperationsManager/index.tsx**:
```typescript
import { DailySummary } from './components/DailySummary';
import { CriticalAlerts } from './components/CriticalAlerts';
import { QualityDistribution } from './components/QualityDistribution';
import { TopPerformers } from './components/TopPerformers';
import { DamagePrevention } from './components/DamagePrevention';
import { ProblemAreas } from './components/ProblemAreas';
import { ActionQueue } from './components/ActionQueue';
import { useRealtimeAlerts } from '@/hooks/useRealtimeAlerts';
import { ENDPOINTS } from '@/config/api.config';

export default function OperationsManagerDashboard() {
  // Set up real-time alerts
  const { isConnected } = useRealtimeAlerts(ENDPOINTS.ws.criticalAlerts);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            🚚 TForce Quality Control
          </h1>
          <p className="text-gray-600">Operations Manager Dashboard</p>
        </div>

        {/* Daily Summary */}
        <DailySummary />

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          {/* Left Column (2/3) */}
          <div className="lg:col-span-2 space-y-6">
            <CriticalAlerts isConnected={isConnected} />
            <QualityDistribution />
            <TopPerformers />
          </div>

          {/* Right Column (1/3) */}
          <div className="space-y-6">
            <DamagePrevention />
            <ProblemAreas />
          </div>
        </div>

        {/* Action Queue */}
        <div className="mt-6">
          <ActionQueue />
        </div>
      </div>
    </div>
  );
}
```

**src/pages/OperationsManager/components/DailySummary.tsx**:
```typescript
import { MetricCard } from '@/components/metrics/MetricCard';
import { useFleetDailySummary } from '@/hooks/useFleetData';
import { subDays } from 'date-fns';
import { TruckIcon, CheckCircleIcon, CurrencyDollarIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

export function DailySummary() {
  const yesterday = subDays(new Date(), 1);
  const { data, isLoading, error } = useFleetDailySummary(yesterday);

  if (isLoading) return <DailySummarySkeleton />;
  if (error) return <ErrorMessage />;
  if (!data) return null;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-700 mb-4">
        📊 Yesterday's Performance
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Deliveries"
          value={data.totalDeliveries.toLocaleString()}
          icon={<TruckIcon className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.deliveries,
            direction: data.weekOverWeek.deliveries >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />
        
        <MetricCard
          title="Quality Pass Rate"
          value={`${data.qualityPassRate}%`}
          icon={<CheckCircleIcon className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.qualityPass,
            direction: data.weekOverWeek.qualityPass >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />
        
        <MetricCard
          title="Cost Savings"
          value={`$${data.costSavings.toLocaleString()}`}
          icon={<CurrencyDollarIcon className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.costSavings,
            direction: data.weekOverWeek.costSavings >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />
        
        <MetricCard
          title="Total Issues"
          value={data.totalIssues}
          icon={<ExclamationTriangleIcon className="h-5 w-5" />}
          trend={{
            value: Math.abs(data.weekOverWeek.issues),
            direction: data.weekOverWeek.issues >= 0 ? 'up' : 'down',
            isPositive: false, // Down is better for issues
          }}
        />
      </div>
    </div>
  );
}

function DailySummarySkeleton() {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
      <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-32 bg-gray-100 rounded"></div>
        ))}
      </div>
    </div>
  );
}
```

---

## 📱 PWA Configuration (Driver Dashboard)

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: 'TForce Driver Portal',
        short_name: 'TForce',
        description: 'Personal performance dashboard for TForce drivers',
        theme_color: '#0ea5e9',
        background_color: '#ffffff',
        display: 'standalone',
        orientation: 'portrait',
        scope: '/',
        start_url: '/driver',
        icons: [
          {
            src: '/icons/icon-192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/icons/icon-512.png',
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
      workbox: {
        // Cache strategy for API calls
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.tforce\.com\/driver\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'driver-data-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 24 * 60 * 60, // 24 hours
              },
            },
          },
          {
            urlPattern: /^https:\/\/objectstorage\..*\.oraclecloud\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'photos-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
              },
            },
          },
        ],
      },
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

---

## 🧪 Testing Strategy

### Unit Tests (Vitest)
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

**vitest.config.ts**:
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

**Example test**:
```typescript
import { render, screen } from '@testing-library/react';
import { MetricCard } from '@/components/metrics/MetricCard';

describe('MetricCard', () => {
  it('renders metric value and title', () => {
    render(
      <MetricCard
        title="Total Deliveries"
        value="1,247"
      />
    );
    
    expect(screen.getByText('Total Deliveries')).toBeInTheDocument();
    expect(screen.getByText('1,247')).toBeInTheDocument();
  });
  
  it('shows trend indicator when provided', () => {
    render(
      <MetricCard
        title="Quality Score"
        value="92.8"
        trend={{ value: 3.2, direction: 'up', isPositive: true }}
      />
    );
    
    expect(screen.getByText(/3.2/)).toBeInTheDocument();
  });
});
```

---

## 📦 Build & Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm run preview  # Preview production build locally
```

### Deploy to OCI
```bash
# Build for production
npm run build

# Deploy to OCI Object Storage (static hosting)
oci os object bulk-upload --bucket-name tforce-dashboards-prod --src-dir ./dist

# Or deploy to OCI Container Instances
docker build -t tforce-dashboards:latest .
docker tag tforce-dashboards:latest <region>.ocir.io/<namespace>/tforce-dashboards:latest
docker push <region>.ocir.io/<namespace>/tforce-dashboards:latest
```

---

## 🎨 Design System Tips

### Color Palette
```typescript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      tforce: {
        primary: '#0ea5e9',
        secondary: '#64748b',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
      },
      quality: {
        excellent: '#10b981',
        good: '#3b82f6',
        review: '#f59e0b',
        poor: '#ef4444',
      }
    }
  }
}
```

### Consistent Spacing
```typescript
// Use Tailwind's spacing scale
<div className="p-6 space-y-4">  // Padding 24px, gap 16px
  <div className="mb-2">...</div>  // Margin bottom 8px
</div>
```

### Typography
```typescript
<h1 className="text-3xl font-bold">Dashboard Title</h1>
<h2 className="text-xl font-semibold">Section Title</h2>
<p className="text-sm text-gray-600">Subtitle</p>
```

---

## ⚡ Performance Optimization

1. **Code Splitting**
```typescript
// Lazy load dashboards
const OperationsManager = lazy(() => import('./pages/OperationsManager'));
const Driver = lazy(() => import('./pages/Driver'));
const CustomerService = lazy(() => import('./pages/CustomerService'));
```

2. **Image Optimization**
```typescript
// Use WebP format, lazy loading
<img 
  src={photoUrl} 
  alt="Delivery" 
  loading="lazy"
  className="object-cover"
/>
```

3. **Memoization**
```typescript
const MemoizedChart = memo(TrendChart);
const memoizedData = useMemo(() => processData(rawData), [rawData]);
```

---

## 📚 Recommended Resources

- **React Query**: https://tanstack.com/query/latest
- **shadcn/ui**: https://ui.shadcn.com
- **Recharts**: https://recharts.org
- **Vite PWA**: https://vite-pwa-org.netlify.app
- **Tailwind CSS**: https://tailwindcss.com

---

## 🚀 Quick Start Checklist

- [ ] Initialize Vite + React + TypeScript project
- [ ] Install dependencies (React Query, Zustand, Tailwind, shadcn/ui)
- [ ] Set up project structure
- [ ] Configure Tailwind CSS
- [ ] Set up environment variables
- [ ] Create API client and configuration
- [ ] Define TypeScript types
- [ ] Build shared components (MetricCard, charts, etc.)
- [ ] Set up React Query provider
- [ ] Create custom hooks for data fetching
- [ ] Implement WebSocket for real-time alerts
- [ ] Build dashboard pages
- [ ] Configure PWA (for Driver dashboard)
- [ ] Set up testing
- [ ] Optimize for production
- [ ] Deploy!

**This approach will give you a modern, maintainable, and scalable frontend that aligns perfectly with your wireframes! 🎉**

