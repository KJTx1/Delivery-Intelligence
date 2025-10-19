import { Star, CheckCircle, Package, Camera, Clock } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function BestDelivery() {
  const { bestDelivery } = mockDriverPerformance;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Star className="h-6 w-6 text-yellow-500 fill-yellow-500" />
        <h3 className="text-gray-900">Your Best Delivery</h3>
      </div>

      {/* Placeholder for delivery photo */}
      <div className="relative aspect-video bg-gradient-to-br from-green-50 to-green-100 rounded-lg mb-4 flex items-center justify-center border-2 border-dashed border-green-300">
        <div className="text-center">
          <Package className="h-16 w-16 mx-auto mb-2 text-green-600" />
          <div className="text-sm font-medium text-gray-700">Package on covered porch</div>
          <div className="text-xs text-gray-500 mt-1">Well-protected delivery</div>
        </div>
      </div>

      <div className="bg-green-50 rounded-lg p-4 mb-4 border border-green-200">
        <h4 className="font-semibold text-green-900 mb-2 flex items-center gap-2">
          <CheckCircle className="h-5 w-5" />
          Why this was excellent:
        </h4>
        <ul className="space-y-1.5">
          {bestDelivery.aiAnalysis.positiveFactors.map((factor, index) => (
            <li key={index} className="text-sm text-green-800 flex items-start gap-2">
              <span className="text-green-600 mt-0.5">•</span>
              <span>{factor}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center gap-1">
          <Camera className="h-3 w-3" />
          <span>Delivery #{bestDelivery.deliveryId.split('-').pop()}</span>
        </div>
        <div className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          <span>{bestDelivery.timestamp}</span>
        </div>
        <span className="font-semibold text-quality-excellent">Score: {bestDelivery.score}</span>
      </div>
    </div>
  );
}

