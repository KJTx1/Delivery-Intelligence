import { MapPin, Map } from 'lucide-react';
import { mockProblemAreas } from '@/data/mockData';

export function ProblemAreas() {
  const areas = mockProblemAreas;

  const severityStyles = {
    high: { bg: 'bg-quality-poor/10', border: 'border-quality-poor', text: 'text-quality-poor' },
    medium: { bg: 'bg-quality-review/10', border: 'border-quality-review', text: 'text-quality-review' },
    low: { bg: 'bg-quality-excellent/10', border: 'border-quality-excellent', text: 'text-quality-excellent' },
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Map className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Problem Areas</h3>
      </div>

      <div className="space-y-3">
        {areas.map((area) => {
          const style = severityStyles[area.severity];
          return (
            <div
              key={area.area}
              className={`
                group p-4 rounded-xl border-2 ${style.border} ${style.bg} 
                hover:shadow-md hover:scale-[1.02] 
                transition-all duration-200 cursor-pointer
              `}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg bg-white/80 ${style.text}`}>
                    <MapPin className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900 mb-0.5">{area.area}</div>
                    <div className="text-xs text-gray-600">{area.issues} issues detected</div>
                  </div>
                </div>
                <div className={`text-3xl font-bold ${style.text} transition-transform duration-200 group-hover:scale-110`}>
                  {area.issues}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Better call-to-action */}
      <div className="mt-6 pt-5 border-t-2 border-gray-100">
        <button className="w-full px-4 py-2.5 text-sm font-medium text-tforce-primary bg-tforce-primary/5 rounded-lg hover:bg-tforce-primary/10 hover:shadow-sm transition-all duration-200 flex items-center justify-center gap-2">
          <Map className="h-4 w-4" />
          <span>View Map →</span>
        </button>
      </div>
    </div>
  );
}

