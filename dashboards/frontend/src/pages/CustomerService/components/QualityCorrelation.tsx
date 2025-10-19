import { ArrowRight, TrendingUp } from 'lucide-react';
import { mockQualityCorrelation } from '@/data/mockData';

export function QualityCorrelation() {
  const data = mockQualityCorrelation;

  const riskColors = {
    high: 'text-quality-poor',
    medium: 'text-quality-review',
    low: 'text-quality-good',
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <TrendingUp className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Quality → Complaint</h3>
      </div>

      <h4 className="text-gray-700 mb-3">Quality Issue Type</h4>

      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.issueType} className="space-y-1">
            <div className="text-sm font-medium text-gray-900">{item.issueType}</div>
            <div className="flex items-center gap-2">
              <ArrowRight className={`h-4 w-4 ${riskColors[item.riskLevel]}`} />
              <span className="text-sm text-gray-700">
                Complaint Rate:{' '}
                <span className={`font-bold ${riskColors[item.riskLevel]}`}>
                  {item.complaintRate}%
                </span>
              </span>
            </div>
            {item !== data[data.length - 1] && <div className="h-px bg-gray-100 mt-2"></div>}
          </div>
        ))}
      </div>
    </div>
  );
}

