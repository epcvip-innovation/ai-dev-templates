---
description: Audit CLAUDE.md for bloat, embedded content, and violations of lightweight principles
allowed-tools: read_file, run_terminal_cmd, grep
---

## Command

I'll audit your CLAUDE.md file for bloat and violations of lightweight documentation principles.

## Step 1: Length Check

```bash
if [ ! -f "CLAUDE.md" ]; then
  echo "❌ CLAUDE.md not found in project root"
  exit 1
fi

LINES=$(wc -l < CLAUDE.md)
echo "📏 CLAUDE.md Length: $LINES lines"
echo ""

if [ $LINES -gt 300 ]; then
  echo "🔴 CRITICAL BLOAT: $LINES lines (guidance: 100-200, max 250)"
  BLOAT_SEVERITY="CRITICAL"
elif [ $LINES -gt 250 ]; then
  echo "🔴 SEVERE BLOAT: $LINES lines (guidance: 100-200, max 250)"
  BLOAT_SEVERITY="SEVERE"
elif [ $LINES -gt 200 ]; then
  echo "🟡 LENGTH WARNING: $LINES lines (guidance: 100-200)"
  BLOAT_SEVERITY="WARNING"
else
  echo "✅ Length OK: $LINES lines (within 100-200 guidance)"
  BLOAT_SEVERITY="OK"
fi
```

## Step 2: Detect Embedded Coding Standards

```bash
echo ""
echo "🔍 Checking for Embedded Coding Standards..."
echo ""

# Check for coding standards sections that should be separate
STANDARDS_SECTIONS=$(grep -E "^## (Code Quality|Coding Standards|Anti-Slop|Quality Checklist)" CLAUDE.md | wc -l)

if [ $STANDARDS_SECTIONS -gt 0 ]; then
  echo "🔴 VIOLATION: Embedded Coding Standards Detected"
  echo ""
  echo "Found sections that should be in CODING_STANDARDS.md:"
  grep -n "^## (Code Quality|Coding Standards|Anti-Slop|Quality Checklist)" CLAUDE.md || true
  echo ""

  # Count lines in these sections (approximate)
  STANDARDS_LINES=$(awk '/^## (Code Quality|Coding Standards|Anti-Slop|Quality Checklist)/,/^## / {count++} END {print count}' CLAUDE.md 2>/dev/null || echo "0")
  echo "Estimated embedded standards: ~$STANDARDS_LINES lines"
  echo ""
  echo "📋 RECOMMENDATION: Extract to CODING_STANDARDS.md, add 3-line reference"
else
  echo "✅ No embedded coding standards sections"
fi
```

## Step 3: Detect Embedded Domain Knowledge

```bash
echo ""
echo "🔍 Checking for Embedded Domain Knowledge..."
echo ""

# Check for domain/formula sections
DOMAIN_SECTIONS=$(grep -E "^## (Domain|Key.*Concepts|.*Calculations|.*Formulas|Statistical)" CLAUDE.md | wc -l)

if [ $DOMAIN_SECTIONS -gt 0 ]; then
  echo "🔴 VIOLATION: Embedded Domain Knowledge Detected"
  echo ""
  echo "Found sections that should be in DOMAIN_GUIDE.md:"
  grep -n "^## (Domain|Key.*Concepts|.*Calculations|.*Formulas|Statistical)" CLAUDE.md || true
  echo ""
  echo "📋 RECOMMENDATION: Extract to DOMAIN_GUIDE.md or docs/DOMAIN_REFERENCE.md"
else
  echo "✅ No embedded domain knowledge sections"
fi
```

## Step 4: Check Section Lengths

```bash
echo ""
echo "🔍 Checking Section Lengths (max 30 lines)..."
echo ""

# Find sections exceeding 30 lines
awk '
/^## / {
  if (section && count > 30) {
    print "🟡 LONG SECTION: " section " (" count " lines)"
  }
  section = $0
  count = 0
  next
}
{
  count++
}
END {
  if (section && count > 30) {
    print "🟡 LONG SECTION: " section " (" count " lines)"
  }
}
' CLAUDE.md

# Count how many sections exceed limit
LONG_SECTIONS=$(awk '/^## / {if (count > 30) long++; count=0; next} {count++} END {if (count > 30) long++; print long}' CLAUDE.md)

if [ "$LONG_SECTIONS" -gt 0 ]; then
  echo ""
  echo "📋 RECOMMENDATION: Break down sections >30 lines or extract to separate docs"
else
  echo "✅ All sections within 30-line limit"
fi
```

## Step 5: Check for References (Modular Strategy)

```bash
echo ""
echo "🔍 Checking for Reference Links..."
echo ""

# Count reference links (indicators of modular strategy)
REFERENCE_COUNT=$(grep -c -E "(Reference:|See \[.*\]\(|For.*see)" CLAUDE.md || echo "0")

echo "Found $REFERENCE_COUNT reference links"
echo ""

if [ $REFERENCE_COUNT -eq 0 ]; then
  echo "🔴 VIOLATION: No reference links found"
  echo "📋 RECOMMENDATION: Extract detailed content to separate docs, add reference links"
elif [ $REFERENCE_COUNT -lt 3 ]; then
  echo "🟡 WARNING: Low reference count ($REFERENCE_COUNT)"
  echo "📋 RECOMMENDATION: Consider extracting more content to modular docs"
else
  echo "✅ Good modular strategy: $REFERENCE_COUNT references"
fi
```

## Step 6: Check for Duplication with README

```bash
echo ""
echo "🔍 Checking for README Duplication..."
echo ""

if [ -f "README.md" ]; then
  # Check for duplicate section headers
  DUPLICATE_HEADERS=$(comm -12 <(grep "^##" CLAUDE.md | sort) <(grep "^##" README.md | sort) | wc -l)

  if [ $DUPLICATE_HEADERS -gt 2 ]; then
    echo "🟡 WARNING: $DUPLICATE_HEADERS duplicate section headers with README"
    echo "📋 RECOMMENDATION: Remove duplicates from CLAUDE.md (keep in README for users)"
  else
    echo "✅ Minimal duplication with README"
  fi
else
  echo "ℹ️  No README.md found to compare"
fi
```

## Step 7: Detect Common Bloat Patterns

```bash
echo ""
echo "🔍 Checking for Common Bloat Patterns..."
echo ""

# Check for embedded command lists (should be separate if >20 lines)
COMMAND_SECTION_LINES=$(awk '/^## (Commands|Common Commands|Development Commands)/,/^## / {count++} END {print count}' CLAUDE.md || echo "0")

if [ "$COMMAND_SECTION_LINES" -gt 20 ]; then
  echo "🟡 BLOAT PATTERN: Commands section is $COMMAND_SECTION_LINES lines (max 20)"
  echo "📋 RECOMMENDATION: Extract to COMMANDS_REFERENCE.md, keep 5-10 essential commands"
fi

# Check for embedded file trees
FILE_TREE_LINES=$(grep -c "├──\|└──\|│" CLAUDE.md || echo "0")

if [ "$FILE_TREE_LINES" -gt 15 ]; then
  echo "🟡 BLOAT PATTERN: Large file tree ($FILE_TREE_LINES lines)"
  echo "📋 RECOMMENDATION: Show only key 3-5 directories, full tree → DEVELOPMENT_GUIDE.md"
fi

# Check for code examples (good in moderation)
CODE_BLOCK_COUNT=$(grep -c '```' CLAUDE.md || echo "0")
CODE_BLOCKS=$((CODE_BLOCK_COUNT / 2))

if [ "$CODE_BLOCKS" -gt 10 ]; then
  echo "🟡 BLOAT PATTERN: Many code examples ($CODE_BLOCKS blocks)"
  echo "📋 RECOMMENDATION: Keep 1-2 most critical examples, rest → CODING_STANDARDS.md"
fi
```

## Step 8: Calculate Bloat Score

```bash
echo ""
echo "📊 CALCULATING BLOAT SCORE..."
echo ""

# Estimate extractable lines
EXTRACTABLE=0

# Add estimated lines from violations
if [ $STANDARDS_SECTIONS -gt 0 ]; then
  EXTRACTABLE=$((EXTRACTABLE + 100))  # Conservative estimate
fi

if [ $DOMAIN_SECTIONS -gt 0 ]; then
  EXTRACTABLE=$((EXTRACTABLE + 50))
fi

if [ "$LONG_SECTIONS" -gt 0 ]; then
  EXTRACTABLE=$((EXTRACTABLE + LONG_SECTIONS * 20))
fi

if [ "$COMMAND_SECTION_LINES" -gt 20 ]; then
  EXTRACTABLE=$((EXTRACTABLE + COMMAND_SECTION_LINES - 10))
fi

# Calculate percentage
if [ $LINES -gt 0 ]; then
  BLOAT_PERCENT=$((EXTRACTABLE * 100 / LINES))
else
  BLOAT_PERCENT=0
fi

echo "Estimated extractable content: ~$EXTRACTABLE lines"
echo "Bloat percentage: ~$BLOAT_PERCENT%"
echo ""

if [ $BLOAT_PERCENT -gt 50 ]; then
  echo "🔴 HIGH BLOAT: $BLOAT_PERCENT% of file is extractable"
elif [ $BLOAT_PERCENT -gt 25 ]; then
  echo "🟡 MODERATE BLOAT: $BLOAT_PERCENT% of file is extractable"
else
  echo "✅ LOW BLOAT: $BLOAT_PERCENT% extractable (acceptable)"
fi
```

## Step 9: Generate Audit Report Summary

```bash
echo ""
echo "=================================="
echo "📋 CLAUDE.md AUDIT REPORT SUMMARY"
echo "=================================="
echo ""
echo "📏 Length: $LINES lines ($BLOAT_SEVERITY)"
echo "📚 References: $REFERENCE_COUNT links"
echo "📊 Bloat Score: ~$EXTRACTABLE lines extractable ($BLOAT_PERCENT%)"
echo ""

# Count violations
VIOLATIONS=0

if [ "$BLOAT_SEVERITY" = "CRITICAL" ] || [ "$BLOAT_SEVERITY" = "SEVERE" ]; then
  VIOLATIONS=$((VIOLATIONS + 1))
  echo "🔴 Length violation"
fi

if [ $STANDARDS_SECTIONS -gt 0 ]; then
  VIOLATIONS=$((VIOLATIONS + 1))
  echo "🔴 Embedded coding standards"
fi

if [ $DOMAIN_SECTIONS -gt 0 ]; then
  VIOLATIONS=$((VIOLATIONS + 1))
  echo "🔴 Embedded domain knowledge"
fi

if [ $REFERENCE_COUNT -eq 0 ]; then
  VIOLATIONS=$((VIOLATIONS + 1))
  echo "🔴 No modular references"
fi

if [ "$LONG_SECTIONS" -gt 0 ]; then
  VIOLATIONS=$((VIOLATIONS + 1))
  echo "🟡 Sections exceed 30-line limit"
fi

echo ""
echo "Total violations: $VIOLATIONS"
echo ""
```

## Step 10: Provide Refactoring Recommendations

```bash
if [ $VIOLATIONS -gt 0 ]; then
  echo "=================================="
  echo "📋 REFACTORING RECOMMENDATIONS"
  echo "=================================="
  echo ""

  echo "**Immediate Actions:**"
  echo ""

  if [ $STANDARDS_SECTIONS -gt 0 ]; then
    echo "1. Create CODING_STANDARDS.md"
    echo "   - Extract code quality, anti-slop, review checklist sections"
    echo "   - Replace in CLAUDE.md with: 'Reference: See [CODING_STANDARDS.md]'"
    echo ""
  fi

  if [ $DOMAIN_SECTIONS -gt 0 ]; then
    echo "2. Create DOMAIN_GUIDE.md or docs/DOMAIN_REFERENCE.md"
    echo "   - Extract domain concepts, formulas, calculations"
    echo "   - Replace in CLAUDE.md with brief 3-line summary + reference"
    echo ""
  fi

  if [ "$LONG_SECTIONS" -gt 0 ]; then
    echo "3. Break down or extract long sections"
    echo "   - Target: No section should exceed 30 lines"
    echo "   - Move details to separate docs, keep summaries in CLAUDE.md"
    echo ""
  fi

  echo "**Expected Results:**"
  echo "- Target length: 150-200 lines"
  echo "- Current: $LINES lines"
  echo "- Reduction needed: ~$EXTRACTABLE lines"
  echo "- Projected final: ~$((LINES - EXTRACTABLE)) lines"
  echo ""

  echo "**Resources:**"
  echo "- Guidelines: templates/claude-md/CLAUDE-MD-GUIDELINES.md"
  echo "- Example refactoring: templates/claude-md/example-refactored.md"
  echo ""

  echo "**Next Steps:**"
  echo "1. Create target docs (CODING_STANDARDS.md, DOMAIN_GUIDE.md, etc.)"
  echo "2. Extract content from CLAUDE.md to separate docs"
  echo "3. Replace with 3-line summaries + references"
  echo "4. Run /audit-claude-md again to verify"

else
  echo "=================================="
  echo "✅ AUDIT PASSED"
  echo "=================================="
  echo ""
  echo "Your CLAUDE.md follows lightweight best practices!"
  echo ""
  echo "**Next audit:** $(date -d '+3 months' '+%Y-%m-%d' 2>/dev/null || date -v+3m '+%Y-%m-%d' 2>/dev/null || echo '3 months from now')"
  echo ""
  echo "**Maintenance:**"
  echo "- Run this audit quarterly"
  echo "- Check before adding significant content"
  echo "- Keep total length under 200 lines"
  echo "- Use modular references for detailed docs"
fi

echo ""
echo "=================================="
```

---

## Interpreting Results

See [AUDIT_REFERENCE.md](./AUDIT_REFERENCE.md) for:
- Audit frequency guidelines
- How to handle false positives
- Integration with other commands
- Output example with interpretation

