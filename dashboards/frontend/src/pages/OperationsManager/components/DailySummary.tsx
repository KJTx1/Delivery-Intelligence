import { MetricCard } from '@/shared/components/metrics/MetricCard';
import { Truck, CheckCircle, DollarSign, AlertTriangle, BarChart3 } from 'lucide-react';
import { mockFleetSummary } from '@/data/mockData';

export function DailySummary() {
  const data = mockFleetSummary;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <BarChart3 className="h-6 w-6 text-tforce-primary" />
        <h2 className="text-gray-900">Yesterday's Performance</h2>
        <small className="text-gray-500">October 17, 2025</small>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Deliveries"
          value={data.totalDeliveries.toLocaleString()}
          icon={<Truck className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.deliveries,
            direction: data.weekOverWeek.deliveries >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />

        <MetricCard
          title="Quality Pass Rate"
          value={`${data.qualityPassRate}%`}
          icon={<CheckCircle className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.qualityPass,
            direction: data.weekOverWeek.qualityPass >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />

        <MetricCard
          title="Cost Savings"
          value={`$${data.costSavings.toLocaleString()}`}
          icon={<DollarSign className="h-5 w-5" />}
          trend={{
            value: data.weekOverWeek.costSavings,
            direction: data.weekOverWeek.costSavings >= 0 ? 'up' : 'down',
            isPositive: true,
          }}
        />

        <MetricCard
          title="Total Issues"
          value={data.totalIssues}
          icon={<AlertTriangle className="h-5 w-5" />}
          trend={{
            value: Math.abs(data.weekOverWeek.issues),
            direction: data.weekOverWeek.issues >= 0 ? 'up' : 'down',
            isPositive: false,
          }}
        />
      </div>
    </div>
  );
}

