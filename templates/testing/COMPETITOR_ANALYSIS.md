# Competitor Analysis with Claude Code + Playwright MCP

A guide for using AI-driven browser automation to analyze competitor websites, extract data, and inform product decisions.

## Overview

Claude Code with Playwright MCP can navigate to competitor sites, observe features, extract structured data, and generate comparison reports—all through natural language prompts.

> **2026 Trend**: "The browser is becoming the place where AI work gets done—not just a source of information." — Industry research

## Use Cases

| Use Case | Description |
|----------|-------------|
| **Pricing Analysis** | Extract competitor pricing tiers, features, and promotions |
| **Feature Comparison** | Document what features competitors offer |
| **UX Benchmarking** | Analyze flows, patterns, and design choices |
| **Content Monitoring** | Track changes to competitor messaging |
| **Market Research** | Understand positioning and target audience |

## Basic Workflow

### 1. Navigate to Competitor

```
Navigate to https://competitor.com/pricing
```

### 2. Extract Information

```
Extract the pricing information from this page:
- Plan names
- Monthly/annual prices
- Key features for each plan
- Any promotional discounts
```

### 3. Take Evidence Screenshots

```
Take a screenshot of the pricing table for our records
```

### 4. Generate Report

```
Create a markdown comparison table of this pricing vs our pricing at $X/month
```

## Detailed Patterns

### Pattern 1: Pricing Analysis

**Prompt:**
```
Navigate to https://competitor.com/pricing

Extract and organize:
1. All pricing tiers (name, price monthly, price annual)
2. Features included in each tier
3. Any usage limits (users, storage, API calls)
4. Free trial details
5. Enterprise/custom pricing information

Format as a markdown table.
Take a screenshot for reference.
```

**Expected Output:**
- Structured pricing data
- Feature comparison by tier
- Screenshot evidence

### Pattern 2: Feature Audit

**Prompt:**
```
Navigate to https://competitor.com/features

For each major feature:
1. Feature name and description
2. Which pricing tiers include it
3. Any limitations or usage caps
4. Screenshots of key feature pages

Compare to our feature set and identify:
- Features they have that we don't
- Features we have that they don't
- Similar features with different implementations
```

### Pattern 3: Onboarding Flow Analysis

**Prompt:**
```
Navigate to https://competitor.com and sign up for a free trial.

Document the onboarding experience:
1. Number of steps to create account
2. What information is required
3. First-time user experience (tooltips, tutorials)
4. Time to value (how quickly can you do something useful)

Take screenshots of each step.
Rate the experience 1-10 and explain why.
```

### Pattern 4: UX/UI Benchmarking

**Prompt:**
```
Navigate to https://competitor.com/dashboard (use demo or screenshot if login required)

Analyze the design:
1. Navigation structure (sidebar, top nav, etc.)
2. Information hierarchy
3. Color scheme and visual style
4. Mobile responsiveness (resize to mobile viewport)
5. Loading states and animations

Take screenshots at desktop and mobile sizes.
Note any patterns we should consider adopting.
```

### Pattern 5: Content/Messaging Analysis

**Prompt:**
```
Navigate to https://competitor.com homepage

Extract and analyze:
1. Main value proposition (hero section)
2. Key benefits highlighted
3. Social proof (testimonials, logos, stats)
4. Call-to-action text and placement
5. Target audience signals

How does this compare to our messaging?
What are they emphasizing that we aren't?
```

### Pattern 6: Changelog/Release Monitoring

**Prompt:**
```
Navigate to https://competitor.com/changelog

Extract recent updates from the last 3 months:
1. Feature name
2. Release date
3. Brief description
4. Category (new feature, improvement, fix)

Identify trends:
- What areas are they investing in?
- How frequently do they ship?
- Any features that compete with our roadmap?
```

## Multi-Competitor Comparison

**Prompt:**
```
I need to compare pricing across 3 competitors:
- https://competitor-a.com/pricing
- https://competitor-b.com/pricing
- https://competitor-c.com/pricing

For each:
1. Navigate to pricing page
2. Extract all tiers and prices
3. Take screenshot
4. Note any unique features or positioning

Then create a comparison table including our pricing ($29/mo starter, $79/mo pro).
```

## Handling Common Challenges

### Challenge: Login Required

**Solution:** Use public pages or marketing materials
```
The dashboard requires login. Instead:
1. Check their marketing site for feature descriptions
2. Look for a demo video or interactive demo
3. Check G2/Capterra for screenshots
```

### Challenge: Dynamic Content

**Solution:** Wait for content to load
```
Navigate to the page and wait 3 seconds for dynamic content to load.
Then take a snapshot and extract the data.
```

### Challenge: Anti-Bot Protection

**Solution:** Act like a human
```
Navigate slowly, don't rapid-fire requests.
If blocked, note it and move to public pages.
```

### Challenge: Complex Pricing

**Solution:** Break it down
```
This pricing page has multiple tabs.
First, list all the tabs/categories.
Then go through each one and extract pricing.
```

## Ethical Considerations

### Do
- Analyze publicly available information
- Use for competitive intelligence and market research
- Respect robots.txt and rate limits
- Document sources and dates

### Don't
- Attempt to access private/authenticated areas
- Scrape personal data or PII
- Violate terms of service
- Misrepresent findings

### Legal Note

This guide covers analysis of **publicly available** competitor information. Always:
- Review competitor's Terms of Service
- Consult legal if unsure about specific data use
- Keep analysis for internal decision-making
- Attribute sources appropriately in any external communications

## Tools Comparison

For large-scale or ongoing monitoring, consider dedicated tools:

| Tool | Best For | Pricing |
|------|----------|---------|
| **Claude MCP** | Ad-hoc analysis, intelligent extraction | Per-usage |
| [Browse AI](https://www.browse.ai/) | Scheduled monitoring, no-code | $39-249/mo |
| [Firecrawl](https://www.firecrawl.dev/) | Structured data extraction for AI | Usage-based |
| [Bright Data](https://brightdata.com/) | Large-scale scraping, proxies | Enterprise |

### When to Use Claude MCP vs Dedicated Tools

**Use Claude MCP when:**
- One-time or infrequent analysis
- You need intelligent interpretation
- Complex, varied page structures
- Small number of competitors

**Use dedicated tools when:**
- Ongoing monitoring (daily/weekly)
- Large number of pages/competitors
- Need for structured APIs
- Compliance/audit requirements

## Output Templates

### Pricing Comparison Table

```markdown
| Feature | Us | Competitor A | Competitor B |
|---------|-----|--------------|--------------|
| **Starter Price** | $29/mo | $25/mo | $35/mo |
| **Pro Price** | $79/mo | $99/mo | $89/mo |
| **Users (Starter)** | 5 | 3 | Unlimited |
| **Storage** | 10GB | 5GB | 20GB |
| **API Access** | Pro only | All plans | Enterprise |
| **Support** | Email | Email | Chat |
```

### Feature Gap Analysis

```markdown
## Features They Have, We Don't
1. **Real-time collaboration** - Multiple users editing simultaneously
2. **Mobile app** - Native iOS/Android apps
3. **Zapier integration** - 100+ integrations

## Features We Have, They Don't
1. **AI-powered insights** - Automatic analysis
2. **Custom branding** - White-label options
3. **Offline mode** - Works without internet

## Priority Recommendations
1. 🔴 High: Add real-time collaboration (competitive necessity)
2. 🟡 Medium: Build mobile app (market expectation)
3. 🟢 Low: Zapier integration (nice to have)
```

## Further Reading

- [Browse AI: Competitor Monitoring](https://www.browse.ai/)
- [Firecrawl: Web Scraping for AI](https://www.firecrawl.dev/)
- [Top AI Web Scrapers 2026](https://blog.apify.com/best-ai-web-scrapers/)
