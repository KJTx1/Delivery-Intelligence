import { TrendChart } from '@/shared/components/charts/TrendChart';
import { TrendingUp, BarChart3 } from 'lucide-react';
import { mockPreventionTrend } from '@/data/mockData';

export function PreventionAnalytics() {
  const data = mockPreventionTrend;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <BarChart3 className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Prevention Analytics</h3>
      </div>

      <h4 className="text-gray-700 mb-3">Prevention Rate Trend</h4>

      <TrendChart data={data} color="#10b981" height={200} />

      <div className="mt-4 p-3 bg-green-50 rounded-lg text-center border border-green-200">
        <div className="flex items-center justify-center gap-2">
          <TrendingUp className="h-4 w-4 text-quality-excellent" />
          <p className="text-sm font-medium text-quality-excellent">Prevention improving!</p>
        </div>
      </div>
    </div>
  );
}

