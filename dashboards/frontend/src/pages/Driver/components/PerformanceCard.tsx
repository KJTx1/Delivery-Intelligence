import { TrendingUp, Star, Package, Clock } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function PerformanceCard() {
  const data = mockDriverPerformance;
  const { qualityScore, qualityTier, deltaFromAverage, totalDeliveries, onTimePercentage } =
    data.performance;

  const tierConfig = {
    exceptional: { label: 'Exceptional!', color: 'text-yellow-600', bg: 'bg-gradient-to-br from-yellow-50 to-yellow-100' },
    excellent: { label: 'Excellent!', color: 'text-quality-excellent', bg: 'bg-gradient-to-br from-green-50 to-green-100' },
    good: { label: 'Good Job!', color: 'text-quality-good', bg: 'bg-gradient-to-br from-blue-50 to-blue-100' },
    review: { label: 'Keep Improving', color: 'text-quality-review', bg: 'bg-gradient-to-br from-yellow-50 to-yellow-100' },
  };

  const config = tierConfig[qualityTier as keyof typeof tierConfig] || tierConfig.good;

  return (
    <div className={`rounded-lg border border-gray-200 p-6 shadow-sm ${config.bg}`}>
      <div className="flex items-center gap-2 mb-6">
        <Star className="h-6 w-6 text-gray-700" />
        <h2 className="text-gray-900">Yesterday's Performance</h2>
      </div>

      <div className="text-center mb-6">
        <div className="flex items-center justify-center gap-1 mb-3">
          <Star className="h-5 w-5 text-gray-600" />
          <p className="text-gray-600 font-medium">Your Quality Score</p>
        </div>
        <div className={`text-[4rem] font-bold ${config.color} mb-2 leading-none`}>{qualityScore}</div>
        <div className={`text-2xl font-semibold ${config.color}`}>{config.label}</div>

        <div className="flex items-center justify-center gap-1 mt-3">
          <TrendingUp className="h-4 w-4 text-quality-excellent" />
          <span className="text-sm font-medium text-quality-excellent">
            {deltaFromAverage} points from your avg
          </span>
        </div>
      </div>

      <div className="flex items-center justify-around pt-4 border-t border-gray-300">
        <div className="text-center">
          <div className="flex items-center justify-center gap-1 mb-1">
            <Package className="h-4 w-4 text-gray-600" />
          </div>
          <div className="text-2xl font-bold text-gray-900">{totalDeliveries}</div>
          <div className="text-xs text-gray-600">Deliveries</div>
        </div>
        <div className="h-12 w-px bg-gray-300"></div>
        <div className="text-center">
          <div className="flex items-center justify-center gap-1 mb-1">
            <Clock className="h-4 w-4 text-quality-excellent" />
          </div>
          <div className="text-2xl font-bold text-quality-excellent">{onTimePercentage}%</div>
          <div className="text-xs text-gray-600">On-Time</div>
        </div>
      </div>
    </div>
  );
}

