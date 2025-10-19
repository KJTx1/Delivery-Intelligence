import { MapPin, Clock, Package, BarChart2 } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function ScoreBreakdown() {
  const { breakdown } = mockDriverPerformance.performance;

  const items = [
    { label: 'Location', value: breakdown.locationAccuracy, icon: MapPin },
    { label: 'Timeliness', value: breakdown.timeliness, icon: Clock },
    { label: 'Condition', value: breakdown.condition, icon: Package },
  ];

  const getColor = (value: number) => {
    if (value >= 90) return 'bg-quality-excellent';
    if (value >= 75) return 'bg-quality-good';
    if (value >= 60) return 'bg-quality-review';
    return 'bg-quality-poor';
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <BarChart2 className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Score Breakdown</h3>
      </div>

      <div className="space-y-4">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <div key={item.label}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Icon className="h-4 w-4 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">{item.label}</span>
                </div>
                <span className="text-sm font-bold text-gray-900">{item.value}%</span>
              </div>
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${getColor(item.value)}`}
                style={{ width: `${item.value}%` }}
              />
            </div>
          </div>
        );
        })}
      </div>
    </div>
  );
}

