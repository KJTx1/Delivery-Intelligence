import { Trophy, Star } from 'lucide-react';
import { mockTopPerformers } from '@/data/mockData';

export function TopPerformers() {
  const performers = mockTopPerformers;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Trophy className="h-6 w-6 text-yellow-500" />
        <h3 className="text-gray-900">Top Performers</h3>
        <small className="text-gray-500">(Yesterday)</small>
      </div>

      <div className="space-y-3">
        {performers.map((performer, index) => (
          <div
            key={performer.driverId}
            className="group flex items-center justify-between p-4 rounded-xl bg-white border-2 border-gray-200 hover:border-gray-300 hover:shadow-md hover:bg-gradient-to-r hover:from-gray-50 hover:to-white transition-all duration-200 cursor-pointer"
          >
            <div className="flex items-center gap-4">
              {/* Rank badge with medals for top 3 */}
              <div className={`
                flex items-center justify-center w-10 h-10 rounded-full font-bold text-base
                transition-transform duration-200 group-hover:scale-110
                ${index === 0 ? 'bg-gradient-to-br from-yellow-100 to-yellow-200 text-yellow-800 shadow-sm' :
                  index === 1 ? 'bg-gradient-to-br from-gray-100 to-gray-200 text-gray-700 shadow-sm' :
                  index === 2 ? 'bg-gradient-to-br from-orange-100 to-orange-200 text-orange-700 shadow-sm' :
                  'bg-gray-50 text-gray-600'}
              `}>
                {index + 1}
              </div>
              
              {/* Driver info */}
              <div>
                <div className="font-semibold text-gray-900 mb-0.5">{performer.name}</div>
                <div className="text-xs text-gray-500">Driver #{performer.driverId}</div>
              </div>
            </div>

            {/* Score - visual focal point */}
            <div className="text-right">
              <div className="flex items-center gap-1.5 mb-1">
                <Star className="h-5 w-5 text-yellow-500 fill-yellow-500" />
                <span className="text-xl font-bold text-gray-900">{performer.score}</span>
              </div>
              <div className="text-xs text-gray-500">{performer.deliveries} deliveries</div>
            </div>
          </div>
        ))}
      </div>

      {/* Better call-to-action button */}
      <div className="mt-6 pt-5 border-t-2 border-gray-100">
        <button className="w-full px-4 py-2.5 text-sm font-medium text-tforce-primary bg-tforce-primary/5 rounded-lg hover:bg-tforce-primary/10 hover:shadow-sm transition-all duration-200">
          View Full Rankings →
        </button>
      </div>
    </div>
  );
}

