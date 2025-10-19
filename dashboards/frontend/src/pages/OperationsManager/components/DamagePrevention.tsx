import { TrendChart } from '@/shared/components/charts/TrendChart';
import { Shield } from 'lucide-react';
import { mockDamagePrevention } from '@/data/mockData';

export function DamagePrevention() {
  const data = mockDamagePrevention;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Shield className="h-6 w-6 text-quality-excellent" />
        <h3 className="text-gray-900">Damage Prevention</h3>
      </div>

      {/* Chart with better spacing */}
      <div className="mb-6">
        <TrendChart data={data.trend28d} color="#10b981" height={200} />
      </div>

      {/* Key metrics with enhanced visual hierarchy */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="flex flex-col items-center justify-center text-center p-4 bg-gradient-to-br from-red-50 to-white rounded-xl border border-red-100 hover:shadow-sm transition-all duration-200">
          <div className="text-3xl font-bold text-quality-poor mb-1">{data.incidents}</div>
          <div className="text-xs font-medium text-gray-600 mb-2">Incidents</div>
          <div className="text-xs font-semibold text-quality-excellent">↓31%</div>
        </div>
        <div className="flex flex-col items-center justify-center text-center p-4 bg-gradient-to-br from-green-50 to-white rounded-xl border border-green-100 hover:shadow-sm transition-all duration-200">
          <div className="text-3xl font-bold text-quality-excellent mb-1">{data.prevented}</div>
          <div className="text-xs font-medium text-gray-600 mb-2">Prevented</div>
          <div className="text-xs text-gray-500">AI projection</div>
        </div>
        <div className="flex flex-col items-center justify-center text-center p-4 bg-gradient-to-br from-blue-50 to-white rounded-xl border border-blue-100 hover:shadow-sm transition-all duration-200">
          <div className="text-3xl font-bold text-tforce-primary mb-1">${(data.savingsWeekly / 1000).toFixed(1)}K</div>
          <div className="text-xs font-medium text-gray-600 mb-2">Weekly Savings</div>
          <div className="text-xs font-semibold text-quality-excellent">↑15%</div>
        </div>
      </div>

      {/* Top indicators with better grouping */}
      <div className="mt-6 pt-6 border-t-2 border-gray-100">
        <h4 className="text-gray-700 mb-4">Top Damage Indicators</h4>
        <div className="space-y-3">
          {data.topIndicators.map((indicator, index) => (
            <div key={indicator.type} className="flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors duration-200">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-full bg-white border-2 border-gray-300 flex items-center justify-center">
                  <span className="text-xs font-bold text-gray-600">{index + 1}</span>
                </div>
                <span className="text-sm font-medium text-gray-700">{indicator.type}</span>
              </div>
              <span className="text-base font-bold text-gray-900">{indicator.count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

