import { Trophy, Award } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function Achievements() {
  const { earned, inProgress } = mockDriverPerformance.achievements;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Trophy className="h-6 w-6 text-yellow-500" />
        <h3 className="text-gray-900">Achievements</h3>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {/* Earned achievements with celebration effect */}
        {earned.map((achievement) => (
          <div
            key={achievement.id}
            className="group relative flex flex-col items-center p-4 rounded-xl bg-gradient-to-br from-yellow-50 via-yellow-100 to-yellow-50 border-2 border-yellow-200 hover:border-yellow-300 hover:shadow-lg hover:scale-105 transition-all duration-300 cursor-pointer overflow-hidden"
          >
            {/* Shimmer effect on hover */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
            
            <div className="relative z-10 flex flex-col items-center">
              <div className="text-4xl mb-2">{achievement.icon}</div>
              <div className="text-xs font-semibold text-center text-gray-800 leading-tight mb-2">
                {achievement.name}
              </div>
              <Award className="h-5 w-5 text-quality-excellent" />
            </div>
          </div>
        ))}

        {/* In-progress with progress indicator */}
        {inProgress.map((achievement) => (
          <div
            key={achievement.id}
            className="group relative flex flex-col items-center p-4 rounded-xl bg-gradient-to-br from-gray-50 to-white border-2 border-dashed border-gray-300 hover:border-gray-400 hover:shadow-md transition-all duration-200 cursor-pointer"
          >
            <div className="text-4xl mb-2 opacity-60 group-hover:opacity-80 transition-opacity">
              {achievement.icon}
            </div>
            <div className="text-xs font-semibold text-center text-gray-700 leading-tight mb-3">
              {achievement.name}
            </div>
            
            {/* Progress bar */}
            <div className="w-full">
              <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                <span>Progress</span>
                <span className="font-bold">{achievement.progress}/{achievement.target}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
                <div
                  className="h-1.5 bg-gradient-to-r from-tforce-primary to-blue-500 rounded-full transition-all duration-500"
                  style={{ width: `${(achievement.progress / achievement.target) * 100}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

