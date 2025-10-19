#!/bin/bash

# TForce Dashboards - Quick Bootstrap Script
# This script sets up the frontend development environment

set -e  # Exit on error

echo "🚀 TForce Dashboards - Quick Setup"
echo "=================================="
echo ""

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Error: Node.js 18+ required. Current version: $(node -v)"
    exit 1
fi
echo "✅ Node.js version: $(node -v)"

# Step 1: Create project with Vite
echo ""
echo "📦 Step 1: Creating Vite + React + TypeScript project..."
npm create vite@latest frontend -- --template react-ts

cd frontend

# Step 2: Install dependencies
echo ""
echo "📦 Step 2: Installing dependencies..."
npm install

# Core dependencies
npm install @tanstack/react-query @tanstack/react-query-devtools zustand
npm install recharts d3 @types/d3
npm install axios socket.io-client
npm install date-fns clsx tailwind-merge
npm install react-router-dom
npm install @heroicons/react lucide-react
npm install vite-plugin-pwa workbox-window

# Dev dependencies
npm install -D @types/node
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
npm install -D prettier prettier-plugin-tailwindcss

# Step 3: Initialize Tailwind CSS
echo ""
echo "🎨 Step 3: Setting up Tailwind CSS..."
npm install -D tailwindcss postcss autoprefixer tailwindcss-animate
npx tailwindcss init -p

# Step 4: Initialize shadcn/ui
echo ""
echo "🎨 Step 4: Setting up shadcn/ui..."
npx shadcn-ui@latest init -y

# Install commonly used shadcn components
echo "📦 Installing shadcn/ui components..."
npx shadcn-ui@latest add button -y
npx shadcn-ui@latest add card -y
npx shadcn-ui@latest add badge -y
npx shadcn-ui@latest add dialog -y
npx shadcn-ui@latest add dropdown-menu -y
npx shadcn-ui@latest add tabs -y
npx shadcn-ui@latest add table -y
npx shadcn-ui@latest add alert -y
npx shadcn-ui@latest add toast -y

# Step 5: Create directory structure
echo ""
echo "📁 Step 5: Creating project structure..."
mkdir -p src/pages/{OperationsManager,Driver,CustomerService}/components
mkdir -p src/components/{ui,layout,charts,metrics,alerts,common}
mkdir -p src/hooks
mkdir -p src/services/{api,websocket,storage}
mkdir -p src/store
mkdir -p src/types
mkdir -p src/utils
mkdir -p src/config
mkdir -p src/assets/{icons,images,fonts}
mkdir -p public/{icons,sounds}

echo "✅ Created directory structure"

# Step 6: Create configuration files
echo ""
echo "⚙️  Step 6: Creating configuration files..."

# Create .env.example
cat > .env.example << 'EOF'
# API Configuration
VITE_API_BASE_URL=http://localhost:3000/api/v1
VITE_WEBSOCKET_URL=ws://localhost:3000

# OCI Object Storage
VITE_PHOTO_BUCKET_URL=https://objectstorage.us-phoenix-1.oraclecloud.com/...

# Feature Flags
VITE_ENABLE_REALTIME_ALERTS=true
VITE_ENABLE_OFFLINE_MODE=true

# Environment
VITE_ENV=development
EOF

# Create .env.local
cp .env.example .env.local

# Create prettier config
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "plugins": ["prettier-plugin-tailwindcss"]
}
EOF

# Create .prettierignore
cat > .prettierignore << 'EOF'
node_modules
dist
build
.next
coverage
EOF

# Update tsconfig.json with path alias
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path Alias */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOF

# Update vite.config.ts
cat > vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'
import path from 'path'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png'],
      manifest: {
        name: 'TForce Driver Portal',
        short_name: 'TForce',
        description: 'Personal performance dashboard for TForce drivers',
        theme_color: '#0ea5e9',
        background_color: '#ffffff',
        display: 'standalone',
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
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
EOF

# Create vitest.config.ts
cat > vitest.config.ts << 'EOF'
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

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
})
EOF

# Create test setup
mkdir -p src/test
cat > src/test/setup.ts << 'EOF'
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';

afterEach(() => {
  cleanup();
});
EOF

echo "✅ Created configuration files"

# Step 7: Create starter files
echo ""
echo "📝 Step 7: Creating starter files..."

# Create API config
cat > src/config/api.config.ts << 'EOF'
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

export const WS_CONFIG = {
  url: import.meta.env.VITE_WEBSOCKET_URL || 'ws://localhost:3000',
  reconnectDelay: 3000,
  maxReconnectAttempts: 5,
};

export const ENDPOINTS = {
  fleet: {
    dailySummary: '/fleet/daily-summary',
    qualityDistribution: '/fleet/quality-distribution',
    topPerformers: '/fleet/top-performers',
  },
  driver: {
    dailyPerformance: (driverId: string) => `/driver/${driverId}/daily-performance`,
    weeklyTrend: (driverId: string) => `/driver/${driverId}/weekly-trend`,
  },
  cs: {
    preventionSummary: '/cs/prevention-summary',
    atRiskDeliveries: '/cs/at-risk-deliveries',
  },
};
EOF

# Create API client
cat > src/services/api/client.ts << 'EOF'
import axios from 'axios';
import { API_CONFIG } from '@/config/api.config';

export const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: API_CONFIG.headers,
});

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

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
EOF

# Create main.tsx with React Query
cat > src/main.tsx << 'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import App from './App.tsx'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      cacheTime: 10 * 60 * 1000,
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>,
)
EOF

# Create basic App.tsx
cat > src/App.tsx << 'EOF'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/operations" replace />} />
        <Route path="/operations" element={<div className="p-8"><h1 className="text-3xl font-bold">Operations Manager Dashboard</h1><p className="text-gray-600 mt-2">Coming soon...</p></div>} />
        <Route path="/driver" element={<div className="p-8"><h1 className="text-3xl font-bold">Driver Dashboard</h1><p className="text-gray-600 mt-2">Coming soon...</p></div>} />
        <Route path="/cs" element={<div className="p-8"><h1 className="text-3xl font-bold">Customer Service Dashboard</h1><p className="text-gray-600 mt-2">Coming soon...</p></div>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
EOF

echo "✅ Created starter files"

# Step 8: Format index.css for Tailwind
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 199 89% 48%;
    --primary-foreground: 210 40% 98%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📂 Project location: $(pwd)"
echo ""
echo "🚀 Next steps:"
echo "   1. cd frontend"
echo "   2. npm run dev"
echo "   3. Open http://localhost:5173"
echo ""
echo "📚 Documentation:"
echo "   - Frontend Guide: ../FRONTEND-DEVELOPMENT-GUIDE.md"
echo "   - Wireframes: ../wireframes/"
echo ""
echo "Happy coding! 🎉"

