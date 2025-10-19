import { ListTodo } from 'lucide-react';
import { mockActionQueue } from '@/data/mockData';

export function ActionQueue() {
  const actions = mockActionQueue;

  const priorityStyles = {
    high: { bg: 'bg-quality-poor/10', text: 'text-quality-poor', badge: 'HIGH' },
    medium: { bg: 'bg-quality-review/10', text: 'text-quality-review', badge: 'MED' },
    low: { bg: 'bg-quality-good/10', text: 'text-quality-good', badge: 'LOW' },
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      {/* Header with title, count badge, and action buttons */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <ListTodo className="h-6 w-6 text-tforce-primary" />
          <h2 className="text-gray-900">Action Queue</h2>
          <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-gray-100 text-sm font-bold text-gray-700">
            {actions.length}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <ListTodo className="h-4 w-4" />
            Filter
          </button>
          <button className="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            Bulk Assign
          </button>
        </div>
      </div>

      {/* Table with column headers */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left text-sm font-semibold text-gray-600 pb-4 pr-6">Priority</th>
              <th className="text-left text-sm font-semibold text-gray-600 pb-4 pr-6">Task</th>
              <th className="text-left text-sm font-semibold text-gray-600 pb-4 pr-6">Driver/Route</th>
              <th className="text-left text-sm font-semibold text-gray-600 pb-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {actions.map((action) => {
              const style = priorityStyles[action.priority];
              return (
                <tr 
                  key={action.id} 
                  className="border-b border-gray-100 hover:bg-gray-50 transition-colors duration-150"
                >
                  {/* Priority badge */}
                  <td className="py-4 pr-6">
                    <span className={`inline-flex items-center px-3 py-1.5 rounded-lg text-xs font-bold ${style.bg} ${style.text}`}>
                      {style.badge}
                    </span>
                  </td>
                  
                  {/* Task */}
                  <td className="py-4 pr-6">
                    <span className="text-sm font-medium text-gray-900">{action.task}</span>
                  </td>
                  
                  {/* Driver/Route */}
                  <td className="py-4 pr-6">
                    <span className="text-sm text-gray-600">
                      {action.driver && `#${action.driver}`}
                      {action.driver && action.route && '/'}
                      {action.route}
                    </span>
                  </td>
                  
                  {/* Action button */}
                  <td className="py-4">
                    <button className="px-5 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200">
                      {action.actionType}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Footer with view all button */}
      <div className="mt-6 pt-5 border-t border-gray-200 text-center">
        <button className="px-6 py-2.5 text-sm font-medium text-tforce-primary hover:text-tforce-primary/80 transition-colors duration-200">
          View All 18 Actions
        </button>
      </div>
    </div>
  );
}

