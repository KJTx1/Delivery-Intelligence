// Mock data for Operations Manager Dashboard

export const mockFleetSummary = {
  date: '2025-10-17',
  totalDeliveries: 1247,
  qualityPassRate: 94.2,
  costSavings: 8450,
  totalIssues: 23,
  weekOverWeek: {
    deliveries: 12,
    qualityPass: 2.3,
    costSavings: 15,
    issues: -31,
  },
};

export const mockQualityDistribution = {
  excellent: { count: 723, percentage: 58 },
  good: { count: 399, percentage: 32 },
  review: { count: 87, percentage: 7 },
  poor: { count: 38, percentage: 3 },
};

export const mockTopPerformers = [
  { driverId: 'A-092', name: 'Sarah Chen', score: 98.5, deliveries: 32 },
  { driverId: 'C-145', name: 'Mike Johnson', score: 97.8, deliveries: 28 },
  { driverId: 'B-201', name: 'Emma Davis', score: 96.4, deliveries: 41 },
  { driverId: 'D-033', name: 'James Wilson', score: 95.9, deliveries: 35 },
  { driverId: 'A-147', name: 'Lisa Anderson', score: 95.2, deliveries: 29 },
];

export const mockDamagePrevention = {
  trend28d: [
    { date: '7d', value: 6.2 },
    { date: '14d', value: 5.8 },
    { date: '21d', value: 5.1 },
    { date: '28d', value: 4.3 },
  ],
  incidents: 23,
  prevented: 89,
  savingsWeekly: 8450,
  topIndicators: [
    { type: 'Box Deformation', count: 12 },
    { type: 'Corner Damage', count: 8 },
    { type: 'Weather Exposure', count: 3 },
  ],
};

export const mockProblemAreas = [
  { area: 'Downtown', issues: 8, severity: 'high' as const },
  { area: 'Airport Rd', issues: 4, severity: 'medium' as const },
  { area: 'Industrial', issues: 3, severity: 'medium' as const },
  { area: 'Suburban', issues: 1, severity: 'low' as const },
];

export const mockCriticalAlerts = [
  {
    id: 'ALT-001',
    severity: 'critical' as const,
    type: 'Severe Damage',
    driver: { id: 'A-147', name: 'Lisa Anderson' },
    route: 'Downtown Route',
    timestamp: '2 mins ago',
    message: 'Severe damage detected - Box deformation visible',
    details: {
      damageScore: 35,
      deliveryId: 'DEL-2025-10-18-4738',
    },
  },
  {
    id: 'ALT-002',
    severity: 'warning' as const,
    type: 'Location Violation',
    driver: { id: 'B-023', name: 'Robert Martinez' },
    route: 'Airport Route',
    timestamp: '15 mins ago',
    message: 'Package delivered 0.3 miles from target address',
    details: {
      locationAccuracy: 68,
      deliveryId: 'DEL-2025-10-18-4821',
    },
  },
];

export const mockActionQueue = [
  {
    id: '1',
    priority: 'high' as const,
    task: 'Customer follow-up: Wrong location',
    driver: 'B-23',
    route: 'Route 5',
    status: 'pending' as const,
    actionType: 'Assign' as const,
  },
  {
    id: '2',
    priority: 'high' as const,
    task: 'Driver coaching: Repeated damage',
    driver: 'A-147',
    route: 'Route 2',
    status: 'pending' as const,
    actionType: 'Assign' as const,
  },
  {
    id: '3',
    priority: 'medium' as const,
    task: 'Photo quality review needed',
    driver: 'C-089',
    route: 'Route 8',
    status: 'pending' as const,
    actionType: 'Review' as const,
  },
  {
    id: '4',
    priority: 'medium' as const,
    task: 'Route optimization: Low scores',
    driver: '',
    route: 'Route 12',
    status: 'pending' as const,
    actionType: 'Analyze' as const,
  },
  {
    id: '5',
    priority: 'low' as const,
    task: 'Performance recognition',
    driver: 'A-092',
    route: '',
    status: 'pending' as const,
    actionType: 'Send' as const,
  },
];

// Mock data for Driver Dashboard

export const mockDriverPerformance = {
  driverId: 'A-092',
  driverName: 'Sarah Chen',
  date: '2025-10-17',
  performance: {
    qualityScore: 92.8,
    qualityTier: 'excellent',
    personalAverage: 89.6,
    deltaFromAverage: 3.2,
    totalDeliveries: 28,
    onTimePercentage: 96,
    breakdown: {
      locationAccuracy: 95,
      timeliness: 96,
      condition: 88,
    },
  },
  bestDelivery: {
    deliveryId: 'DEL-2025-10-17-2847',
    timestamp: '2:34 PM',
    score: 98.5,
    photoUrl: '/api/photos/2847.jpg',
    aiAnalysis: {
      positiveFactors: [
        'Package placed under shelter (weather protection)',
        'Clearly visible from door',
        'Secure positioning against wall',
        'Perfect GPS accuracy (2m from target)',
      ],
      caption: 'Package delivered to covered front porch, well-protected from weather',
      locationType: 'porch',
    },
  },
  improvementDelivery: {
    deliveryId: 'DEL-2025-10-17-2851',
    timestamp: '4:15 PM',
    score: 76.2,
    photoUrl: '/api/photos/2851.jpg',
    aiSuggestions: {
      primaryIssue: 'Weather exposure',
      steps: [
        'Look for covered areas (garage overhang, entry)',
        'Place against wall for wind protection',
        'Notify customer via app about placement',
      ],
      videoTutorial: {
        id: 'VID-WEATHER-101',
        title: 'Weather Protection Tips',
        duration: '1:45',
      },
    },
  },
  weeklyTrend: [
    { date: 'Mon', score: 85.2 },
    { date: 'Tue', score: 87.4 },
    { date: 'Wed', score: 89.1 },
    { date: 'Thu', score: 88.9 },
    { date: 'Fri', score: 90.3 },
    { date: 'Sat', score: 91.5 },
    { date: 'Sun', score: 92.8 },
  ],
  achievements: {
    earned: [
      { id: 'perfect-week', name: 'Perfect Week', icon: '⭐', earnedDate: '2025-10-17' },
      { id: '100-deliveries', name: '100 Deliveries', icon: '🎯', earnedDate: '2025-10-15' },
      { id: 'package-master', name: 'Package Master', icon: '📦', earnedDate: '2025-10-10' },
      { id: '5-day-streak', name: '5-Day Streak', icon: '🌟', earnedDate: '2025-10-16' },
      { id: 'zero-damage', name: 'Zero Damage', icon: '🔒', earnedDate: '2025-10-12' },
    ],
    inProgress: [
      { id: 'speed-demon', name: 'Speed Demon', icon: '💨', progress: 12, target: 15 },
    ],
  },
  todaysGoals: {
    primary: 'Maintain 90+ score',
    focusArea: 'Improve package protection in weather',
    tip: 'Take 5 extra seconds to find the best spot!',
  },
  recommendedTutorials: [
    {
      id: 'VID-WEATHER-101',
      title: 'Weather Protection Tips',
      duration: '2:30',
      difficulty: 'beginner',
    },
    {
      id: 'VID-PHOTO-CHECKLIST',
      title: 'Perfect Photo Checklist',
      duration: '1:45',
      difficulty: 'all-levels',
    },
    {
      id: 'VID-HIGH-RISE',
      title: 'High-Rise Deliveries',
      duration: '3:15',
      difficulty: 'advanced',
    },
  ],
};

// Mock data for Customer Service Dashboard

export const mockPreventionMetrics = {
  date: '2025-10-17',
  atRiskDeliveries: 23,
  preventionRate: 89,
  proactiveContacts: 18,
  avgResponseTime: 3.2,
  weekOverWeek: {
    atRiskDeliveries: -12,
    preventionRate: 8,
    proactiveContacts: 22,
    avgResponseTime: -0.8,
  },
};

export const mockPreventionTrend = [
  { date: '7d', value: 78 },
  { date: '14d', value: 82 },
  { date: '21d', value: 87 },
  { date: '28d', value: 89 },
];

export const mockImpactMetrics = {
  thisWeek: {
    complaintsPrevented: 15,
    customerSatisfaction: 4.6,
    resolutionTimeAvg: 3.2,
  },
  costImpact: {
    claimsAvoided: 12400,
    refundsSaved: 3200,
  },
};

export const mockQualityCorrelation = [
  { issueType: 'Damage (High Risk)', complaintRate: 78, riskLevel: 'high' as const },
  { issueType: 'Location Error (Medium)', complaintRate: 45, riskLevel: 'medium' as const },
  { issueType: 'Late Delivery (Low)', complaintRate: 12, riskLevel: 'low' as const },
  { issueType: 'Photo Quality (Low)', complaintRate: 8, riskLevel: 'low' as const },
];

export const mockAtRiskDeliveries = [
  {
    id: 'DEL-4738',
    priority: 'high' as const,
    issueType: 'Severe Damage',
    customer: {
      name: 'Jane Smith',
      tier: 'premium',
      phone: '(555) 123-4567',
      email: 'jane.smith@email.com',
      preferredContact: 'phone',
    },
    orderId: 'ORD-2025-10-17-4738',
    deliveryTime: 'Today, 2:15 PM',
    driver: { id: 'A-147', name: 'Lisa Anderson' },
    route: 'Downtown Route',
    qualityIssues: [
      'Damage Score: 35/100 (Severe)',
      'Box deformation visible',
      'Packaging integrity compromised',
    ],
    aiRecommendation: 'Contact customer immediately. Offer replacement/refund. Apologize for inconvenience.',
    status: 'pending' as const,
    timestamp: '15 mins ago',
  },
  {
    id: 'DEL-4821',
    priority: 'medium' as const,
    issueType: 'Wrong Location',
    customer: {
      name: 'Michael Chen',
      tier: 'regular',
      phone: '(555) 234-5678',
      email: 'michael.chen@email.com',
      preferredContact: 'sms',
    },
    orderId: 'ORD-2025-10-17-4821',
    deliveryTime: 'Today, 4:32 PM',
    driver: { id: 'B-023', name: 'Robert Martinez' },
    route: 'Airport Route',
    qualityIssues: [
      'Location Accuracy: 68/100',
      'Delivered 0.3 miles from address',
      'GPS confidence: Low',
    ],
    aiRecommendation: 'Send SMS to confirm package location. If not found, arrange redelivery.',
    status: 'new' as const,
    timestamp: '2 mins ago',
  },
  {
    id: 'DEL-4692',
    priority: 'low' as const,
    issueType: 'Photo Quality Issue',
    customer: {
      name: 'Sarah Johnson',
      tier: 'regular',
      phone: '(555) 345-6789',
      email: 'sarah.j@email.com',
      preferredContact: 'email',
    },
    orderId: 'ORD-2025-10-17-4692',
    deliveryTime: 'Today, 11:20 AM',
    driver: { id: 'C-089', name: 'Tom Williams' },
    route: 'Suburban Route',
    qualityIssues: [
      'Unclear package visibility in photo',
      'Otherwise excellent delivery',
    ],
    aiRecommendation: 'Monitor for customer contact. No immediate action needed.',
    status: 'monitoring' as const,
    timestamp: '25 mins ago',
  },
];

export const mockRecentActivity = [
  {
    id: '1',
    timestamp: '15:42',
    action: 'Resolved case #4821 (satisfied)',
    customer: 'Jane Smith',
  },
  {
    id: '2',
    timestamp: '14:28',
    action: 'Called customer',
    customer: 'Jane Smith',
  },
  {
    id: '3',
    timestamp: '13:15',
    action: 'Sent SMS to',
    customer: 'Michael Chen',
  },
  {
    id: '4',
    timestamp: '12:03',
    action: 'Escalated case #4738 to ops',
    customer: '',
  },
];

export const mockCommunicationLog = [
  {
    id: '1',
    dateTime: 'Oct 18 3:42p',
    customer: 'Jane Smith',
    issueType: 'Severe Damage',
    actionTaken: 'Called, offered replacement',
    outcome: 'Satisfied' as const,
  },
  {
    id: '2',
    dateTime: 'Oct 18 1:15p',
    customer: 'Michael Chen',
    issueType: 'Wrong Location',
    actionTaken: 'SMS sent, confirmed found',
    outcome: 'Resolved' as const,
  },
  {
    id: '3',
    dateTime: 'Oct 18 11:28a',
    customer: 'Robert Davis',
    issueType: 'Package Exposed',
    actionTaken: 'Email with photo, apologized',
    outcome: 'Acknowledged' as const,
  },
  {
    id: '4',
    dateTime: 'Oct 17 5:12p',
    customer: 'Lisa Anderson',
    issueType: 'Late + Damage',
    actionTaken: 'Called, refunded',
    outcome: 'Satisfied' as const,
  },
];

