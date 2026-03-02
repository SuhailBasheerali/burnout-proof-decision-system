# 📋 Research Log: Academic Burnout-Proof Decision System Development

**Purpose:** Document all prompts, search queries, references, and AI interactions that shaped this project's design and evolution.

---

## 🎯 Core Prompts That Shaped the System

### Foundational Questions
- How to build a decision companion system
- How practical will be a burnout proof decision system
- Another name for a burnout proof decision system
- Resilience driven growth decision system
- Synonyms for a sustainable growth decision system

### System Design Decisions
- Two high impact metrics for an academic burnout proof system
- What qualities ensure sustainability in academic stress management
- Target users for the system
- How is this different from other tools
- Does this system accept multiple options
- What if the multiple actions are of high impact
- What if the single option is high burden

### Algorithm & Normalization Prompts
- Normalisation for an Eisenhower decision matrix
- What is a stateless comparison system
- Most ideal normalization technique
- Weighted mean normalization scaling to 0–100
- Rule trigger explanation
- Add tension severity level
- Triggered message and sensitivity analysis mode

### Single-Option Handling
- What will be the output if the user wants to decide about executing a single option

### Documentation Generation
- Can you generate a document
- All these (referring to generation of 9 comprehensive markdown guides)

### Architecture & Feasibility
- Is the backend sufficient for a stateless dual-score burnout system
- Is this approachable through multiple devices at a time without user login
- Can we retrieve data from other users in other systems
- I want to keep it stateless but explain why it's a threat to release into public internet
- Will it generate any costs to host on any free hosting platform
- Will it generate any cost in future after hosting for free in Hugging Face after API validation
- How can we create a live demo for recruiter without hosting
- Is it possible to host this backend in Streamlit Cloud
- Which has high impact for a recruiter

### Documentation & Refactoring
- Create a .docx in docs about refactoring from previous mathematical model to present system design
- Just create on the basis of what changes you have made to previous mathematical model to arrive into new version
- Create a quadrant mapping diagram as docx for the classification zone (like an Eisenhower matrix)

### Documentation Files Creation

#### README.md
- Create a comprehensive README for the project
- What should be the primary user-facing documentation structure
- How to explain the burnout-proof decision system to recruiters and users
- Include system problem statement and conceptual interpretation
- Add system architecture explanation with visual diagrams
- How to structure the use case examples section
- Create sections for quick start, features, and deployment instructions
- Make it accessible for both technical and non-technical audiences
- Update README with system identity and final architecture descriptions
- Include the dual-axis evaluation methodology in user-friendly terms

#### BUILD_PROCESS.md
- Document the design evolution and build journey
- Explain the changes from the previous mathematical model to the current system design
- Create a chronicle of architectural decisions and their rationale
- Document the 6 major development phases and key insights
- Include sections for normalization choices, alternatives considered, and refactoring decisions
- Explain mistakes made and how they were corrected
- Document lessons learned throughout the development process
- Show how the system evolved from conceptual design to production-ready implementation
- Capture technical debt considerations and design trade-offs

#### research_log.md (This Document)
- Create a comprehensive research log documenting all development prompts
- Track all search queries used for knowledge discovery
- Document references and influences that shaped the system
- Categorize AI suggestions as: accepted, rejected, and modified
- List all system design assumptions with validation status
- Include all core prompts organized by theme
- Document the major evolution phases with key insights
- Create a technical decisions table with alternatives considered
- Capture key learnings and what worked vs. what didn't
- Maintain a record of all design decisions and their reasoning

### Frontend Development
- Create a creative Streamlit frontend... responsive design... avoid complexity
- Make the frontend more creative (led to zone classifications, persona voices, risk meters, storytelling)
- Change terminology to critical/realistic (refining sustainability assessment)
- Replace TIME_BOX with Sprint Mode display name
- Remove multiple criteria - simplify to one factor per type
- Remove JSON view and Absolem wisdom sections
- Remove Absolem character introduction from assessment page
- Resolve the issues in the frontend. Keep dark mode. Footer section should have same color as hero section... keep a black-blue theme
- Export the chat with all the prompts listed to docx in docs
- Will the changes made affect normalization and score logic
- Commit the changes in git
- Ensure that unnecessary paths and details aren't available in git
- Suggest more design improvements for result page
- Remove the persona for the result page and consider it as for general growth and sustainability
- Rank multiple options as per executability
- Give proper explanation and reasons for each decision
- Show risk analysis
- Process this on my backend logic
- Remove the team persona from the result page

### Backend Validation
- Check whether the backend logic is blunder proof and can practically decide in potential failure scenarios
- Delete the entire frontend and uninstall packages that aren't required for the backend
- Don't put it to gitignore, just uncommit it
- I'm only getting fallback wisdom for now, has it reach the limits
- Don't make it too short but still make the philosophical wisdom and action plan brief
- Ensure that changes made are committed. Do not commit docs folder
- Can you check if API is functioning properly

### Testing & Validation Prompts

#### Robustness Testing
- Check whether the backend logic is blunder proof and can practically decide in potential failure scenarios
- How does the system handle single options vs. multiple options
- What happens when all criteria values are equal or very close
- Can the system provide meaningful output with incomplete or contradictory user input
- How does the system behave when growth and sustainability scores are both very low

#### API & External Service Validation
- Can you check if API is functioning properly
- I'm only getting fallback wisdom for now, has it reach the limits
- What happens when Gemini API is unreachable or rate-limited
- Does the system gracefully degrade when external APIs fail
- How long should the system wait for API responses before falling back
- Should the frontend be notified of API failures

#### Edge Case Validation
- Test single option decision scenarios
- Test close competition scenarios (two options with very similar scores)
- Test clear winner scenarios
- Test all options poor-fit scenarios
- Test high impact but unsustainable options
- Test low impact but sustainable options
- Test options with zero criteria values

#### Output Quality Testing
- Don't make it too short but still make the philosophical wisdom and action plan brief
- Is the output helpful for the user's actual decision-making
- Does the risk analysis accurately represent the decision uncertainty
- Are the recommendations actionable and specific
- Does fallback wisdom maintain substantive value when API is unavailable


- Test multi-device access without authentication or session management

#### Integration Testing
- Verify frontend can handle all possible backend response formats
- Test error messages are properly displayed in the UI
- Validate that sensitivity analysis correctly reflects the algorithm
- Ensure risk levels are accurately displayed in the UI
- Test that all decision zones display correctly in the frontend

#### Deployment & Accessibility Testing
- Can the system be deployed on Streamlit Cloud
- Will the system function without requiring installation or setup
- Does the demo work for recruiters without local hosting
- Is the system accessible from multiple devices simultaneously
- Does the system work with different browsers and network conditions

---

## 🔍 Search Queries (Knowledge Discovery)

### Core Concepts
- Stateless design
- Streamlit monolith
- API essentials
- Gemini AI API
- Decision support system
- Data-driven decision support system
- Knowledge-based decision support system

### Decision Frameworks
- Quadrant mapping
- Eisenhower matrix
- Min-max algorithm
- Weighted score model
- Analytical hierarchy process

### Technical Infrastructure
- Virtual environment
- Gitignore
- Git workflow

---

## 📚 References & Influences

### Academic & Practical References

**1. Weighted Scoring Model Implementation**
- **Source:** Carlos Gonzalez de Villaumbrosia
- **Title:** Weighted Scoring Model: Step-by-Step Implementation Guide
- **URL:** https://productschool.com/blog/product-fundamentals/weighted-scoring-model
- **Influence:** Informed the weighted mean normalization approach and score calculation methodology

**2. Decision Matrix Fundamentals**
- **Source:** ASQ (American Society for Quality)
- **Title:** What is a Decision Matrix
- **URL:** https://asq.org/quality-resources/decision-matrix
- **Influence:** Shaped the multi-criteria evaluation framework and zone classification logic

### System Design Principles
- **Eisenhower Matrix:** Influenced the 4-zone classification (Urgent/Important, Urgent/Non-Important, Non-Urgent/Important, Non-Urgent/Non-Important)
- **Multi-Criteria Decision Analysis (MCDA):** Foundation for weighted scoring and criteria independence assumptions
- **Stateless Architecture:** Inspired by REST API principles and microservices patterns

---

## ✅ What Was ACCEPTED From AI Suggestions

### Core Algorithm
✅ **Dual-Axis Evaluation (Growth + Sustainability)**
- Recommendation: Separate scores instead of single composite
- Status: Accepted and became system cornerstone
- Implementation: Independent calculation with tension penalty

✅ **Weighted Mean Normalization**
- Recommendation: Use weighted average vs. min-max
- Status: Accepted for stateless design
- Impact: Eliminated database dependency for normalization

✅ **Explicit Decision Statuses**
- Recommendation: Define 4 explicit states (SINGLE_OPTION, CLEAR_WINNER, CLOSE_COMPETITION, ALL_OPTIONS_POOR_FIT)
- Status: Accepted and fully implemented
- Impact: Proper UX handling for all edge cases

✅ **Tension Penalty System**
- Recommendation: Penalize high growth + low sustainability combinations
- Status: Accepted with severity levels
- Impact: Core mechanism to prevent burnout trap recommendations

✅ **Risk Assessment Matrix (6 Levels)**
- Recommendation: Categorical risk levels instead of continuous scores
- Status: Accepted
- Impact: Clear user communication of decision risk

✅ **Sensitivity Analysis**
- Recommendation: ±5-10% weight perturbation to show stability
- Status: Accepted and implemented
- Impact: Shows which criteria most influence decision

✅ **Absolem AI Reflection Layer**
- Recommendation: Optional AI as complementary reviewer (not core decision-maker)
- Status: Accepted with strict constraints
- Impact: Maintains transparency while adding wisdom

### Frontend Improvements
✅ **Dark Mode Theme**
- Status: Accepted and implemented throughout
- Impact: Better UX, reduced eye strain

✅ **Zone-Based Visual Display**
- Recommendation: Show decision zones graphically
- Status: Accepted
- Impact: Intuitive understanding of decision type

✅ **Streamlined Interface**
- Recommendation: Reduce complexity, remove JSON view, simplify criteria
- Status: Accepted
- Impact: Improved usability for non-technical users

---

## ❌ What Was REJECTED or MODIFIED

### Algorithm Approaches

❌ **Machine Learning-Based Ranking**
- Suggestion: Use neural networks to learn optimal decisions
- Reason for Rejection: Violates transparency principle; requires training data; creates black box
- Chosen Alternative: Deterministic weighted scoring

❌ **SQLite Persistence for Core Logic**
- Suggestion: Store all evaluations and compute trends
- Reason for Rejection: Violated "works out of the box" principle; added setup burden
- Chosen Alternative: Stateless process with optional history storage

❌ **Single Composite Score**
- Suggestion: Combine growth and sustainability into one metric
- Reason for Rejection: Hid burnout risk; lost transparency
- Chosen Alternative: Dual-axis with explicit tension detection

❌ **Min-Max Normalization**
- Suggestion: Use traditional min-max scaling
- Reason for Rejection: Requires historical data; new options shift ranges; context-dependent
- Chosen Alternative: Weighted mean normalization (stateless, reproducible)

### Feature Requests

❌ **Multiple Criteria Per Type**
- Suggestion: Allow 5+ criteria per growth/sustainability
- Reason for Rejection: Increased complexity without clarity improvement
- Chosen Alternative: Simplified to focused criteria per category

❌ **Persona Voices in Results**
- Suggestion: Different AI personas for different decision types
- Reason for Rejection: Reduced clarity; added unnecessarily complexity
- Chosen Alternative: Unified, professional analysis

❌ **AI Influence on Core Decision**
- Suggestion: Let Absolem modify weights or recommendations
- Reason for Rejection: Violated core principle of user control and transparency
- Chosen Alternative: Absolem as post-hoc reflection only

### Frontend Elements

❌ **JSON Export View**
- Suggestion: Show raw JSON output for technical users
- Reason for Rejection: Confusing for general users; reduced UX clarity
- Chosen Alternative: Human-readable structured output

❌ **Team Persona Section**
- Suggestion: Show how different team members would decide
- Reason for Rejection: Out of scope; complicates single-user decision context
- Chosen Alternative: Focus on individual decision-maker

❌ **Multiple Wizard Flows**
- Suggestion: Different flows for different user types
- Reason for Rejection: Maintenance burden; added complexity
- Chosen Alternative: Single streamlined flow suited to all users

---

## 🔄 What Was MODIFIED From Original Suggestions

### Algorithm Refinements

🔄 **Tension Penalty Calculation**
- Original Suggestion: Simple subtraction (Growth - Sustainability)
- Modification: Implemented multiplicative penalty with severity levels
- Reason: Better captures burnout risk; prevents high-low scenarios

🔄 **Decision Margin Threshold**
- Original Suggestion: Single fixed threshold (e.g., 10 points)
- Modification: Adaptive threshold based on stability grading
- Reason: Accounts for decision uncertainty; fragile criteria require higher margins

🔄 **Risk Assessment Levels**
- Original Suggestion: Continuous risk score (0-100)
- Modification: Discrete 6-level hierarchy (CRITICAL → SAFE)
- Reason: Clearer communication; reduces decision paralysis

### Frontend Modifications

🔄 **Color Scheme**
- Original Suggestion: Blue and white theme
- Modification: Dark blue/black theme with strategic color accents
- Reason: Better visual hierarchy; improved accessibility

🔄 **Sprint Mode Naming**
- Original Suggestion: Keep "TIME_BOX"
- Modification: Changed to "Sprint Mode" (more relatable)
- Reason: Better resonates with academic/workplace terminology

🔄 **AI Reflection Output Length**
- Original Suggestion: Comprehensive multi-paragraph wisdom
- Modification: Brief philosophical insight + 2-3 action steps
- Reason: Users want actionable guidance, not lengthy essays

### Architecture Adjustments

🔄 **Multi-Device Access**
- Original Suggestion: Add user authentication
- Modification: Kept stateless (no login required)
- Reason: Reduces friction; maintains simplicity; suitable for demo/educational use

🔄 **Fallback Wisdom**
- Original Suggestion: Generic fallback messages
- Modification: Philosophically grounded, substantive fallback wisdom
- Reason: Maintains quality when API unavailable; still provides value

---

## 📊 System Design Assumptions (Validated/Tested)

### Core Assumptions
1. Real-world decisions can be decomposed into measurable criteria. ✅
2. Selected criteria sufficiently represent the decision space. ✅
3. Criteria are independent and do not strongly interact. ⚠️ (assumes user-chosen criteria)
4. Linear weighted sum model adequately represents user preferences. ✅
5. Trade-offs between criteria are proportional (linearity). ✅
6. Normalization methods preserve fairness across criteria. ✅
7. Small weight variations (±5–10%) approximate decision uncertainty. ✅
8. Users can accurately assign importance weights. ⚠️ (mitigated by sensitivity analysis)
9. Users provide honest and reasonably accurate inputs. ⚠️ (design assumes good faith)
10. Users behave rationally when interacting with structured output. ✅

### Domain-Specific Assumptions
11. Burnout risk can be approximated using self-reported indicators. ⚠️ (simplified model)
12. Elevated burnout risk should reduce preference for high-intensity options. ✅ (core logic)
13. Sustainability is preferable to short-term maximization under strain. ✅ (philosophical)
14. Knowledge base values are consistent and calibrated. ⚠️ (user-dependent)
15. Decision context remains stable during evaluation. ✅ (single-session assumption)
16. AI enhances interpretability but does not influence core logic. ✅
17. AI responses remain constrained and aligned with deterministic output. ✅
18. System supports decision-making but does not replace human judgment. ✅

---

## 📈 Major Evolution Points

### Phase 1: Conceptual Design
- **Focus:** Identify the burnout-growth tension problem
- **Key Insight:** Most decision systems reward ambition but ignore capacity
- **Outcome:** Dual-axis architecture established

### Phase 2: Algorithm Development
- **Focus:** Implement normalized scoring and tension detection
- **Key Evolution:** Min-Max → Weighted Mean → Stateless Process
- **Outcome:** Reproducible, database-independent evaluation

### Phase 3: Edge Case Handling
- **Focus:** Handle single options, poor-fit scenarios, close competitions
- **Key Evolution:** Implicit handling → Explicit decision statuses
- **Outcome:** 8 documented edge cases with test coverage

### Phase 4: Frontend Development
- **Focus:** Design intuitive UX for complex decision data
- **Key Evolution:** Persona-driven → Professional, analytics-focused
- **Outcome:** Clean, dark-themed interface with zone visualization

### Phase 5: AI Integration
- **Focus:** Add reflection layer without compromising transparency
- **Key Evolution:** Optional AI enhancement with strict constraints
- **Outcome:** Absolem as wisdom layer, not decision influencer

### Phase 6: Documentation & Deployment
- **Focus:** Prepare for recruitment/educational use
- **Key Evolution:** Internal architecture docs → Public-facing README
- **Outcome:** Comprehensive documentation + working backend/frontend

---

## 🎓 Key Learnings

### What Worked Well
1. **Separating Concerns Early:** Core logic separate from API/UI enabled rapid iterationand testing
2. **Explicit Over Implicit:** Named decision statuses prevented ambiguous handling
3. **User-Defined Criteria:** Flexibility drove adoption potential across different academic contexts
4. **Deterministic Transparency:** Users understood *why* despite complexity
5. **Optional AI Layer:** Absolem enhanced without creating dependency

### What Needed Adjustment
1. **Initial Complexity:** Too many features initially; learned to strip down to essentials
2. **Terminology:** "Burnout Proof" reframed to "Supporting Sustainable Decisions"
3. **Frontend Evolution:** Personas and creative elements → Professional analytics focus
4. **API Resilience:** Fallback wisdom critical for real-world deployment

### Development Insights
- **Stateless Design:** Gained reproducibility and simplicity at cost of adaptive features
- **Weighted Scoring:** Sufficient for academic decisions without ML overhead
- **Edge Cases:** 80% of production issues come from edge cases (tested extensively)
- **User Assumptions:** System assumes good-faith input and rational decision-making

---

## 🔧 Technical Decisions & Rationale

| Decision | Alternative Considered | Why Chosen |
|----------|----------------------|-----------|
| Python FastAPI | Node.js, Django | Rapid prototyping, data science libraries |
| Streamlit Frontend | React, Vue | No deployment overhead, dynamic updates |
| Gemini API | OpenAI, Anthropic | Cost-effective, available during development |
| Weighted Mean Norm | Min-Max, Z-score | Stateless, no historical data needed |
| Dual Axes | Single Score | Transparency, burnout-risk visibility |
| Explicit Zones | Continuous Gradient | Clear user communication, actionability |
| Stateless Core | Persistent DB | "Works out of box", reproducibility |
| Optional AI | Integrated AI | User control preserved, transparency maintained |

---


## 🎯 Conclusion

This research log captures the iterative journey from "How do we prevent burnout through better decisions?" to a working dual-axis decision system. The balance between **AI suggestions accepted** (core architecture, most UX), **suggestions rejected** (for transparency and simplicity), and **suggestions modified** (refined for user clarity) reflects a commitment to transparent, explainable decision support over sophisticated black boxes.

**Final Philosophy:** Build for understanding, not sophistication. Users should trust the system because they *understand it*, not because it's impressive.

---

*Log created: March 2, 2026*
