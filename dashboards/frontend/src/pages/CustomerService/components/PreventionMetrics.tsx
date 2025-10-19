import { MetricCard } from '@/shared/components/metrics/MetricCard';
import { Shield, Phone, Clock, AlertTriangle, Calendar } from 'lucide-react';
import { mockPreventionMetrics } from '@/data/mockData';

export function PreventionMetrics() {
  const data = mockPreventionMetrics;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Calendar className="h-6 w-6 text-tforce-primary" />
        <h2 className="text-gray-900">Prevention Metrics</h2>
        <small className="text-gray-500">(Yesterday - October 17, 2025)</small>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="At-Risk Deliveries"
          value={data.atRiskDeliveries}
          icon={<AlertTriangle className="h-5 w-5" />}
          trend={{
            value: Math.abs(data.weekOverWeek.atRiskDeliveries),
            direction: data.weekOverWeek.atRiskDeliveries >= 0 ? 'up' : 'down',
            isPositive: false,
          }}
        />

        <MetricCard
          title="Prevention Rate"
          value={`${data.preventionRate}%`}
          icon={<Shield className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.preventionRate,
            direction: data.weekOverWeek.preventionRate >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />

        <MetricCard
          title="Proactive Contacts"
          value={data.proactiveContacts}
          icon={<Phone className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.proactiveContacts,
            direction: data.weekOverWeek.proactiveContacts >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />

        <MetricCard
          title="Avg Response Time"
          value={`${data.avgResponseTime}h`}
          icon={<Clock className="h-5 w-5" />}
          trend={{
            value: Math.abs(data.weekOverWeek.avgResponseTime),
            direction: data.weekOverWeek.avgResponseTime >= 0 ? 'up' : 'down',
            isPositive: false,
          }}
        />
      </div>
    </div>
  );
}

