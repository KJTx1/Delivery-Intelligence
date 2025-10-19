# Operations Manager - Daily Quality Control Dashboard
## Wireframe Specification

### Overview
**Purpose**: Enable operations managers to review batch-processed quality data from previous day and monitor real-time critical alerts  
**Update Frequency**: Batch data refreshed daily at 2:00 AM, Real-time alerts as they occur  
**Screen Size**: Desktop (1920x1080 primary, responsive to 1440x900)  
**Primary Actions**: Review quality reports, investigate alerts, assign follow-up actions

---

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🚚 TForce Quality Control     Operations Manager Dashboard     [Today: Oct 18] │
│ ─────────────────────────────────────────────────────────────────────────────── │
│                                                                                 │
│ ┌─── HEADER: DAILY QUALITY SUMMARY ────────────────────────────────────────┐  │
│ │                     📊 Yesterday: October 17, 2025                        │  │
│ │                                                                            │  │
│ │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│ │  │   1,247      │  │    94.2%     │  │    $8,450    │  │     23       │ │  │
│ │  │  Deliveries  │  │ Quality Pass │  │ Cost Savings │  │   Issues     │ │  │
│ │  │              │  │              │  │              │  │              │ │  │
│ │  │  ↑ 12% WoW  │  │  ↑ 2.3% WoW  │  │  ↑ 15% WoW  │  │  ↓ 31% WoW  │ │  │
│ │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │  │
│ └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│ ┌─── LEFT COLUMN (60%) ────────────────┐ ┌─── RIGHT COLUMN (40%) ──────────┐  │
│ │                                       │ │                                  │  │
│ │ 🚨 CRITICAL ALERTS (Real-time)       │ │ 📈 DAMAGE PREVENTION IMPACT     │  │
│ │ ─────────────────────────────────────│ │ ──────────────────────────────── │  │
│ │                                       │ │                                  │  │
│ │ ⚠️  SEVERE DAMAGE - Driver #A-147    │ │ ┌────────────────────────────┐  │  │
│ │    📍 Downtown Route                  │ │ │                            │  │  │
│ │    🕐 2 mins ago                      │ │ │     Damage Rate Trend      │  │  │
│ │    [View Details] [Contact Driver]   │ │ │  8%│                       │  │  │
│ │                                       │ │ │    │                       │  │  │
│ │ ⚠️  LOCATION VIOLATION - Driver #B-23│ │ │  6%│        ╱╲            │  │  │
│ │    📍 0.3 miles from target address   │ │ │    │       ╱  ╲           │  │  │
│ │    🕐 15 mins ago                     │ │ │  4%│      ╱    ╲          │  │  │
│ │    [View Photo] [Customer Service]   │ │ │    │     ╱      ╲___      │  │  │
│ │                                       │ │ │  2%│____╱           ╲___  │  │  │
│ │ 🔔 No other critical alerts           │ │ │    └──┬────┬────┬────┬──  │  │  │
│ │                                       │ │ │      7d  14d  21d  28d     │  │  │
│ │ ─────────────────────────────────────│ │ │                            │  │  │
│ │                                       │ │ └────────────────────────────┘  │  │
│ │ 📊 QUALITY DISTRIBUTION (Yesterday)  │ │                                  │  │
│ │ ─────────────────────────────────────│ │ Incidents: 23 (↓31% from prev)  │  │
│ │                                       │ │ Prevented: 89 potential issues  │  │
│ │  Excellent (95-100)  ████████ 58%    │ │ Savings: $8,450 this week       │  │
│ │  Good (85-94)        ████     32%    │ │                                  │  │
│ │  Review (70-84)      █         7%    │ │ ┌────────────────────────────┐  │  │
│ │  Poor (<70)          ▌         3%    │ │ │  Top Damage Indicators      │  │  │
│ │                                       │ │ ├────────────────────────────┤  │  │
│ │  Total: 1,247 deliveries             │ │ │ • Box Deformation     12   │  │  │
│ │  Avg Score: 91.2 (↑1.8 from prev)   │ │ │ • Corner Damage        8   │  │  │
│ │                                       │ │ │ • Weather Exposure     3   │  │  │
│ │ ─────────────────────────────────────│ │ └────────────────────────────┘  │  │
│ │                                       │ │                                  │  │
│ │ 🏆 TOP PERFORMERS (Yesterday)        │ │ 📍 PROBLEM AREAS               │  │
│ │ ─────────────────────────────────────│ │ ──────────────────────────────── │  │
│ │                                       │ │                                  │  │
│ │  1. Driver #A-092  ⭐ 98.5 (32 del.) │ │ ┌────────────────────────────┐  │  │
│ │  2. Driver #C-145  ⭐ 97.8 (28 del.) │ │ │      [MAP VISUALIZATION]    │  │  │
│ │  3. Driver #B-201  ⭐ 96.4 (41 del.) │ │ │                            │  │  │
│ │  4. Driver #D-033  ⭐ 95.9 (35 del.) │ │ │    🔴 Downtown (8 issues)  │  │  │
│ │  5. Driver #A-147  ⭐ 95.2 (29 del.) │ │ │    🟡 Airport Rd (4 issues)│  │  │
│ │                                       │ │ │    🟡 Industrial (3 issues)│  │  │
│ │  [View Full Rankings]                │ │ │    🟢 Suburban (1 issue)   │  │  │
│ │                                       │ │ │                            │  │  │
│ └───────────────────────────────────────┘ │ └────────────────────────────┘  │  │
│                                           │                                  │  │
│ ┌──────────────────────────────────────────────────────────────────────────┐  │
│ │ ✅ ACTION QUEUE (Mixed: Batch Analysis + Real-time)                      │  │
│ │ ──────────────────────────────────────────────────────────────────────── │  │
│ │                                                                           │  │
│ │ Priority  Task                                  Driver/Route    Status   │  │
│ │ ──────────────────────────────────────────────────────────────────────── │  │
│ │ 🔴 HIGH   Customer follow-up: Wrong location    #B-23/Route 5  [Assign] │  │
│ │ 🔴 HIGH   Driver coaching: Repeated damage      #A-147/Route 2 [Assign] │  │
│ │ 🟡 MED    Photo quality review needed           #C-089/Route 8 [Review] │  │
│ │ 🟡 MED    Route optimization: Low scores        Route 12       [Analyze]│  │
│ │ 🟢 LOW    Performance recognition               #A-092         [Send]   │  │
│ │                                                                           │  │
│ │ [View All 18 Actions] [Filter] [Bulk Assign]                            │  │
│ └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Widget Specifications

### 1. Header: Daily Quality Summary
**Data Source**: Batch processing (yesterday's aggregated data)  
**Refresh**: Daily at 2:00 AM  

**Metrics Cards** (4 cards):
- **Total Deliveries**: Count with Week-over-Week comparison
- **Quality Pass Rate**: Percentage of deliveries scoring ≥85
- **Cost Savings**: Calculated from prevented damage incidents
- **Total Issues**: Count of deliveries requiring review

**Visual Design**:
- Large numbers (48px bold)
- Metric labels (16px regular)
- Trend indicators (↑/↓ with percentage in green/red)
- Light background (#F8F9FA) with border

---

### 2. Critical Alerts Panel (Real-time)
**Data Source**: Real-time streaming events  
**Refresh**: Live updates (WebSocket/SSE)  
**Alert Retention**: Last 4 hours

**Alert Types**:
1. **Severe Damage** (damage score < 0.4)
   - Driver ID and route
   - Timestamp
   - Quick actions: View Details, Contact Driver

2. **Location Violation** (location_accuracy < 0.7)
   - Distance from target
   - Timestamp  
   - Quick actions: View Photo, Escalate to Customer Service

3. **Quality Pattern** (3+ poor deliveries by same driver in 2 hours)
   - Driver ID
   - Issue count
   - Quick action: Immediate coaching

**Visual Design**:
- Alert severity colors: Red (#DC3545), Orange (#FD7E14), Yellow (#FFC107)
- Icon indicators: ⚠️ for warnings, 🚨 for critical
- Expandable cards with action buttons
- Sound notification for critical alerts (configurable)
- Auto-dismiss after resolution

---

### 3. Quality Distribution (Yesterday's Batch Data)
**Data Source**: Batch processing  
**Refresh**: Daily at 2:00 AM

**Distribution Breakdown**:
- Excellent (95-100): Green bar
- Good (85-94): Blue bar  
- Review (70-84): Yellow bar
- Poor (<70): Red bar

**Additional Metrics**:
- Total deliveries count
- Average quality score with trend

**Visual Design**:
- Horizontal bar chart with percentages
- Color-coded (green → yellow → red gradient)
- Comparison to previous period (subtle text)

---

### 4. Top Performers (Yesterday's Batch Data)
**Data Source**: Batch processing  
**Refresh**: Daily at 2:00 AM

**Display**:
- Top 5 drivers by quality score
- Driver ID, quality score, delivery count
- Star ratings (visual indicator)

**Interaction**:
- Click driver to view detailed performance
- "View Full Rankings" button → opens full leaderboard
- Ability to send recognition message

---

### 5. Damage Prevention Impact
**Data Source**: Batch analytics with 7/14/21/28 day trends  
**Refresh**: Daily at 2:00 AM

**Components**:
1. **Trend Chart**: 28-day damage rate trend line
   - Y-axis: Damage incident percentage
   - X-axis: Time (7-day intervals)
   - Green fill under curve

2. **Key Metrics**:
   - Total incidents (with trend)
   - Prevented issues (AI projection)
   - Weekly savings calculation

3. **Top Damage Indicators**:
   - List of most common damage types
   - Count for each type

**Visual Design**:
- Line chart with smooth curves
- Metrics in green (positive impact)
- Clear labels and legends

---

### 6. Problem Areas (Geographic Map)
**Data Source**: Batch processing with geolocation analysis  
**Refresh**: Daily at 2:00 AM

**Map Features**:
- Color-coded pins by issue severity
  - 🔴 Red: 5+ issues
  - 🟡 Yellow: 2-4 issues  
  - 🟢 Green: 0-1 issues

**List View**:
- Route/area name
- Issue count
- Severity indicator

**Interaction**:
- Click area → detailed breakdown
- Hover → quick stats tooltip

---

### 7. Action Queue (Mixed Data)
**Data Source**: Batch analysis + real-time alerts  
**Refresh**: Real-time additions, batch-generated items daily

**Queue Items**:
- Priority level (High/Medium/Low)
- Task description
- Associated driver/route
- Action buttons
- Status indicator

**Functionality**:
- Sort by priority, date, driver
- Filter by type, status, route
- Bulk assign to team members
- Mark as complete
- Add notes/comments

**Visual Design**:
- Table/list hybrid layout
- Priority color coding (left border)
- Hover state for rows
- Action buttons appear on hover
- Status badges

---

## Interaction Patterns

### Primary User Flows

**Flow 1: Morning Review (8:00 AM)**
1. User logs in → Dashboard loads with yesterday's batch data
2. Scans header KPIs → Identifies trends
3. Reviews critical alerts → Addresses urgent issues
4. Checks quality distribution → Assesses overall performance
5. Reviews action queue → Assigns tasks to team

**Flow 2: Real-time Alert Response**
1. Critical alert appears → Sound/visual notification
2. User clicks alert → Expands for details
3. Views photo/evidence → Assesses situation
4. Takes action (contact driver, escalate, etc.)
5. Alert moves to action queue or dismissed

**Flow 3: End-of-Day Review (5:00 PM)**
1. Reviews action queue completion
2. Checks updated real-time metrics
3. Identifies coaching opportunities
4. Plans for next day

### Navigation
- Dashboard is default landing page
- Drill-down: Click any metric → detailed view
- Breadcrumb navigation for return
- Quick filters: Date range, route, driver

### Responsive Behavior
- **1920x1080**: Full 2-column layout
- **1440x900**: Adjust column ratio to 55%/45%
- **1280x720**: Stack right column below left
- **Mobile**: Not primary use case, show summary view only

---

## Data Requirements

### Batch Processing Outputs (Daily 2:00 AM)
```json
{
  "summary": {
    "date": "2025-10-17",
    "total_deliveries": 1247,
    "quality_pass_rate": 94.2,
    "cost_savings": 8450,
    "total_issues": 23,
    "week_over_week": {
      "deliveries": 12,
      "quality_pass": 2.3,
      "cost_savings": 15,
      "issues": -31
    }
  },
  "distribution": {
    "excellent": {"count": 723, "percentage": 58},
    "good": {"count": 399, "percentage": 32},
    "review": {"count": 87, "percentage": 7},
    "poor": {"count": 38, "percentage": 3}
  },
  "top_performers": [
    {"driver_id": "A-092", "score": 98.5, "deliveries": 32},
    ...
  ],
  "damage_prevention": {
    "trend_28d": [6.2, 5.8, 5.1, 4.3],
    "incidents": 23,
    "prevented": 89,
    "savings_weekly": 8450,
    "top_indicators": {
      "box_deformation": 12,
      "corner_damage": 8,
      "weather_exposure": 3
    }
  },
  "problem_areas": [
    {"area": "Downtown", "issues": 8, "severity": "high"},
    {"area": "Airport Rd", "issues": 4, "severity": "medium"},
    ...
  ],
  "action_queue": [
    {
      "priority": "high",
      "task": "Customer follow-up: Wrong location",
      "driver": "B-23",
      "route": "Route 5",
      "status": "pending"
    },
    ...
  ]
}
```

### Real-time Alert Stream
```json
{
  "alert_id": "ALT-20251018-001",
  "type": "severe_damage",
  "severity": "critical",
  "timestamp": "2025-10-18T14:32:00Z",
  "driver_id": "A-147",
  "route": "Downtown Route",
  "delivery_id": "DEL-2025-10-18-4738",
  "details": {
    "damage_score": 0.35,
    "damage_type": "box_deformation",
    "photo_url": "oci://bucket/photo.jpg"
  },
  "actions": [
    {"label": "View Details", "action": "view_delivery"},
    {"label": "Contact Driver", "action": "contact_driver"}
  ]
}
```

---

## Technical Notes

### Performance Optimization
- Lazy load action queue (paginate after 10 items)
- Cache batch data (24-hour TTL)
- WebSocket for real-time alerts (fallback to polling)
- Optimize map rendering (cluster nearby pins)

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatible
- High contrast mode option
- Configurable alert sounds

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Success Metrics

### Dashboard Usage
- Time to first action: < 30 seconds
- Daily active usage: > 80% of operations managers
- Alert response time: < 5 minutes
- Action queue completion rate: > 90%

### Business Impact
- Reduced time to identify issues: 75%
- Improved driver coaching effectiveness: 30%
- Faster alert resolution: 50%
- Cost savings tracking accuracy: 95%


