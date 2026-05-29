# Package Discovery & Search Architecture

**Hardware Script Package Search**  
**Cost**: $0/month  
**Speed**: Instant (local + client-side)  
**Last Updated**: March 2026

---

## Overview

Package discovery uses a dual-path approach:
1. **CLI/LLM**: Lightning-fast local search (like `grep`)
2. **Web/Human**: Beautiful client-side search UI (like docs.rs)

**Both paths cost $0 to host and scale infinitely.**

---

## The Schema: Enforcing Good Metadata

### Required Fields in package.hw.json

Before any package can be searched, it must have proper metadata. The CI validation enforces this schema:

```json
{
  "name": "@sensors/mpu6050",
  "version": "1.0.0",
  "description": "6-axis IMU (Accelerometer + Gyroscope) over I2C",
  "author": "Jane Doe <jane@example.com>",
  "license": "MIT",
  "category": "sensor",
  "keywords": ["imu", "accelerometer", "gyroscope", "i2c", "motion"],
  "repository": "https://github.com/jane/hw-mpu6050",
  "download_url": "https://github.com/jane/hw-mpu6050/releases/download/v1.0.0/package.zip",
  "checksum": "sha256:8f4e2d1a9c3b7e5f...",
  "electrical": {
    "voltage_min": "2.375V",
    "voltage_max": "3.46V",
    "current_typical": "3.9mA"
  },
  "physical": {
    "dimensions": "4mm x 4mm x 0.9mm",
    "package": "QFN-24"
  },
  "dependencies": {
    "@std/materials": "^1.0.0"
  }
}
```

### Required Fields

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | ✅ | Unique package identifier |
| `version` | string | ✅ | Semantic version |
| `description` | string | ✅ | Human-readable summary (for search) |
| `author` | string | ✅ | Package maintainer |
| `license` | string | ✅ | Open-source license |
| `category` | string | ✅ | Primary category (for filtering) |
| `keywords` | array | ✅ | Search tags (min 3, max 10) |
| `repository` | string | ✅ | Source code URL |
| `download_url` | string | ✅ | Package download URL |
| `checksum` | string | ✅ | SHA-256 integrity hash |

### Valid Categories

```
power           - Power supplies, regulators, batteries
sensor          - Temperature, motion, light, pressure sensors
passive         - Resistors, capacitors, inductors, LEDs
logic           - Gates, flip-flops, multiplexers
microcontroller - MCUs, CPUs, SoCs
communication   - UART, I2C, SPI, Ethernet, WiFi, Bluetooth
display         - LCDs, OLEDs, e-paper
motor           - DC, stepper, servo, brushless
audio           - Speakers, microphones, amplifiers
memory          - RAM, ROM, Flash, EEPROM
connector       - Headers, terminals, USB, HDMI
mechanical      - Switches, buttons, encoders
rf              - Antennas, transceivers, amplifiers
analog          - Op-amps, comparators, ADCs, DACs
other           - Miscellaneous components
```

### CI Validation

The GitHub Action rejects packages that:
- Missing required fields
- Invalid category
- Less than 3 keywords
- Description shorter than 20 characters
- Invalid semantic version
- Broken download URL

---

## Path 1: CLI & LLM Search (Local)

### How It Works

**Installation**:
```bash
# When user installs hpm
hpm install

# hpm automatically clones the registry
git clone https://github.com/hwsl-lang/registry ~/.hw/registry_cache/
```

**Search Execution**:
```bash
hpm search "imu i2c"
```

**What happens behind the scenes**:

1. **Update cache** (if stale):
```bash
cd ~/.hw/registry_cache/
git pull origin main
```

2. **Scan JSON files**:
```rust
// Pseudo-code for hpm search implementation
fn search_packages(query: &str) -> Vec<Package> {
    let registry_path = home_dir().join(".hw/registry_cache/packages");
    let mut results = Vec::new();
    
    // Walk through all JSON files
    for entry in WalkDir::new(registry_path) {
        if entry.path().extension() == Some("json") {
            let package: Package = serde_json::from_str(&fs::read_to_string(entry.path())?)?;
            
            // Score package against query
            let score = calculate_relevance(&package, query);
            if score > 0.3 {
                results.push((package, score));
            }
        }
    }
    
    // Sort by relevance
    results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    results.into_iter().map(|(pkg, _)| pkg).collect()
}

fn calculate_relevance(package: &Package, query: &str) -> f32 {
    let query_lower = query.to_lowercase();
    let mut score = 0.0;
    
    // Exact name match (highest priority)
    if package.name.to_lowercase().contains(&query_lower) {
        score += 10.0;
    }
    
    // Description match
    if package.description.to_lowercase().contains(&query_lower) {
        score += 5.0;
    }
    
    // Keyword match
    for keyword in &package.keywords {
        if keyword.to_lowercase().contains(&query_lower) {
            score += 3.0;
        }
    }
    
    // Category match
    if package.category.to_lowercase().contains(&query_lower) {
        score += 2.0;
    }
    
    score
}
```

3. **Display results**:
```
> hpm search "imu i2c"

Found 3 packages:

@sensors/mpu6050 (v1.0.0)
  6-axis IMU (Accelerometer + Gyroscope) over I2C
  Category: sensor
  Tags: imu, accelerometer, gyroscope, i2c, motion

@sensors/bno085 (v2.1.0)
  9-axis IMU with sensor fusion
  Category: sensor
  Tags: imu, magnetometer, i2c, spi, fusion

@sensors/lsm6ds3 (v1.5.0)
  Low-power 6-axis IMU for wearables
  Category: sensor
  Tags: imu, accelerometer, gyroscope, i2c, low-power
```

### JSON Output (for LLMs)

```bash
hpm search "imu i2c" --json
```

**Output**:
```json
[
  {
    "name": "@sensors/mpu6050",
    "version": "1.0.0",
    "description": "6-axis IMU (Accelerometer + Gyroscope) over I2C",
    "category": "sensor",
    "keywords": ["imu", "accelerometer", "gyroscope", "i2c", "motion"],
    "repository": "https://github.com/jane/hw-mpu6050"
  },
  {
    "name": "@sensors/bno085",
    "version": "2.1.0",
    "description": "9-axis IMU with sensor fusion",
    "category": "sensor",
    "keywords": ["imu", "magnetometer", "i2c", "spi", "fusion"],
    "repository": "https://github.com/bob/hw-bno085"
  }
]
```

### Why This Is Perfect for LLMs

**Scenario**: AI assistant is writing a `.hw` file and needs a temperature sensor

```
AI: *Executes* hpm search "temperature i2c" --json
AI: *Reads JSON output*
AI: *Picks best match: @sensors/ds18b20*
AI: *Generates code*
```

```hw
import TemperatureSensor from @sensors/ds18b20

define Space "WeatherStation":
    dimensions: 100mm by 100mm by 2mm
    grid: 100 by 100 by 2

add TemperatureSensor named Temp1 at [1, 50, 50]
```

**No web scraping. No API calls. Instant.**

---

## Path 2: Web Search (Client-Side)

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Actions                         │
│  (Runs on every registry update)                        │
│                                                          │
│  1. Read all packages/*.json files                      │
│  2. Aggregate into search_index.json                    │
│  3. Compress and optimize                               │
│  4. Deploy to GitHub Pages                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              GitHub Pages (Free Hosting)                 │
│         https://registry.hw-script.org                   │
│                                                          │
│  - search_index.json (2MB for 10,000 packages)         │
│  - index.html (Search UI)                               │
│  - app.js (Fuse.js search engine)                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  User's Browser                          │
│                                                          │
│  1. Downloads search_index.json once                    │
│  2. Caches in browser memory                            │
│  3. Searches locally (no server calls)                  │
│  4. Instant results with typo tolerance                 │
└─────────────────────────────────────────────────────────┘
```

### Step 1: Aggregator (GitHub Actions)

**File**: `.github/workflows/build-search-index.yml` in `hwsl-lang/registry`

```yaml
name: Build Search Index

on:
  push:
    branches: [main]
    paths:
      - 'packages/**/*.json'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Aggregate packages
        run: |
          node scripts/build-search-index.js
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          cname: registry.hw-script.org
```

**Script**: `scripts/build-search-index.js`

```javascript
const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Read all package JSON files
const packageFiles = glob.sync('packages/**/*.json');
const packages = [];

for (const file of packageFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const pkg = JSON.parse(content);
  
  // Extract latest version
  const versions = Object.keys(pkg.versions);
  const latestVersion = versions.sort().reverse()[0];
  const latest = pkg.versions[latestVersion];
  
  // Add to search index
  packages.push({
    name: pkg.name,
    version: latestVersion,
    description: latest.description || '',
    category: latest.category || 'other',
    keywords: latest.keywords || [],
    author: latest.author || '',
    license: latest.license || '',
    repository: latest.repository || '',
    downloads: latest.downloads || 0,
    published_at: latest.published_at || ''
  });
}

// Write search index
const searchIndex = {
  generated_at: new Date().toISOString(),
  total_packages: packages.length,
  packages: packages
};

fs.mkdirSync('public', { recursive: true });
fs.writeFileSync(
  'public/search_index.json',
  JSON.stringify(searchIndex, null, 2)
);

console.log(`Built search index with ${packages.length} packages`);
```

### Step 2: Web UI (GitHub Pages)

**File**: `public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hardware Script Package Registry</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>Hardware Script Package Registry</h1>
    <p>Discover hardware components for your projects</p>
  </header>
  
  <main>
    <div class="search-container">
      <input 
        type="text" 
        id="search-input" 
        placeholder="Search packages (e.g., 'temperature sensor i2c')"
        autocomplete="off"
      />
      <div id="search-stats"></div>
    </div>
    
    <div class="content">
      <aside class="filters">
        <h3>Categories</h3>
        <div id="category-filters"></div>
      </aside>
      
      <section class="results">
        <div id="search-results"></div>
      </section>
    </div>
  </main>
  
  <script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2"></script>
  <script src="app.js"></script>
</body>
</html>
```

**File**: `public/app.js`

```javascript
let packages = [];
let fuse = null;

// Load search index
fetch('search_index.json')
  .then(response => response.json())
  .then(data => {
    packages = data.packages;
    initializeSearch();
    renderCategories();
    renderAllPackages();
  });

function initializeSearch() {
  // Configure Fuse.js for fuzzy search
  const options = {
    keys: [
      { name: 'name', weight: 0.4 },
      { name: 'description', weight: 0.3 },
      { name: 'keywords', weight: 0.2 },
      { name: 'category', weight: 0.1 }
    ],
    threshold: 0.4,  // Typo tolerance
    includeScore: true
  };
  
  fuse = new Fuse(packages, options);
  
  // Attach search handler
  document.getElementById('search-input').addEventListener('input', (e) => {
    const query = e.target.value.trim();
    if (query.length > 0) {
      performSearch(query);
    } else {
      renderAllPackages();
    }
  });
}

function performSearch(query) {
  const results = fuse.search(query);
  const packages = results.map(r => r.item);
  
  document.getElementById('search-stats').textContent = 
    `Found ${packages.length} packages`;
  
  renderPackages(packages);
}

function renderPackages(packages) {
  const container = document.getElementById('search-results');
  
  if (packages.length === 0) {
    container.innerHTML = '<p>No packages found</p>';
    return;
  }
  
  container.innerHTML = packages.map(pkg => `
    <div class="package-card">
      <h3>
        <a href="${pkg.repository}" target="_blank">${pkg.name}</a>
        <span class="version">v${pkg.version}</span>
      </h3>
      <p class="description">${pkg.description}</p>
      <div class="metadata">
        <span class="category">${pkg.category}</span>
        <span class="author">${pkg.author}</span>
        <span class="license">${pkg.license}</span>
      </div>
      <div class="keywords">
        ${pkg.keywords.map(k => `<span class="keyword">${k}</span>`).join('')}
      </div>
      <div class="install">
        <code>hpm install ${pkg.name}</code>
      </div>
    </div>
  `).join('');
}

function renderCategories() {
  const categories = [...new Set(packages.map(p => p.category))].sort();
  const container = document.getElementById('category-filters');
  
  container.innerHTML = categories.map(cat => `
    <label>
      <input type="checkbox" value="${cat}" onchange="filterByCategory()">
      ${cat} (${packages.filter(p => p.category === cat).length})
    </label>
  `).join('');
}

function filterByCategory() {
  const selected = Array.from(
    document.querySelectorAll('#category-filters input:checked')
  ).map(cb => cb.value);
  
  if (selected.length === 0) {
    renderAllPackages();
  } else {
    const filtered = packages.filter(p => selected.includes(p.category));
    renderPackages(filtered);
  }
}

function renderAllPackages() {
  document.getElementById('search-stats').textContent = 
    `Showing all ${packages.length} packages`;
  renderPackages(packages);
}
```

### Step 3: User Experience

**User visits**: `https://registry.hw-script.org`

1. **Page loads**: Downloads `search_index.json` (2MB, one-time)
2. **Caches in memory**: Browser stores JSON in RAM
3. **User types**: "temperature i2c"
4. **Instant results**: Fuse.js searches locally (no network call)
5. **Typo tolerance**: "temprature" → "temperature" (fuzzy matching)
6. **Filters**: User clicks "sensor" category
7. **Results update**: Instantly (all client-side)

**Performance**:
- Initial load: 2-3 seconds (download JSON)
- Search latency: <10ms (local search)
- No server costs: $0/month
- Scales to: 100,000+ packages

---

## Comparison: Traditional vs Static Search

### Traditional (Expensive)

```
User types "imu" → 
  Browser sends HTTP request → 
    Server queries PostgreSQL → 
      ElasticSearch indexes → 
        Results returned → 
          Browser renders

Cost: $50-500/month
Latency: 100-500ms
Scalability: Requires scaling
```

### Static (Free)

```
User types "imu" → 
  Fuse.js searches local JSON → 
    Results rendered

Cost: $0/month
Latency: <10ms
Scalability: Infinite (CDN)
```

---

## Search Features

### Fuzzy Matching (Typo Tolerance)

```
User types: "temprature sensro"
Results:    "temperature sensor"
```

### Multi-Word Search

```
User types: "i2c temperature"
Matches:    Packages with BOTH "i2c" AND "temperature"
```

### Category Filtering

```
User selects: "sensor" category
Results:      Only sensor packages
```

### Sorting Options

- Relevance (default)
- Downloads (most popular)
- Recently updated
- Alphabetical

---

## Implementation Checklist

### Phase 1: Schema Enforcement (Week 1)

- [ ] Define required fields in schema.json
- [ ] Update CI validation to enforce schema
- [ ] Reject packages missing required fields
- [ ] Document schema in CONTRIBUTING.md

### Phase 2: CLI Search (Week 2)

- [ ] Implement `hpm search` command
- [ ] Add local registry caching
- [ ] Implement relevance scoring
- [ ] Add `--json` flag for LLM output
- [ ] Add category filtering

### Phase 3: Web Search (Week 3-4)

- [ ] Create aggregator script (build-search-index.js)
- [ ] Set up GitHub Action for auto-build
- [ ] Design web UI (HTML/CSS)
- [ ] Integrate Fuse.js for search
- [ ] Add category filters
- [ ] Deploy to GitHub Pages

### Phase 4: Polish (Week 5)

- [ ] Add package statistics (downloads, stars)
- [ ] Implement sorting options
- [ ] Add "Copy install command" button
- [ ] Mobile-responsive design
- [ ] SEO optimization

---

## Example Search Queries

### By Component Type
```bash
hpm search "resistor"
hpm search "capacitor"
hpm search "led"
```

### By Interface
```bash
hpm search "i2c"
hpm search "spi"
hpm search "uart"
```

### By Function
```bash
hpm search "temperature sensor"
hpm search "motor controller"
hpm search "voltage regulator"
```

### By Manufacturer
```bash
hpm search "espressif"
hpm search "adafruit"
hpm search "sparkfun"
```

### Combined
```bash
hpm search "i2c temperature sensor low power"
```

---

## Conclusion

By using static client-side search, Hardware Script achieves:

- ✅ $0 hosting costs (GitHub Pages)
- ✅ Instant search (<10ms latency)
- ✅ Typo tolerance (fuzzy matching)
- ✅ LLM-friendly (JSON output)
- ✅ Scales infinitely (CDN)
- ✅ Works offline (CLI cache)

**Inspired by**: Rust's docs.rs, npm's search, Cargo's local index

**Next Step**: Implement `hpm search` command in CLI
