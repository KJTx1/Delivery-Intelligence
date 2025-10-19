import { Phone, Mail, MessageSquare, CheckCircle, Clock, Lightbulb, AlertCircle } from 'lucide-react';

interface AtRiskCardProps {
  delivery: {
    id: string;
    priority: 'high' | 'medium' | 'low';
    issueType: string;
    customer: {
      name: string;
      tier: string;
      phone: string;
      email: string;
      preferredContact: string;
    };
    orderId: string;
    deliveryTime: string;
    driver: { id: string; name: string };
    route: string;
    qualityIssues: string[];
    aiRecommendation: string;
    status: string;
    timestamp: string;
  };
}

export function AtRiskCard({ delivery }: AtRiskCardProps) {
  const priorityStyles = {
    high: {
      border: 'border-l-4 border-l-quality-poor',
      bg: 'bg-red-50/50',
      badge: 'bg-quality-poor text-white shadow-md',
      label: 'HIGH PRIORITY',
      sublabel: 'Immediate Action Needed',
    },
    medium: {
      border: 'border-l-4 border-l-quality-review',
      bg: 'bg-yellow-50/50',
      badge: 'bg-quality-review text-white shadow-md',
      label: 'MEDIUM PRIORITY',
      sublabel: 'Proactive Outreach',
    },
    low: {
      border: 'border-l-4 border-l-quality-good',
      bg: 'bg-green-50/50',
      badge: 'bg-quality-good text-white shadow-md',
      label: 'LOW PRIORITY',
      sublabel: 'Monitor',
    },
  };

  const style = priorityStyles[delivery.priority];

  return (
    <div className={`bg-white rounded-xl border border-gray-200 ${style.border} overflow-hidden hover:shadow-md transition-all duration-200`}>
      {/* Priority header with clear visual hierarchy */}
      <div className={`px-5 py-3 ${style.bg} border-b border-gray-200`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className={`px-3 py-1 rounded-lg text-xs font-bold ${style.badge}`}>
              {style.label}
            </span>
            <span className="text-sm font-medium text-gray-700">{style.sublabel}</span>
          </div>
          <div className="flex items-center gap-1 text-gray-600">
            <Clock className="h-3.5 w-3.5" />
            <span className="text-xs font-medium">{delivery.timestamp}</span>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Issue header - clear and prominent */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle className="h-5 w-5 text-quality-poor" />
            <h4 className="text-lg font-bold text-gray-900">{delivery.issueType}</h4>
          </div>
          {/* Key info grid - easy scanning */}
          <div className="grid grid-cols-2 gap-x-6 gap-y-3 text-sm">
            <div>
              <div className="text-xs text-gray-500 mb-1">Customer</div>
              <div className="font-semibold text-gray-900">{delivery.customer.name}</div>
            </div>
            <div>
              <div className="text-xs text-gray-500 mb-1">Order</div>
              <div className="font-medium text-gray-900">{delivery.orderId}</div>
            </div>
            <div>
              <div className="text-xs text-gray-500 mb-1">Delivered</div>
              <div className="text-gray-700">{delivery.deliveryTime}</div>
            </div>
            <div>
              <div className="text-xs text-gray-500 mb-1">Driver</div>
              <div className="text-gray-700">#{delivery.driver.id} - {delivery.route}</div>
            </div>
          </div>
        </div>

        {/* Quality Issues - clear visual grouping */}
        <div>
          <h4 className="text-sm font-bold text-gray-900 mb-3">Quality Issues</h4>
          <div className="space-y-2">
            {delivery.qualityIssues.map((issue, idx) => (
              <div key={idx} className="flex items-start gap-2 text-sm">
                <div className="w-1.5 h-1.5 rounded-full bg-quality-poor mt-1.5 flex-shrink-0"></div>
                <span className="text-gray-700 leading-relaxed">{issue}</span>
              </div>
            ))}
          </div>
        </div>

        {/* AI Recommendation - highlighted for importance */}
        <div className="bg-gradient-to-r from-blue-50 to-blue-50/50 border-l-4 border-l-blue-500 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <Lightbulb className="h-5 w-5 text-blue-700" />
            <h4 className="text-sm font-bold text-blue-900">Recommended Action</h4>
          </div>
          <p className="text-sm text-blue-800 leading-relaxed">{delivery.aiRecommendation}</p>
        </div>

        {/* Customer Profile - organized info */}
        <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
          <h4 className="text-sm font-bold text-gray-900 mb-3">Customer Profile</h4>
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <div className="text-gray-500 mb-1">Tier</div>
              <div className="font-semibold text-gray-900">
                {delivery.customer.tier === 'premium' ? '⭐ Premium' : 'Regular'}
              </div>
            </div>
            <div>
              <div className="text-gray-500 mb-1">Preferred Contact</div>
              <div className="font-medium text-gray-900 capitalize">{delivery.customer.preferredContact}</div>
            </div>
            <div>
              <div className="text-gray-500 mb-1">Phone</div>
              <div className="text-gray-700">{delivery.customer.phone}</div>
            </div>
            <div>
              <div className="text-gray-500 mb-1">Email</div>
              <div className="text-gray-700 truncate" title={delivery.customer.email}>{delivery.customer.email}</div>
            </div>
          </div>
        </div>

        {/* Action Buttons - clear primary action (CTA) */}
        <div className="flex flex-wrap gap-2 pt-4 border-t-2 border-gray-100">
          <button className="flex-1 min-w-[120px] flex items-center justify-center gap-2 px-4 py-3 text-sm font-semibold text-white bg-tforce-primary rounded-xl hover:bg-tforce-primary/90 hover:shadow-lg transition-all duration-200">
            <Phone className="h-4 w-4" />
            Call Now
          </button>
          <button className="flex items-center gap-2 px-4 py-3 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200">
            <Mail className="h-4 w-4" />
            Email
          </button>
          <button className="flex items-center gap-2 px-4 py-3 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200">
            <MessageSquare className="h-4 w-4" />
            SMS
          </button>
          <button className="flex items-center gap-2 px-4 py-3 text-sm font-medium text-quality-excellent bg-green-50 border-2 border-quality-excellent rounded-xl hover:bg-green-100 hover:shadow-sm transition-all duration-200">
            <CheckCircle className="h-4 w-4" />
            Resolve
          </button>
        </div>
      </div>
    </div>
  );
}

