---
name: infographic-skill
description: |
  Renders data visualizations and infographics inline in chat as live React components.
  Agent writes JSX inside ```jsx_preview``` fenced code blocks in normal text responses.
  Frontend renders them via JSXPreview from @ai-sdk/elements with a pre-loaded component library.
  Use when user asks to visualize, chart, compare, summarize stats, or create a dashboard view.
---

# Infographic Skill

Embed live infographics in your text response using `jsx_preview` fenced code blocks. The frontend renders them as interactive React components — not code blocks.

## Output Format

Write raw JSX fragments inside triple-backtick fences with the `jsx_preview` language tag. No imports, no `export default`, no module syntax. Just JSX.

````
Here's the breakdown:

```jsx_preview
<StatsGrid>
  <StatCard label="Revenue" value="$12.4k" trend="+8%" />
  <StatCard label="Users" value="1,204" trend="+12%" />
</StatsGrid>
```

Want me to dig deeper into any metric?
````

Rules:
- Raw JSX only — no `import`, no `export`, no `function Component()`
- Use component names from the library below (they're pre-loaded in scope)
- Tailwind classes for all layout and styling
- Use the design token CSS variables listed below — never hardcode colors
- All data inline in JSX props — no external fetches, no `useState`, no hooks
- Multiple `jsx_preview` blocks in one message are fine — each renders independently
- Keep blocks focused: one visualization per block, not entire dashboards
- Surround blocks with normal markdown text for context and insights

## Design Tokens (CSS Variables)

Use these via `var(--token-name)` in `style` props or Tailwind arbitrary values like `text-[var(--color-font-primary)]`.

### Surfaces

| Token | Light value | Use for |
|-------|-------------|---------|
| `--color-surface-primary` | `#FFFFFF` | Card / container backgrounds |
| `--color-surface-tertiary` | `#F0F0F0` | Subtle background, secondary containers |
| `--color-neutral-surface` | `#FFFFFF` | Tooltip / popover surfaces |
| `--color-neutral-surface-subtle` | `rgba(26,28,31,0.08)` | Hover states, muted fills |
| `--color-button-secondary` | `#F0F0F0` | Muted button / pill backgrounds |

### Brand

| Token | Value | Use for |
|-------|-------|---------|
| `--color-surface-brand` | `#4FCEE4` | Primary brand accent — chart highlights, active indicators, primary buttons |
| `--color-surface-brand-alpha-1` | `rgba(79,206,228,0.24)` | Brand tint backgrounds, selected states |
| `--color-surface-brand-alpha-2` | `rgba(79,206,228,0.48)` | Stronger brand tint |
| `--color-surface-brand-secondary` | `#FF005B` | Secondary accent — callouts, badges, hot metrics |
| `--color-surface-brand-secondary-alpha-1` | `rgba(255,0,91,0.24)` | Secondary accent tint |

### State

| Token | Value | Use for |
|-------|-------|---------|
| `--color-surface-success` | `#53C546` | Positive trends, completed states, good metrics |
| `--color-surface-success-alpha-1` | `rgba(0,195,20,0.2)` | Success tint backgrounds |
| `--color-surface-error` | `#E72930` | Negative trends, errors, danger states |
| `--color-surface-error-alpha-1` | `rgba(231,41,48,0.2)` | Error tint backgrounds |
| `--color-surface-warning` | `#FFBE4C` | Caution, in-progress, attention |
| `--color-surface-warning-alpha-1` | `rgba(255,190,76,0.2)` | Warning tint backgrounds |

### Typography

| Token | Value | Use for |
|-------|-------|---------|
| `--color-font-primary` | `#1A1C1F` | Headings, primary text, values |
| `--color-font-primary-reverted` | `#FFFFFF` | Text on dark/brand backgrounds |
| `--color-font-secondary` | `#898A8B` | Labels, captions, muted text |
| `--color-font-brand` | `#4FCEE4` | Brand-colored text, links |
| `--color-font-brand-secondary` | `#FF005B` | Secondary accent text |
| `--color-font-error` | `#E72930` | Error text, negative trend values |
| `--color-font-success` | `#53C546` | Success text, positive trend values |
| `--color-font-warning` | `#F3C977` | Warning text |
| `--color-font-disabled` | `#ACAEB1` | Disabled / inactive text |

### Dividers & Separators

| Token | Value | Use for |
|-------|-------|---------|
| `--color-divider-primary` | `rgba(0,0,0,0.08)` | Primary divider lines |
| `--color-divider-secondary` | `rgba(0,0,0,0.06)` | Subtle dividers |
| `--color-separator-card` | `rgba(0,0,0,0.06)` | Card borders |
| `--color-separator-brand` | `#4FCEE4` | Brand-colored borders |
| `--color-separator-error` | `#DB3F3E` | Error borders |
| `--color-separator-success` | `#00C314` | Success borders |

### Neutral Opacity Scales

For fine-grained opacity control on dark (`--color-neutral-primary-*`) or light (`--color-neutral-primary-reverted-*`) backgrounds:

- `--color-neutral-primary-10` through `--color-neutral-primary-100` — white at 10%-100% opacity
- `--color-neutral-primary-reverted-10` through `--color-neutral-primary-reverted-100` — black at 10%-100% opacity

### Token Usage Guidelines

- **Chart bars/lines/fills**: `--color-surface-brand` (primary), `--color-surface-brand-secondary` (secondary), `--color-surface-success` / `--color-surface-error` for positive/negative
- **Card backgrounds**: `--color-surface-primary` with `--color-separator-card` border
- **Stat values**: `--color-font-primary`; trends use `--color-font-success` (positive) or `--color-font-error` (negative)
- **Labels/captions**: `--color-font-secondary`
- **Section titles**: `--color-font-primary`
- **Hover/muted fills**: `--color-neutral-surface-subtle`
- **Table row alternation**: `--color-surface-tertiary` for even rows

## Component Library

### Data Visualization

#### `BarChart`

Vertical or horizontal bar chart.

```jsx_preview
<BarChart
  data={[
    { label: "Mon", value: 42 },
    { label: "Tue", value: 58 },
    { label: "Wed", value: 35 },
    { label: "Thu", value: 71 },
    { label: "Fri", value: 63 },
  ]}
  color="var(--color-surface-brand)"
  horizontal={false}
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `{ label: string, value: number }[]` | required | Data points |
| `color` | `string` | `var(--color-surface-brand)` | Bar fill color (CSS value) |
| `horizontal` | `boolean` | `false` | Horizontal layout |
| `showValues` | `boolean` | `true` | Display values on bars |
| `height` | `number` | `200` | Chart height in px |

#### `LineChart`

Trend line with optional smoothing.

```jsx_preview
<LineChart
  data={[
    { label: "Jan", value: 120 },
    { label: "Feb", value: 145 },
    { label: "Mar", value: 132 },
    { label: "Apr", value: 178 },
  ]}
  smooth={true}
  color="var(--color-surface-brand-secondary)"
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `{ label: string, value: number }[]` | required | Data points |
| `color` | `string` | `var(--color-surface-brand)` | Line stroke color |
| `smooth` | `boolean` | `false` | Smooth curve interpolation |
| `showDots` | `boolean` | `true` | Show data point dots |
| `showArea` | `boolean` | `false` | Fill area under line |
| `height` | `number` | `200` | Chart height in px |

#### `PieChart`

Proportional breakdown as a donut/pie.

```jsx_preview
<PieChart
  data={[
    { label: "Organic", value: 45, color: "var(--color-success)" },
    { label: "Paid", value: 30, color: "var(--color-surface-brand)" },
    { label: "Referral", value: 25, color: "var(--color-surface-brand-secondary)" },
  ]}
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `{ label: string, value: number, color?: string }[]` | required | Segments |
| `donut` | `boolean` | `true` | Donut style (hollow center) |
| `showLabels` | `boolean` | `true` | Show segment labels |
| `showPercent` | `boolean` | `true` | Show percentage values |
| `size` | `number` | `200` | Chart diameter in px |

#### `AreaChart`

Filled area trend chart.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `{ label: string, value: number }[]` | required | Data points |
| `color` | `string` | `var(--color-surface-brand)` | Fill/stroke color |
| `gradient` | `boolean` | `true` | Gradient fill from color to transparent |
| `smooth` | `boolean` | `true` | Smooth curve |
| `height` | `number` | `200` | Chart height in px |

### Metrics

#### `StatCard`

Single metric with optional trend indicator.

```jsx_preview
<StatCard label="Monthly Revenue" value="$48.2k" trend="+12.5%" icon="dollar" />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | required | Metric name |
| `value` | `string` | required | Display value (pre-formatted) |
| `trend` | `string` | — | Change indicator ("+8%", "-3%", "→ 0%") |
| `icon` | `string` | — | Icon name: `dollar`, `users`, `chart`, `eye`, `heart`, `star`, `clock`, `zap` |
| `variant` | `string` | `"default"` | `"default"` \| `"highlight"` \| `"muted"` |

#### `StatsGrid`

Responsive grid of `StatCard` children.

```jsx_preview
<StatsGrid columns={4}>
  <StatCard label="Views" value="24.1k" trend="+18%" icon="eye" />
  <StatCard label="Likes" value="3.2k" trend="+7%" icon="heart" />
  <StatCard label="Shares" value="892" trend="+23%" icon="zap" />
  <StatCard label="Comments" value="341" trend="-2%" icon="chat" />
</StatsGrid>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `number` | `3` | Grid columns (responsive: stacks on mobile) |
| `children` | `StatCard[]` | required | StatCard components |

#### `ProgressBar`

Labeled progress indicator.

```jsx_preview
<ProgressBar label="Campaign Budget" value={72} max={100} color="var(--color-surface-success)" />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | — | Description |
| `value` | `number` | required | Current value |
| `max` | `number` | `100` | Maximum value |
| `color` | `string` | `var(--color-surface-brand)` | Fill color |
| `showPercent` | `boolean` | `true` | Show percentage text |

### Structure

#### `ComparisonTable`

Side-by-side comparison of items across features.

```jsx_preview
<ComparisonTable
  headers={["Feature", "Plan A", "Plan B", "Plan C"]}
  rows={[
    ["Price", "$9/mo", "$19/mo", "$49/mo"],
    ["Users", "1", "5", "Unlimited"],
    ["Storage", "10 GB", "50 GB", "500 GB"],
    ["Support", "Email", "Priority", "Dedicated"],
  ]}
  highlight={2}
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `headers` | `string[]` | required | Column headers |
| `rows` | `string[][]` | required | Row data (each row = array of cell values) |
| `highlight` | `number` | — | 0-based column index to highlight |

#### `Timeline`

Vertical event timeline.

```jsx_preview
<Timeline>
  <TimelineItem date="Jan 15" title="Project Kickoff" description="Initial planning and team assembly" variant="completed" />
  <TimelineItem date="Feb 1" title="Alpha Release" description="Internal testing begins" variant="completed" />
  <TimelineItem date="Mar 15" title="Beta Launch" description="Public beta with 500 users" variant="active" />
  <TimelineItem date="Apr 30" title="GA Release" variant="upcoming" />
</Timeline>
```

**Timeline** — no props, wraps `TimelineItem` children.

**TimelineItem**:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `date` | `string` | required | Date label |
| `title` | `string` | required | Event title |
| `description` | `string` | — | Event detail |
| `variant` | `string` | `"default"` | `"completed"` \| `"active"` \| `"upcoming"` \| `"default"` |

### Labels

#### `Badge`

Inline colored label.

```jsx_preview
<Badge variant="success">Active</Badge>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | required | Label text |
| `variant` | `string` | `"default"` | `"default"` \| `"success"` \| `"warning"` \| `"danger"` \| `"info"` |

#### `Tag`

Smaller, outlined label.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | required | Label text |
| `color` | `string` | `var(--color-font-secondary)` | Border/text color |

### Layout

#### `Section`

Titled content block with padding and border.

```jsx_preview
<Section title="Revenue Breakdown">
  <BarChart data={[...]} />
</Section>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | — | Section heading |
| `children` | `ReactNode` | required | Content |

#### `Grid`

CSS grid layout.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `number` | `2` | Column count |
| `gap` | `number` | `4` | Tailwind gap unit |
| `children` | `ReactNode` | required | Grid items |

#### `Stack`

Vertical flex layout.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `gap` | `number` | `3` | Tailwind gap unit |
| `children` | `ReactNode` | required | Stacked items |

### Typography

#### `Heading`

Themed heading.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | required | Heading text |
| `level` | `number` | `2` | 1-4 (maps to text size) |

#### `Text`

Body text.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | required | Text content |
| `muted` | `boolean` | `false` | Use muted color |

#### `Caption`

Small muted text.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | required | Caption text |

## When to Use Infographics

**Use `jsx_preview` when:**
- User asks to visualize, chart, graph, or plot data
- Comparing multiple items/options side by side
- Summarizing metrics or KPIs (stat cards)
- Showing a timeline or project progress
- Data-heavy research results that benefit from visual structure
- User says "dashboard", "infographic", "breakdown", "overview"

**Do NOT use when:**
- Simple text answer is sufficient (don't over-visualize)
- User asks for a file export (PDF, CSV) — write the file instead
- The data is a single number or short list — just say it in text
- Image/video generation — use the generation pipeline, not JSX

## Examples

### Stats Dashboard

````
Your campaign performed well this week:

```jsx_preview
<Section title="Campaign Performance — Week 12">
  <StatsGrid columns={4}>
    <StatCard label="Impressions" value="142k" trend="+24%" icon="eye" />
    <StatCard label="Clicks" value="8.3k" trend="+11%" icon="zap" />
    <StatCard label="CTR" value="5.8%" trend="+0.4%" icon="chart" />
    <StatCard label="Conversions" value="412" trend="+32%" icon="star" />
  </StatsGrid>
  <Grid columns={2}>
    <BarChart
      data={[
        { label: "Mon", value: 1120 },
        { label: "Tue", value: 1340 },
        { label: "Wed", value: 980 },
        { label: "Thu", value: 1560 },
        { label: "Fri", value: 1890 },
        { label: "Sat", value: 720 },
        { label: "Sun", value: 640 },
      ]}
      color="var(--color-surface-brand)"
    />
    <PieChart
      data={[
        { label: "Instagram", value: 45, color: "var(--color-surface-brand-secondary)" },
        { label: "TikTok", value: 32, color: "var(--color-surface-brand)" },
        { label: "YouTube", value: 23, color: "var(--color-font-secondary)" },
      ]}
    />
  </Grid>
</Section>
```

Thursday and Friday drove the most clicks. Instagram remains the top channel at 45%.
````

### Comparison Table

````
Here's how the three plans stack up:

```jsx_preview
<ComparisonTable
  headers={["", "Starter", "Pro", "Enterprise"]}
  rows={[
    ["Monthly Price", "$29", "$79", "$199"],
    ["Video Credits", "50", "200", "Unlimited"],
    ["Team Members", "1", "5", "25"],
    ["Priority Support", "—", "✓", "✓"],
    ["Custom Branding", "—", "—", "✓"],
  ]}
  highlight={2}
/>
```

Pro is the sweet spot for most teams — 4x the credits at under 3x the price.
````

### Timeline

````
Here's the production timeline:

```jsx_preview
<Timeline>
  <TimelineItem date="Apr 21" title="Script & Storyboard" description="Finalize script, shot list, and visual references" variant="completed" />
  <TimelineItem date="Apr 23" title="Asset Generation" description="Generate all character and location elements" variant="active" />
  <TimelineItem date="Apr 25" title="Video Production" description="Render all shots via Seedance" variant="upcoming" />
  <TimelineItem date="Apr 28" title="Assembly & Montage" description="Stitch shots, add transitions and audio" variant="upcoming" />
  <TimelineItem date="Apr 30" title="Final Delivery" variant="upcoming" />
</Timeline>
```

We're currently on asset generation. On track for the Apr 30 deadline.
````

### Mixed Layout

````
Research summary for the skincare niche:

```jsx_preview
<Stack gap={4}>
  <StatsGrid columns={3}>
    <StatCard label="Avg Views" value="2.1M" icon="eye" />
    <StatCard label="Engagement" value="8.4%" icon="heart" />
    <StatCard label="Top Format" value="Before/After" icon="zap" />
  </StatsGrid>
  <Section title="Views by Platform">
    <BarChart
      data={[
        { label: "TikTok", value: 2100000 },
        { label: "Instagram", value: 1400000 },
        { label: "YouTube", value: 890000 },
      ]}
      horizontal={true}
      color="var(--color-surface-brand-secondary)"
    />
  </Section>
  <Section title="Trending Topics">
    <div className="flex flex-wrap gap-2">
      <Tag color="var(--color-surface-success)">Glass Skin</Tag>
      <Tag color="var(--color-surface-success)">Slugging</Tag>
      <Tag color="var(--color-surface-brand)">Retinol</Tag>
      <Tag color="var(--color-surface-brand)">SPF Layering</Tag>
      <Tag color="var(--color-surface-brand-secondary)">Skin Cycling</Tag>
    </div>
  </Section>
</Stack>
```

TikTok dominates at 2.1M average views. "Glass Skin" and "Slugging" are the highest-growth topics.
````
