import { type ReactNode } from 'react';
import { TrendIndicator } from './TrendIndicator';

interface MetricCardProps {
  title: string;
  value: string | number;
  trend?: {
    value: number;
    direction: 'up' | 'down';
    isPositive: boolean;
  };
  icon?: ReactNode;
  className?: string;
}

export function MetricCard({ title, value, trend, icon, className = '' }: MetricCardProps) {
  return (
    <div 
      className={`
        group relative bg-white rounded-xl border border-gray-200 p-6 
        shadow-sm hover:shadow-md hover:border-gray-300
        transition-all duration-200 ease-in-out
        ${className}
      `}
    >
      {/* Icon with subtle background */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
        </div>
        {icon && (
          <div className="p-2 bg-gray-50 rounded-lg text-gray-500 group-hover:bg-tforce-primary/10 group-hover:text-tforce-primary transition-colors duration-200">
            {icon}
          </div>
        )}
      </div>
      
      {/* Large metric value - focal point */}
      <div className="mb-3">
        <div className="text-4xl font-bold text-gray-900 tracking-tight leading-none">
          {value}
        </div>
      </div>
      
      {/* Trend indicator */}
      {trend && (
        <TrendIndicator
          value={trend.value}
          direction={trend.direction}
          isPositive={trend.isPositive}
        />
      )}
    </div>
  );
}

