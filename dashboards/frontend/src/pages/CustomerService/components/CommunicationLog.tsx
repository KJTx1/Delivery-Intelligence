import { CheckCircle, MessageSquare } from 'lucide-react';
import { mockCommunicationLog } from '@/data/mockData';

export function CommunicationLog() {
  const logs = mockCommunicationLog;

  const outcomeStyles = {
    Satisfied: 'bg-quality-excellent/10 text-quality-excellent border-quality-excellent',
    Resolved: 'bg-quality-good/10 text-quality-good border-quality-good',
    Acknowledged: 'bg-blue-50 text-blue-700 border-blue-200',
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <MessageSquare className="h-6 w-6 text-tforce-primary" />
        <h2 className="text-gray-900">Communication Log</h2>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left text-xs font-semibold text-gray-600 pb-3 pr-4">Date/Time</th>
              <th className="text-left text-xs font-semibold text-gray-600 pb-3 pr-4">Customer</th>
              <th className="text-left text-xs font-semibold text-gray-600 pb-3 pr-4">Issue Type</th>
              <th className="text-left text-xs font-semibold text-gray-600 pb-3 pr-4">Action Taken</th>
              <th className="text-left text-xs font-semibold text-gray-600 pb-3">Outcome</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 pr-4 text-sm text-gray-600">{log.dateTime}</td>
                <td className="py-3 pr-4 text-sm font-medium text-gray-900">{log.customer}</td>
                <td className="py-3 pr-4 text-sm text-gray-700">{log.issueType}</td>
                <td className="py-3 pr-4 text-sm text-gray-700">{log.actionTaken}</td>
                <td className="py-3">
                  <span
                    className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs border ${
                      outcomeStyles[log.outcome as keyof typeof outcomeStyles]
                    }`}
                  >
                    <CheckCircle className="h-3 w-3" />
                    {log.outcome}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200 flex items-center justify-between">
        <div className="flex gap-2">
          <button className="text-sm text-tforce-primary hover:text-tforce-primary/80 font-medium">
            View Full Log
          </button>
          <span className="text-gray-300">|</span>
          <button className="text-sm text-tforce-primary hover:text-tforce-primary/80 font-medium">
            Export CSV
          </button>
          <span className="text-gray-300">|</span>
          <button className="text-sm text-tforce-primary hover:text-tforce-primary/80 font-medium">
            Filter
          </button>
        </div>
      </div>
    </div>
  );
}

