import { Play, Lightbulb, Package, PartyPopper, Camera, Clock } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function ImprovementArea() {
  const { improvementDelivery } = mockDriverPerformance;

  if (!improvementDelivery || improvementDelivery.score >= 85) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-6">
          <Lightbulb className="h-6 w-6 text-yellow-500" />
          <h3 className="text-gray-900">Area for Improvement</h3>
        </div>
        <div className="text-center py-8">
          <PartyPopper className="h-16 w-16 mx-auto mb-3 text-quality-excellent" />
          <p className="text-sm font-medium text-gray-700">All Deliveries Met Standards!</p>
          <p className="text-xs text-gray-500 mt-1">Keep up the great work!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Lightbulb className="h-6 w-6 text-yellow-500" />
        <h3 className="text-gray-900">Area for Improvement</h3>
      </div>

      {/* Placeholder for delivery photo */}
      <div className="relative aspect-video bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg mb-4 flex items-center justify-center border-2 border-dashed border-yellow-300">
        <div className="text-center">
          <Package className="h-16 w-16 mx-auto mb-2 text-yellow-600" />
          <div className="text-sm font-medium text-gray-700">Package left exposed</div>
          <div className="text-xs text-gray-500 mt-1">On open driveway</div>
        </div>
      </div>

      <div className="bg-yellow-50 rounded-lg p-4 mb-4 border border-yellow-200">
        <h4 className="font-semibold text-yellow-900 mb-3 flex items-center gap-2">
          <Lightbulb className="h-5 w-5" />
          AI Suggestion:
        </h4>
        <p className="text-sm text-yellow-800 mb-3">
          <strong>Issue:</strong> {improvementDelivery.aiSuggestions.primaryIssue}
        </p>
        <div className="space-y-2">
          {improvementDelivery.aiSuggestions.steps.map((step, index) => (
            <div key={index} className="flex items-start gap-2 text-sm text-yellow-800">
              <span className="font-semibold">{index + 1}.</span>
              <span>{step}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
        <div className="flex items-center gap-1">
          <Camera className="h-3 w-3" />
          <span>Delivery #{improvementDelivery.deliveryId.split('-').pop()}</span>
        </div>
        <div className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          <span>{improvementDelivery.timestamp}</span>
        </div>
        <span className="font-semibold text-quality-review">Score: {improvementDelivery.score}</span>
      </div>

      <button className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-tforce-primary text-white rounded-lg hover:bg-tforce-primary/90 transition-all hover:shadow-md">
        <Play className="h-4 w-4" />
        <span className="text-sm font-medium">
          Watch Video Tutorial ({improvementDelivery.aiSuggestions.videoTutorial.duration})
        </span>
      </button>
    </div>
  );
}

