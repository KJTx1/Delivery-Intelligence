import { Target } from 'lucide-react';
import { mockImpactMetrics } from '@/data/mockData';

export function ImpactMetrics() {
  const data = mockImpactMetrics;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Target className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Impact Metrics</h3>
      </div>

      <div className="space-y-4">
        <div>
          <div className="text-sm font-semibold text-gray-700 mb-3">This Week:</div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Complaints Prevented:</span>
              <span className="text-lg font-bold text-quality-excellent">{data.thisWeek.complaintsPrevented}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Customer Satisfaction:</span>
              <span className="text-lg font-bold text-quality-excellent">{data.thisWeek.customerSatisfaction}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Resolution Time:</span>
              <span className="text-lg font-bold text-tforce-primary">{data.thisWeek.resolutionTimeAvg}h avg</span>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-200">
          <div className="text-sm font-semibold text-gray-700 mb-3">Cost Impact:</div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Claims Avoided:</span>
              <span className="text-lg font-bold text-quality-excellent">
                ${data.costImpact.claimsAvoided.toLocaleString()}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Refunds Saved:</span>
              <span className="text-lg font-bold text-quality-excellent">
                ${data.costImpact.refundsSaved.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

