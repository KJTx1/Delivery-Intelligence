import { PreventionMetrics } from './components/PreventionMetrics';
import { AtRiskQueue } from './components/AtRiskQueue';
import { PreventionAnalytics } from './components/PreventionAnalytics';
import { ImpactMetrics } from './components/ImpactMetrics';
import { QualityCorrelation } from './components/QualityCorrelation';
import { RecentActivity } from './components/RecentActivity';
import { CommunicationLog } from './components/CommunicationLog';
import { Headset, Calendar, LayoutDashboard } from 'lucide-react';

export default function CustomerServiceDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-tforce-primary/10 rounded-lg">
              <Headset className="h-8 w-8 text-tforce-primary" />
            </div>
            <div>
              <h1 className="text-gray-900">TForce Customer Service Hub</h1>
              <div className="flex items-center gap-2 mt-2">
                <LayoutDashboard className="h-4 w-4 text-gray-500" />
                <p className="text-gray-600">Customer Service Dashboard</p>
                <span className="text-gray-400">•</span>
                <div className="flex items-center gap-1">
                  <Calendar className="h-4 w-4 text-gray-500" />
                  <small className="text-gray-600">Today: Oct 18</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Prevention Metrics */}
        <PreventionMetrics />

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          {/* Left Column (2/3) */}
          <div className="lg:col-span-2">
            <AtRiskQueue />
          </div>

          {/* Right Column (1/3) */}
          <div className="space-y-6">
            <PreventionAnalytics />
            <ImpactMetrics />
            <QualityCorrelation />
            <RecentActivity />
          </div>
        </div>

        {/* Communication Log */}
        <div className="mt-6">
          <CommunicationLog />
        </div>
      </div>
    </div>
  );
}

