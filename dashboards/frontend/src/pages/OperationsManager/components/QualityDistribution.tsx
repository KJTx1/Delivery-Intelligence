import { PieChart } from 'lucide-react';
import { mockQualityDistribution } from '@/data/mockData';

export function QualityDistribution() {
  const data = mockQualityDistribution;
  const total = data.excellent.count + data.good.count + data.review.count + data.poor.count;

  const items = [
    { label: 'Excellent (95-100)', ...data.excellent, color: 'bg-quality-excellent', textColor: 'text-quality-excellent' },
    { label: 'Good (85-94)', ...data.good, color: 'bg-quality-good', textColor: 'text-quality-good' },
    { label: 'Review (70-84)', ...data.review, color: 'bg-quality-review', textColor: 'text-quality-review' },
    { label: 'Poor (<70)', ...data.poor, color: 'bg-quality-poor', textColor: 'text-quality-poor' },
  ];

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <PieChart className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Quality Distribution</h3>
        <small className="text-gray-500">(Yesterday)</small>
      </div>

      <div className="space-y-5">
        {items.map((item) => (
          <div key={item.label} className="group">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">{item.label}</span>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500">{item.count.toLocaleString()}</span>
                <span className={`text-base font-bold ${item.textColor}`}>{item.percentage}%</span>
              </div>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
              <div
                className={`h-3 rounded-full ${item.color} transition-all duration-500 ease-out`}
                style={{ width: `${item.percentage}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Summary section with better visual separation */}
      <div className="mt-8 pt-6 border-t-2 border-gray-100 space-y-3">
        <div className="flex justify-between items-baseline">
          <span className="text-sm font-medium text-gray-600">Total Deliveries</span>
          <span className="text-2xl font-bold text-gray-900">{total.toLocaleString()}</span>
        </div>
        <div className="flex justify-between items-baseline">
          <span className="text-sm font-medium text-gray-600">Average Score</span>
          <div className="text-right">
            <span className="text-2xl font-bold text-quality-excellent">91.2</span>
            <span className="text-xs font-normal text-gray-500 ml-2">(↑1.8)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

