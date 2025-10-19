import { Play, Clock, BookOpen } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function LearningCenter() {
  const tutorials = mockDriverPerformance.recommendedTutorials;

  const difficultyColors = {
    beginner: 'bg-green-100 text-green-700',
    'all-levels': 'bg-blue-100 text-blue-700',
    advanced: 'bg-purple-100 text-purple-700',
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <BookOpen className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Learning Center</h3>
      </div>

      <p className="text-gray-600 mb-4">Recommended for you:</p>

      <div className="space-y-3">
        {tutorials.map((tutorial) => (
          <button
            key={tutorial.id}
            className="w-full flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:bg-gray-50 hover:shadow-md transition-all text-left"
          >
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-tforce-primary/10 flex items-center justify-center">
              <Play className="h-5 w-5 text-tforce-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-medium text-sm text-gray-900">{tutorial.title}</div>
              <div className="flex items-center gap-2 mt-1">
                <div className="flex items-center gap-1 text-xs text-gray-500">
                  <Clock className="h-3 w-3" />
                  {tutorial.duration}
                </div>
                <span
                  className={`text-xs px-2 py-0.5 rounded ${
                    difficultyColors[tutorial.difficulty as keyof typeof difficultyColors]
                  }`}
                >
                  {tutorial.difficulty}
                </span>
              </div>
            </div>
          </button>
        ))}
      </div>

      <button className="w-full mt-4 text-sm text-tforce-primary hover:text-tforce-primary/80 font-medium">
        View All Tutorials →
      </button>
    </div>
  );
}

