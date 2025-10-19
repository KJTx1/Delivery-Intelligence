import { Star, Lightbulb, Target } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function TodaysGoals() {
  const { primary, focusArea, tip } = mockDriverPerformance.todaysGoals;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Target className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Today's Goals</h3>
      </div>

      <div className="space-y-4">
        <div className="flex items-start gap-3">
          <Star className="h-5 w-5 text-yellow-500 mt-0.5" />
          <div>
            <div className="text-xs font-medium text-gray-600 mb-1">Primary Goal:</div>
            <div className="text-sm font-semibold text-gray-900">{primary}</div>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <Target className="h-5 w-5 text-tforce-primary mt-0.5" />
          <div>
            <div className="text-xs font-medium text-gray-600 mb-1">Focus Area:</div>
            <div className="text-sm font-semibold text-gray-900">{focusArea}</div>
          </div>
        </div>

        <div className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
          <Lightbulb className="h-5 w-5 text-blue-600 mt-0.5" />
          <div>
            <div className="text-xs font-medium text-blue-900 mb-1">Tip of the Day:</div>
            <div className="text-sm font-medium text-blue-800">{tip}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

