import { PerformanceCard } from './components/PerformanceCard';
import { ScoreBreakdown } from './components/ScoreBreakdown';
import { BestDelivery } from './components/BestDelivery';
import { ImprovementArea } from './components/ImprovementArea';
import { WeeklyProgress } from './components/WeeklyProgress';
import { Achievements } from './components/Achievements';
import { TodaysGoals } from './components/TodaysGoals';
import { LearningCenter } from './components/LearningCenter';
import { User, Calendar } from 'lucide-react';
import { mockDriverPerformance } from '@/data/mockData';

export default function DriverDashboard() {
  const { driverName } = mockDriverPerformance;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* Header */}
        <div className="mb-8 bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-tforce-primary/10 rounded-full">
              <User className="h-8 w-8 text-tforce-primary" />
            </div>
            <div>
              <h1 className="text-gray-900">
                Good Morning, {driverName.split(' ')[0]}!
              </h1>
              <div className="flex items-center gap-2 mt-2">
                <Calendar className="h-4 w-4 text-gray-500" />
                <p className="text-gray-600">Here's your October 17 report</p>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Card */}
        <PerformanceCard />

        {/* Score Breakdown */}
        <ScoreBreakdown />

        {/* Best Delivery */}
        <BestDelivery />

        {/* Improvement Area */}
        <ImprovementArea />

        {/* Weekly Progress */}
        <WeeklyProgress />

        {/* Achievements */}
        <Achievements />

        {/* Today's Goals */}
        <TodaysGoals />

        {/* Learning Center */}
        <LearningCenter />

        {/* Footer */}
        <div className="pt-6 pb-8 text-center">
          <button className="text-sm text-tforce-primary hover:text-tforce-primary/80 font-medium">
            View Full Performance Report →
          </button>
        </div>
      </div>
    </div>
  );
}

