import { AlertCard } from '@/shared/components/alerts/AlertCard';
import { Bell, Wifi, WifiOff, CheckCircle } from 'lucide-react';
import { mockCriticalAlerts } from '@/data/mockData';

interface CriticalAlertsProps {
  isConnected?: boolean;
}

export function CriticalAlerts({ isConnected = true }: CriticalAlertsProps) {
  const alerts = mockCriticalAlerts;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Bell className="h-6 w-6 text-quality-poor" />
          <h3 className="text-gray-900">Critical Alerts</h3>
          <small className="text-gray-500">(Real-time)</small>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-gray-50">
          {isConnected ? (
            <>
              <Wifi className="h-4 w-4 text-quality-excellent" />
              <span className="text-xs font-medium text-quality-excellent">Connected</span>
            </>
          ) : (
            <>
              <WifiOff className="h-4 w-4 text-gray-400" />
              <span className="text-xs font-medium text-gray-600">Disconnected</span>
            </>
          )}
        </div>
      </div>

      <div className="space-y-3">
        {alerts.length > 0 ? (
          alerts.map((alert) => (
            <AlertCard
              key={alert.id}
              severity={alert.severity}
              title={`${alert.type} - Driver #${alert.driver.id}`}
              message={alert.message}
              timestamp={alert.timestamp}
              actions={
                <>
                  <button className="px-4 py-2 text-sm font-medium text-white bg-tforce-primary rounded-lg hover:bg-tforce-primary/90 hover:shadow-md transition-all duration-200">
                    View Details
                  </button>
                  <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200">
                    Contact Driver
                  </button>
                </>
              }
            />
          ))
        ) : (
          <div className="text-center py-12 text-gray-500">
            <CheckCircle className="h-12 w-12 mx-auto mb-3 text-quality-excellent" />
            <p className="text-sm font-medium text-gray-700">No critical alerts</p>
            <p className="text-xs mt-1 text-gray-500">All systems operating normally</p>
          </div>
        )}
      </div>
    </div>
  );
}

