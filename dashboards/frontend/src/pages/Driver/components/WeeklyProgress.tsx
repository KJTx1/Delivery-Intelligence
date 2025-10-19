import { TrendChart } from '@/shared/components/charts/TrendChart';
import { Calendar, TrendingUp } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export function WeeklyProgress() {
  const weeklyData = mockDriverPerformance.weeklyTrend;
  const firstScore = weeklyData[0].score;
  const lastScore = weeklyData[weeklyData.length - 1].score;
  const improvement = (lastScore - firstScore).toFixed(1);

  // Transform data to match TrendChart expected format
  const chartData = weeklyData.map(item => ({
    date: item.date,
    value: item.score
  }));

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <Calendar className="h-6 w-6 text-tforce-primary" />
        <h3 className="text-gray-900">Weekly Progress</h3>
      </div>

      <TrendChart data={chartData} color="#0ea5e9" height={200} />

      <div className="mt-4 p-3 bg-green-50 rounded-lg text-center border border-green-200">
        <div className="flex items-center justify-center gap-2">
          <TrendingUp className="h-4 w-4 text-quality-excellent" />
          <p className="text-sm font-medium text-quality-excellent">
            Great work! You're up {improvement} points this week
          </p>
        </div>
      </div>
    </div>
  );
}

