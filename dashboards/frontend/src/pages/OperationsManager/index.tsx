import { DailySummary } from './components/DailySummary';
import { CriticalAlerts } from './components/CriticalAlerts';
import { QualityDistribution } from './components/QualityDistribution';
import { TopPerformers } from './components/TopPerformers';
import { DamagePrevention } from './components/DamagePrevention';
import { ProblemAreas } from './components/ProblemAreas';
import { ActionQueue } from './components/ActionQueue';
import { Truck, LayoutDashboard } from 'lucide-react';

export default function OperationsManagerDashboard() {
  // In a real app, this would come from WebSocket connection
  const isConnected = true;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-tforce-primary/10 rounded-lg">
              <Truck className="h-8 w-8 text-tforce-primary" />
            </div>
            <div>
              <h1 className="text-gray-900">TForce Quality Control</h1>
              <div className="flex items-center gap-2 mt-2">
                <LayoutDashboard className="h-4 w-4 text-gray-500" />
                <p className="text-gray-600">Operations Manager Dashboard</p>
              </div>
            </div>
          </div>
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

