import { AlertCircle, Clock } from 'lucide-react';
import { type ReactNode } from 'react';

interface AlertCardProps {
  severity: 'critical' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: string;
  actions?: ReactNode;
  className?: string;
}

export function AlertCard({
  severity,
  title,
  message,
  timestamp,
  actions,
  className = '',
}: AlertCardProps) {
  const severityStyles = {
    critical: {
      border: 'border-l-4 border-l-quality-poor',
      bg: 'bg-red-50/50',
      iconBg: 'bg-quality-poor/10',
      iconColor: 'text-quality-poor',
      badge: 'bg-quality-poor text-white',
    },
    warning: {
      border: 'border-l-4 border-l-quality-review',
      bg: 'bg-yellow-50/50',
      iconBg: 'bg-quality-review/10',
      iconColor: 'text-quality-review',
      badge: 'bg-quality-review text-white',
    },
    info: {
      border: 'border-l-4 border-l-quality-good',
      bg: 'bg-blue-50/50',
      iconBg: 'bg-quality-good/10',
      iconColor: 'text-quality-good',
      badge: 'bg-quality-good text-white',
    },
  };

  const style = severityStyles[severity];

  return (
    <div 
      className={`
        bg-white rounded-xl border border-gray-200 overflow-hidden
        ${style.border} ${style.bg}
        hover:shadow-md transition-all duration-200
        ${className}
      `}
    >
      <div className="p-5">
        <div className="flex items-start gap-4">
          {/* Icon with background */}
          <div className={`flex-shrink-0 p-2.5 rounded-lg ${style.iconBg}`}>
            <AlertCircle className={`h-5 w-5 ${style.iconColor}`} />
          </div>
          
          {/* Content */}
          <div className="flex-1 min-w-0">
            {/* Header */}
            <div className="flex items-start justify-between gap-3 mb-2">
              <h4 className="font-semibold text-gray-900 leading-tight">{title}</h4>
              <div className="flex items-center gap-1 text-gray-500 flex-shrink-0">
                <Clock className="h-3 w-3" />
                <span className="text-xs">{timestamp}</span>
              </div>
            </div>
            
            {/* Message */}
            <p className="text-sm text-gray-700 leading-relaxed mb-4">{message}</p>
            
            {/* Actions */}
            {actions && (
              <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-200">
                {actions}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

