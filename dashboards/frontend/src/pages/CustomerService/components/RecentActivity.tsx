import { Clock, Bell } from 'lucide-react';
import { mockRecentActivity } from '@/data/mockData';

export function RecentActivity() {
  const activities = mockRecentActivity;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Bell className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Recent Activity</h3>
      </div>

      <div className="space-y-3">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-start gap-3 text-sm p-2 rounded-lg hover:bg-gray-50 transition-colors">
            <Clock className="h-4 w-4 text-gray-400 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <div className="text-xs text-gray-500">{activity.timestamp}</div>
              <div className="text-gray-700">
                {activity.action}
                {activity.customer && (
                  <span className="font-medium text-gray-900"> {activity.customer}</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <button className="w-full text-sm text-tforce-primary hover:text-tforce-primary/80 font-medium">
          View All Activity →
        </button>
      </div>
    </div>
  );
}

