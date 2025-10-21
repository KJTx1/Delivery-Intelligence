# Delivery Driver - Personal Performance Dashboard
## Wireframe Specification

### Overview
**Purpose**: Provide drivers with daily performance feedback and personalized improvement guidance  
**Update Frequency**: Batch data refreshed daily at 2:00 AM (shows yesterday's results)  
**Screen Size**: Mobile-first (375x667), Tablet (768x1024), Desktop (1280x720)  
**Primary Actions**: Review performance, view AI feedback, track progress, learn best practices

---

## Layout Structure - Mobile (Primary)

```
┌─────────────────────────────────┐
│ 🚚 TForce Driver Portal    ☰   │
│ ─────────────────────────────── │
│                                 │
│ Good Morning, Sarah! 👋         │
│ Here's your October 17 report   │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 📊 YESTERDAY'S PERFORMANCE  │ │
│ │                             │ │
│ │   ⭐ Your Quality Score     │ │
│ │                             │ │
│ │         92.8                │ │
│ │      ──────────              │ │
│ │      Excellent!              │ │
│ │                             │ │
│ │    ↑ 3.2 points from avg    │ │
│ │                             │ │
│ │ ─────────────────────────── │ │
│ │                             │ │
│ │  28 Deliveries  ✓ 96% On-Time │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 📈 SCORE BREAKDOWN          │ │
│ │                             │ │
│ │  Location    ████████  95%  │ │
│ │  Timeliness  ████████  96%  │ │
│ │  Condition   ████████  88%  │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 🌟 YOUR BEST DELIVERY       │ │
│ │                             │ │
│ │ ┌─────────────────────────┐ │ │
│ │ │                         │ │ │
│ │ │   [DELIVERY PHOTO]      │ │ │
│ │ │                         │ │ │
│ │ │   Package on covered    │ │ │
│ │ │   porch, well-protected │ │ │
│ │ └─────────────────────────┘ │ │
│ │                             │ │
│ │ ✅ Why this was excellent:  │ │
│ │                             │ │
│ │ • Package placed under      │ │
│ │   shelter (weather          │ │
│ │   protection)               │ │
│ │ • Clearly visible from door │ │
│ │ • Secure positioning        │ │
│ │ • Perfect GPS accuracy      │ │
│ │                             │ │
│ │ 📸 Delivery #2847 - 2:34 PM │ │
│ │ Score: 98.5                 │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 💡 AREA FOR IMPROVEMENT     │ │
│ │                             │ │
│ │ ┌─────────────────────────┐ │ │
│ │ │                         │ │ │
│ │ │   [DELIVERY PHOTO]      │ │ │
│ │ │                         │ │ │
│ │ │   Package left exposed  │ │ │
│ │ │   on open driveway      │ │ │
│ │ └─────────────────────────┘ │ │
│ │                             │ │
│ │ 🎯 AI Suggestion:           │ │
│ │                             │ │
│ │ When no porch is available: │ │
│ │                             │ │
│ │ 1. Look for covered areas   │ │
│ │    (garage overhang, entry) │ │
│ │ 2. Place against wall for   │ │
│ │    wind protection          │ │
│ │ 3. Notify customer via app  │ │
│ │                             │ │
│ │ 📸 Delivery #2851 - 4:15 PM │ │
│ │ Score: 76.2                 │ │
│ │                             │ │
│ │ [Watch Video Tutorial 1:45] │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 📅 WEEKLY PROGRESS          │ │
│ │                             │ │
│ │  Quality Score Trend        │ │
│ │                             │ │
│ │  95 │            ●──●       │ │
│ │     │         ●──┘          │ │
│ │  90 │      ●──┘             │ │
│ │     │   ●──┘                │ │
│ │  85 │●──┘                   │ │
│ │     └──┬──┬──┬──┬──┬──┬──  │ │
│ │       M  T  W  T  F  S  S   │ │
│ │                             │ │
│ │  Great work! You're up 7.3  │ │
│ │  points this week 🎉        │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 🏆 ACHIEVEMENTS              │ │
│ │                             │ │
│ │  ┌────┐  ┌────┐  ┌────┐    │ │
│ │  │ ⭐ │  │ 🎯 │  │ 📦 │    │ │
│ │  └────┘  └────┘  └────┘    │ │
│ │  Perfect  100    Package   │ │
│ │   Week  Deliveries Master  │ │
│ │                             │ │
│ │  ┌────┐  ┌────┐  ┌────┐    │ │
│ │  │ 🌟 │  │ 🔒 │  │ 💨 │    │ │
│ │  └────┘  └────┘  └────┘    │ │
│ │   5-Day   Zero    Speed    │ │
│ │   Streak  Damage   Demon   │ │
│ │   ✓      ✓        (12/15)  │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 🎯 TODAY'S GOALS             │ │
│ │                             │ │
│ │  Primary Goal:              │ │
│ │  ⭐ Maintain 90+ score       │ │
│ │                             │ │
│ │  Focus Area:                │ │
│ │  📦 Improve package          │ │
│ │     protection in weather   │ │
│ │                             │ │
│ │  Tip of the Day:            │ │
│ │  💡 Take 5 extra seconds    │ │
│ │     to find the best spot!  │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 📚 LEARNING CENTER           │ │
│ │                             │ │
│ │ Recommended for you:        │ │
│ │                             │ │
│ │ ▶️ Weather Protection Tips  │ │
│ │    2:30 mins • Beginner     │ │
│ │                             │ │
│ │ ▶️ Perfect Photo Checklist  │ │
│ │    1:45 mins • All Levels   │ │
│ │                             │ │
│ │ ▶️ High-Rise Deliveries     │ │
│ │    3:15 mins • Advanced     │ │
│ │                             │ │
│ │ [View All Tutorials]        │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│                                 │
│ [View Full Performance Report] │
│                                 │
└─────────────────────────────────┘
```

---

## Layout Structure - Desktop (Optional)

```
┌───────────────────────────────────────────────────────────────────────────┐
│ 🚚 TForce Driver Portal - Sarah Chen (#A-092)            Thu, Oct 18, 2025│
│ ───────────────────────────────────────────────────────────────────────── │
│                                                                            │
│ ┌─── LEFT COLUMN (50%) ────────────────┐ ┌─── RIGHT COLUMN (50%) ──────┐│
│ │                                       │ │                              ││
│ │ Good Morning, Sarah! 👋               │ │ 🎯 TODAY'S GOALS            ││
│ │ Here's your October 17 report         │ │ ──────────────────────────── ││
│ │                                       │ │                              ││
│ │ ┌───────────────────────────────────┐ │ │  ⭐ Maintain 90+ score      ││
│ │ │ 📊 YESTERDAY'S PERFORMANCE        │ │ │  📦 Focus: Weather          ││
│ │ │                                   │ │ │     protection              ││
│ │ │       ⭐ Your Quality Score       │ │ │                              ││
│ │ │                                   │ │ │ 💡 Tip: Take 5 extra        ││
│ │ │            92.8                   │ │ │    seconds to find the      ││
│ │ │        ────────────                │ │ │    best spot!               ││
│ │ │         Excellent!                │ │ │                              ││
│ │ │                                   │ │ │ ──────────────────────────── ││
│ │ │      ↑ 3.2 from your avg         │ │ │                              ││
│ │ │                                   │ │ │ 📅 WEEKLY PROGRESS          ││
│ │ │  28 Deliveries   ✓ 96% On-Time  │ │ │ ──────────────────────────── ││
│ │ │                                   │ │ │                              ││
│ │ │  Location    ████████  95%       │ │ │ ┌──────────────────────────┐││
│ │ │  Timeliness  ████████  96%       │ │ │ │  95 │         ●──●      │││
│ │ │  Condition   ████████  88%       │ │ │ │     │      ●──┘         │││
│ │ └───────────────────────────────────┘ │ │ │  90 │   ●──┘            │││
│ │                                       │ │ │     │●──┘               │││
│ │ ┌───────────────────────────────────┐ │ │ │  85 └─┬─┬─┬─┬─┬─┬─     │││
│ │ │ 🌟 YOUR BEST DELIVERY             │ │ │ │      M T W T F S S      │││
│ │ │                                   │ │ │ └──────────────────────────┘││
│ │ │ ┌──────────┐  ✅ Why excellent:  │ │ │                              ││
│ │ │ │          │                      │ │ │  ↑ 7.3 points this week! 🎉 ││
│ │ │ │  PHOTO   │  • Weather protection│ │ │                              ││
│ │ │ │          │  • Clearly visible   │ │ │ ──────────────────────────── ││
│ │ │ │  Package │  • Secure position   │ │ │                              ││
│ │ │ │  on      │  • Perfect GPS       │ │ │ 🏆 ACHIEVEMENTS             ││
│ │ │ │  porch   │                      │ │ │ ──────────────────────────── ││
│ │ │ └──────────┘  Score: 98.5         │ │ │                              ││
│ │ │               #2847 - 2:34 PM     │ │ │  ⭐ Perfect Week (earned)   ││
│ │ └───────────────────────────────────┘ │ │  🎯 100 Deliveries (earned) ││
│ │                                       │ │  📦 Package Master (earned) ││
│ │ ┌───────────────────────────────────┐ │ │  🌟 5-Day Streak (earned)   ││
│ │ │ 💡 AREA FOR IMPROVEMENT           │ │ │  🔒 Zero Damage (earned)    ││
│ │ │                                   │ │ │  💨 Speed Demon (12/15)     ││
│ │ │ ┌──────────┐  🎯 AI Suggestion:  │ │ │                              ││
│ │ │ │          │                      │ │ │ ──────────────────────────── ││
│ │ │ │  PHOTO   │  When no porch:     │ │ │                              ││
│ │ │ │          │                      │ │ │ 📚 LEARNING CENTER          ││
│ │ │ │  Package │  1. Look for        │ │ │ ──────────────────────────── ││
│ │ │ │  exposed │     covered areas   │ │ │                              ││
│ │ │ │  on      │  2. Place against   │ │ │ Recommended for you:        ││
│ │ │ │  driveway│     wall            │ │ │                              ││
│ │ │ └──────────┘  3. Notify customer │ │ │ ▶️ Weather Protection       ││
│ │ │               Score: 76.2         │ │ │    2:30 • Beginner          ││
│ │ │               #2851 - 4:15 PM     │ │ │                              ││
│ │ │                                   │ │ │ ▶️ Perfect Photo Checklist  ││
│ │ │ [Watch Video Tutorial 1:45]       │ │ │    1:45 • All Levels        ││
│ │ └───────────────────────────────────┘ │ │                              ││
│ │                                       │ │ [View All Tutorials]        ││
│ └───────────────────────────────────────┘ └──────────────────────────────┘│
│                                                                            │
│                            [View Full Performance Report]                 │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Widget Specifications

### 1. Personal Greeting & Date Context
**Data Source**: User profile + current date  
**Purpose**: Personalize experience and set time context

**Design**:
- Driver's first name
- Friendly emoji
- Date reference (yesterday's data)
- Casual, encouraging tone

---

### 2. Yesterday's Performance Card
**Data Source**: Batch processing (yesterday's aggregated driver data)  
**Refresh**: Daily at 2:00 AM

**Primary Metric**: Quality Score
- Large number display (72px on mobile, 96px on desktop)
- Quality tier label:
  - 95-100: "Exceptional!" (Gold)
  - 90-94: "Excellent!" (Green)
  - 85-89: "Good Job!" (Blue)
  - 70-84: "Keep Improving" (Yellow)
  - <70: "Needs Attention" (Red)

**Comparison**: 
- Difference from personal average
- Trend arrow and delta

**Secondary Metrics**:
- Total deliveries completed
- On-time percentage

**Visual Design**:
- Card with subtle gradient background based on score tier
- Center-aligned large number
- Clear visual hierarchy

---

### 3. Score Breakdown
**Data Source**: Batch processing  
**Components**: 
- Location accuracy (%)
- Timeliness (%)  
- Package condition (%)

**Visual Design**:
- Horizontal progress bars
- Color-coded: Green (>90%), Yellow (75-90%), Red (<75%)
- Percentage values right-aligned
- Subtle icons for each category

**Interaction**:
- Tap bar → see detailed explanation
- Compare to fleet average

---

### 4. Your Best Delivery
**Data Source**: Batch processing with AI caption analysis  
**Selection Logic**: Highest scoring delivery from yesterday

**Components**:
1. **Delivery Photo** (from Object Storage)
   - Display at 16:9 aspect ratio
   - Tap to enlarge

2. **AI Analysis - Why Excellent**:
   - Bulleted list of positive factors
   - Direct quotes from AI caption analysis
   - Specific, actionable observations

3. **Metadata**:
   - Delivery ID
   - Timestamp
   - Exact quality score

**Visual Design**:
- Bright, positive styling (light green background)
- Checkmark icons for positive factors
- Clear photo with rounded corners

**Learning Value**:
- Reinforces good behaviors
- Provides concrete examples
- Builds confidence

---

### 5. Area for Improvement
**Data Source**: Batch processing with AI caption + damage analysis  
**Selection Logic**: Lowest scoring delivery from yesterday (if score < 85)

**Components**:
1. **Delivery Photo** (from Object Storage)
   - Display at 16:9 aspect ratio
   - Tap to enlarge

2. **AI Suggestion**:
   - Specific, actionable improvement steps
   - Numbered list (3-4 items max)
   - Based on actual delivery context

3. **Video Tutorial Link** (optional):
   - Relevant training video
   - Duration displayed
   - Opens in-app player

4. **Metadata**:
   - Delivery ID
   - Timestamp
   - Quality score

**Visual Design**:
- Constructive tone (light yellow background)
- Lightbulb icon for suggestions
- Non-judgmental language

**Conditional Display**:
- Only show if there's a delivery < 85 score
- If all deliveries ≥ 85, show "All Deliveries Met Standards! 🎉"

---

### 6. Weekly Progress Chart
**Data Source**: Batch processing (7-day rolling trend)  
**Refresh**: Daily at 2:00 AM

**Chart Type**: Line chart
- X-axis: Days of week (M, T, W, T, F, S, S)
- Y-axis: Quality score (70-100 range)
- Line with dots for each day
- Green fill under curve

**Summary Text**:
- Week-over-week change
- Encouraging message based on trend

**Visual Design**:
- Simple, clean chart
- Large touch targets for mobile
- Tooltip on tap showing exact score

---

### 7. Achievement Badges
**Data Source**: Batch processing + achievement logic  

**Badge Types**:
1. **Perfect Week**: 95+ score for 7 consecutive days
2. **100 Deliveries**: Milestone achievement
3. **Package Master**: 50+ deliveries with 0 damage incidents
4. **5-Day Streak**: 5 consecutive days with 90+ scores
5. **Zero Damage**: 30 consecutive days with no damage
6. **Speed Demon**: 15 deliveries in a day with 90+ avg score

**Visual Design**:
- Grid layout (2-3 columns)
- Badge icons with labels
- Earned badges: Full color
- In-progress badges: Grayscale with progress indicator
- Locked badges: Outline only

**Gamification**:
- Tap badge → see criteria and progress
- Share badge on social (optional)
- Monthly leaderboard

---

### 8. Today's Goals
**Data Source**: AI-generated based on recent performance patterns  

**Components**:
1. **Primary Goal**: Quality score target
2. **Focus Area**: Specific skill to improve
3. **Tip of the Day**: One actionable tip

**Visual Design**:
- Compact card
- Icons for each section
- Simple, scannable format

**Personalization**:
- Goals based on individual performance gaps
- Adaptive difficulty (achievable but challenging)

---

### 9. Learning Center
**Data Source**: Content management system  
**Personalization**: AI-recommended based on performance gaps

**Video Tutorials**:
- Title
- Duration
- Difficulty level
- Play button
- Thumbnail image

**Categories**:
- Weather protection techniques
- Photo best practices
- High-rise delivery tips
- Customer communication
- Safety procedures

**Interaction**:
- Tap to play in-app video player
- Track completion
- Mark as favorite
- Rate/review tutorials

---

## Interaction Patterns

### Primary User Flows

**Flow 1: Morning Check-in (7:00 AM)**
1. Driver opens app during breakfast
2. Sees greeting and yesterday's performance
3. Reviews best delivery → reinforces good behavior
4. Reads improvement suggestion → learns from mistake
5. Checks today's goals → sets intention
6. Ready to start deliveries with clear focus

**Flow 2: End-of-Day Review (6:00 PM)**
1. Completed deliveries for the day
2. Checks if new achievements unlocked
3. Reviews weekly progress trend
4. Watches recommended tutorial (5-10 mins)
5. Feels prepared and motivated for tomorrow

**Flow 3: Improvement Journey**
1. Notices low score in "Condition" metric
2. Reviews improvement suggestion
3. Watches related video tutorial
4. Applies learning to next delivery
5. Sees score improvement next day
6. Unlocks "Improvement Champion" badge

### Navigation
- Single-page scrolling experience (mobile)
- Pull to refresh for latest data
- Swipe between photo examples
- Tap any widget for detailed view

### Offline Support
- Cache yesterday's data for offline viewing
- Show "Waiting for connection" for today's goals
- Queue achievement notifications for when online

### Notifications
- Daily morning notification: "Your performance report is ready!"
- Achievement unlocked: "🏆 You earned Perfect Week!"
- Improvement milestone: "Quality score up 5 points this week!"

---

## Data Requirements

### Daily Driver Performance (Batch Output)
```json
{
  "driver_id": "A-092",
  "driver_name": "Sarah Chen",
  "date": "2025-10-17",
  "performance": {
    "quality_score": 92.8,
    "quality_tier": "excellent",
    "personal_average": 89.6,
    "delta_from_average": 3.2,
    "total_deliveries": 28,
    "on_time_percentage": 96,
    "breakdown": {
      "location_accuracy": 95,
      "timeliness": 96,
      "condition": 88
    }
  },
  "best_delivery": {
    "delivery_id": "DEL-2025-10-17-2847",
    "timestamp": "2025-10-17T14:34:00Z",
    "score": 98.5,
    "photo_url": "oci://bucket/deliveries/2847.jpg",
    "ai_analysis": {
      "positive_factors": [
        "Package placed under shelter (weather protection)",
        "Clearly visible from door",
        "Secure positioning against wall",
        "Perfect GPS accuracy (2m from target)"
      ],
      "caption": "Package delivered to covered front porch...",
      "location_type": "porch"
    }
  },
  "improvement_delivery": {
    "delivery_id": "DEL-2025-10-17-2851",
    "timestamp": "2025-10-17T16:15:00Z",
    "score": 76.2,
    "photo_url": "oci://bucket/deliveries/2851.jpg",
    "ai_suggestions": {
      "primary_issue": "Weather exposure",
      "steps": [
        "Look for covered areas (garage overhang, entry)",
        "Place against wall for wind protection",
        "Notify customer via app about placement"
      ],
      "video_tutorial": {
        "id": "VID-WEATHER-101",
        "title": "Weather Protection Tips",
        "duration": "1:45",
        "url": "..."
      }
    }
  },
  "weekly_trend": [
    {"date": "2025-10-11", "score": 85.2},
    {"date": "2025-10-12", "score": 87.4},
    {"date": "2025-10-13", "score": 89.1},
    {"date": "2025-10-14", "score": 88.9},
    {"date": "2025-10-15", "score": 90.3},
    {"date": "2025-10-16", "score": 91.5},
    {"date": "2025-10-17", "score": 92.8}
  ],
  "achievements": {
    "earned": [
      {"id": "perfect-week", "name": "Perfect Week", "earned_date": "2025-10-17"},
      {"id": "100-deliveries", "name": "100 Deliveries", "earned_date": "2025-10-15"},
      {"id": "package-master", "name": "Package Master", "earned_date": "2025-10-10"}
    ],
    "in_progress": [
      {"id": "speed-demon", "name": "Speed Demon", "progress": 12, "target": 15}
    ]
  },
  "todays_goals": {
    "primary": "Maintain 90+ score",
    "focus_area": "Improve package protection in weather",
    "tip": "Take 5 extra seconds to find the best spot!"
  },
  "recommended_tutorials": [
    {
      "id": "VID-WEATHER-101",
      "title": "Weather Protection Tips",
      "duration": "2:30",
      "difficulty": "beginner"
    },
    {
      "id": "VID-PHOTO-CHECKLIST",
      "title": "Perfect Photo Checklist",
      "duration": "1:45",
      "difficulty": "all-levels"
    }
  ]
}
```

---

## Technical Notes

### Mobile Performance
- Target load time: < 1.5 seconds
- Optimize photo delivery (WebP format, lazy loading)
- Cache API responses (24-hour TTL)
- Minimize JavaScript bundle size

### Offline Capability
- Service worker for offline access
- Cache previous 7 days of data
- Queue analytics events when offline
- Sync when connection restored

### Accessibility
- VoiceOver/TalkBack support
- Minimum touch target: 44x44px
- WCAG AA contrast ratios
- Screen reader friendly labels
- Support for system font size adjustments

### Platform Support
- iOS 14+ (Safari, in-app webview)
- Android 9+ (Chrome, in-app webview)
- Progressive Web App (PWA) for both platforms

### Analytics Tracking
- Dashboard opens (daily, weekly trends)
- Widget interactions (taps, expansions)
- Video tutorial completions
- Achievement unlock events
- Goal completion tracking

---

## Success Metrics

### Engagement
- Daily active usage: > 75% of drivers
- Average session duration: 3-5 minutes
- Return visit rate: > 5 days/week
- Video tutorial completion: > 40%

### Learning Impact
- Drivers viewing improvement suggestions: > 90%
- Drivers watching tutorials: > 60%
- Improvement in focused area: > 10% within 7 days

### Business Impact
- Driver quality score improvement: > 5 points in 30 days
- Reduction in repeat mistakes: > 30%
- Driver satisfaction with feedback: > 4.2/5.0
- Self-reported confidence increase: > 25%

---

## Future Enhancements

### Phase 2 Features
- Peer comparison (opt-in)
- Driver community/forum
- Custom goal setting
- Weekly challenges with rewards
- Photo upload from app (not just from delivery)

### Phase 3 Features
- Voice-based coaching assistant
- AR overlay for ideal package placement
- Real-time delivery quality assessment
- Integration with route navigation
- Social sharing of achievements


