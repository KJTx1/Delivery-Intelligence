import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid';

interface TrendIndicatorProps {
  value: number;
  direction: 'up' | 'down';
  isPositive: boolean;
  suffix?: string;
  className?: string;
}

export function TrendIndicator({
  value,
  direction,
  isPositive,
  suffix = '%',
  className = '',
}: TrendIndicatorProps) {
  const isGood = (direction === 'up' && isPositive) || (direction === 'down' && !isPositive);
  const colorClass = isGood ? 'text-quality-excellent' : 'text-quality-poor';
  const Icon = direction === 'up' ? ArrowUpIcon : ArrowDownIcon;

  return (
    <div className={`flex items-center gap-1 text-sm font-medium ${colorClass} ${className}`}>
      <Icon className="h-4 w-4" />
      <span>
        {Math.abs(value)}
        {suffix} WoW
      </span>
    </div>
  );
}

