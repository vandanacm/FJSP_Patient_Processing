# Flexible Job Shop Scheduling for Hospital Patient Processing

## Project Overview
Implementation of the research paper applying **Flexible Job Shop Scheduling (FJSP)** to optimize hospital patient processing time by treating patients as jobs and test counters as machines.

## Problem Statement
Hospitals face challenges serving patients efficiently due to unscheduled management systems, leading to:
- Long queues at test counters
- Excessive waiting and transportation time
- Increased total processing time (makespan)
- Poor patient experience

## Solution: FJSP Optimization
### Key Concept
- **Jobs**: Patients requiring multiple operations
- **Machines**: Hospital test counters
- **Objective**: Minimize makespan (total processing time)
- **Method**: Genetic Algorithm / Mixed Integer Linear Programming

### Mathematical Model
**Objective Function:**
```
Minimize Cmax (Makespan)
```

**Decision Variables:**
- `Cmax`: Maximum completion time (makespan)
- `Y[i,j]`: Starting time of patient j at counter i
- `Z[j,k,i]`: Binary variable for sequencing

**Constraints (43 Total):**
1. **Counter Capacity** (11 constraints): Only one patient per counter at a time
2. **Patient Precedence** (7 constraints): Operations must follow required sequence
3. **Makespan Boundary** (12 constraints): Cmax ≥ all operation completion times
4. **Non-Negativity** (13 constraints): All variables ≥ 0

## Data Set
Based on survey from 3 private hospitals in Rajshahi, Bangladesh:

| Patient | Operations (Counters) | Processing Times (min) |
|---------|----------------------|------------------------|
| P1      | C1 → C2             | 11, 5                  |
| P2      | C2 → C3 → C4        | 5, 10, 18              |
| P3      | C2 → C3             | 5, 10                  |
| P4      | C2 → C3 → C4        | 5, 10, 18              |
| P5      | C1 → C5             | 11, 15                 |

*Note: Processing times include transportation time between counters*

## Implementation Files

### 1. `fjsp_constraint_calculator.py`
Generates and displays all 43 constraints explicitly:
```bash
python3 fjsp_constraint_calculator.py
```

### 2. `fjsp_solver_milp.py`
Solves the FJSP optimization problem using PuLP MILP solver:
```bash
python3 fjsp_solver_milp.py
```

### 3. `visualize_results.py`
Creates Gantt charts comparing unscheduled vs. optimized schedules:
```bash
python3 visualize_results.py
```

## Expected Results
Based on the research paper findings:

| Patient | Unscheduled (min) | Optimized (min) | Reduction |
|---------|-------------------|-----------------|-----------|
| P1      | 20                | 16              | 4 min     |
| P2      | 40                | 33              | 7 min     |
| P3      | 20                | ~15             | ~5 min    |
| P4      | 38                | ~33             | ~5 min    |
| P5      | 30                | 26              | 4 min     |

**Key Achievement:** Eliminates waiting time for most patients through optimal scheduling

## Installation
```bash
pip3 install pulp matplotlib
```

## Usage
1. Calculate and view all 43 constraints:
   ```bash
   python3 fjsp_constraint_calculator.py
   ```

2. Run optimization solver:
   ```bash
   python3 fjsp_solver.py
   ```

3. Generate visualizations:
   ```bash
   python3 visualize_results.py
   ```

## Assumptions
1. All counters are independent
2. Each operation can be performed at one counter at a time
3. At time zero, all counters are available
4. No interruptions during operations
5. Transportation time is included in processing time data
6. Model focuses on 5 patients and 5 counters

## Limitations
- Small number of counters (5) may not generalize to larger hospitals
- Cannot completely eliminate waiting/transportation time
- Focused on outpatient testing, not bed management or operation theaters
- Results are for a specific patient flow scenario

## Future Work
- Scale to more counters and patients
- Apply to hospital bed management
- Extend to operation theater scheduling
- Real-time dynamic scheduling

## References
Research paper: "Flexible Job Shop Scheduling Optimizes Hospital Patient Processing Time"
- Authors: Sarfaraj, Lingkon, Zahan
- Implementation: MATLAB R2018a with Genetic Algorithm
- This prototype: Python with PuLP MILP solver