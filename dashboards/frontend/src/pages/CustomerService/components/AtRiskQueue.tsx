import { AtRiskCard } from './AtRiskCard';
import { AlertCircle, Filter } from 'lucide-react';
import { mockAtRiskDeliveries } from '@/data/mockData';
import { useState } from 'react';

export function AtRiskQueue() {
  const [filter, setFilter] = useState('all');
  const deliveries = mockAtRiskDeliveries;

  const filteredDeliveries =
    filter === 'all'
      ? deliveries
      : deliveries.filter((d) => d.priority === filter);

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <AlertCircle className="h-6 w-6 text-quality-poor" />
        <h3 className="text-gray-900">At-Risk Deliveries</h3>
        <small className="text-gray-500">(Real-time + Batch)</small>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-2 mb-4">
        <Filter className="h-4 w-4 text-gray-500" />
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
              filter === 'all'
                ? 'bg-tforce-primary text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All ({deliveries.length})
          </button>
          <button
            onClick={() => setFilter('high')}
            className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
              filter === 'high'
                ? 'bg-quality-poor text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            High Priority
          </button>
          <button
            onClick={() => setFilter('medium')}
            className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
              filter === 'medium'
                ? 'bg-quality-review text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Medium
          </button>
          <button
            onClick={() => setFilter('low')}
            className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
              filter === 'low'
                ? 'bg-quality-good text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Low
          </button>
        </div>
      </div>

      {/* Deliveries */}
      <div className="space-y-4">
        {filteredDeliveries.map((delivery) => (
          <AtRiskCard key={delivery.id} delivery={delivery} />
        ))}
      </div>

      {deliveries.length > 3 && (
        <div className="mt-4 text-center">
          <button className="text-sm text-tforce-primary hover:text-tforce-primary/80 font-medium">
            Load More (18 more at-risk deliveries) →
          </button>
        </div>
      )}
    </div>
  );
}

