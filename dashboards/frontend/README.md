# TForce Dashboards - Frontend

React + TypeScript + Tailwind CSS application for TForce delivery quality dashboards.

## 🚀 Quick Start

```bash
npm run dev    # Start development server
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## ✅ Step 1 Complete!

### Installed & Configured

- ✅ **React 19** + TypeScript
- ✅ **Vite 7** - Build tool
- ✅ **Tailwind CSS v3** - Styling (fixed PostCSS error)
- ✅ **React Query** - Data fetching & caching
- ✅ **Zustand** - State management
- ✅ **React Router** - Navigation
- ✅ **Recharts + D3.js** - Charts
- ✅ **Axios** - API client
- ✅ **Socket.IO** - WebSocket
- ✅ **Vitest** - Testing
- ✅ **PWA** - Progressive Web App support

### Project Structure

```
src/
├── pages/                    # Dashboard pages
│   ├── OperationsManager/
│   ├── Driver/
│   └── CustomerService/
├── components/               # Shared components
│   ├── ui/                  # shadcn/ui components
│   ├── TestCard.tsx         ✅ Example component
├── hooks/                   # Custom React hooks
├── services/                # API & WebSocket
│   └── api/
│       └── client.ts       ✅ API client ready
├── config/
│   └── api.config.ts       ✅ API endpoints defined
└── lib/
    └── utils.ts            ✅ Utilities
```

## 📝 Scripts

```bash
npm run dev        # Development server
npm run build      # Production build
npm run preview    # Preview production build
npm run test       # Run tests
npm run test:ui    # Run tests with UI
npm run lint       # Lint code
npm run format     # Format with Prettier
```

## 🎨 Custom Tailwind Colors

- `tforce-primary` - #0ea5e9 (TForce brand blue)
- `quality-excellent` - #10b981 (Green for 95-100 scores)
- `quality-good` - #3b82f6 (Blue for 85-94 scores)  
- `quality-review` - #f59e0b (Yellow for 70-84 scores)
- `quality-poor` - #ef4444 (Red for <70 scores)

## 🔧 Configuration

- **Environment**: Edit `.env.local`
- **Tailwind**: `tailwind.config.js`
- **Vite**: `vite.config.ts`
- **TypeScript**: `tsconfig.app.json`

## 📡 API Configuration

Default API endpoint: `http://localhost:3000/api/v1`

Update in `.env.local`:
```bash
VITE_API_BASE_URL=https://your-api.com/api/v1
```

## 🐛 Fixed Issues

- ✅ **PostCSS/Tailwind Error**: Downgraded from Tailwind v4 to v3 for stability

## 🎯 Next Steps

- [ ] Install shadcn/ui components
- [ ] Create shared component library (MetricCard, charts)
- [ ] Build Operations Manager dashboard
- [ ] Add real-time WebSocket alerts
- [ ] Create Driver & CS dashboards

## 📚 Documentation

See parent directory for:
- `../FRONTEND-DEVELOPMENT-GUIDE.md` - Complete development guide
- `../wireframes/` - Dashboard wireframes
