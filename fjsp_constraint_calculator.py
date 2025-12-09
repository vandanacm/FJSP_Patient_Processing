
# Flexible Job Shop Scheduling (FJSP) for Hospital Patient Processing
# This implementation explicitly calculates all 43 constraints based on the 4 basic equations


PATIENTS = [1, 2, 3, 4, 5]
COUNTERS = [1, 2, 3, 4, 5]

P_TIME = {
    1: {1: 11, 2: 5},              # Patient 1: Counter 1 (11 min), Counter 2 (5 min)
    2: {2: 5, 3: 10, 4: 18},       # Patient 2: Counter 2 (5 min), Counter 3 (10 min), Counter 4 (18 min)
    3: {2: 5, 3: 10},              # Patient 3: Counter 2 (5 min), Counter 3 (10 min)
    4: {2: 5, 3: 10, 4: 18},       # Patient 4: Counter 2 (5 min), Counter 3 (10 min), Counter 4 (18 min)
    5: {1: 11, 5: 15}              # Patient 5: Counter 1 (11 min), Counter 5 (15 min)
}

PRECEDENCE = {
    1: [(1, 2)],           # P1: Counter 1 to Counter 2
    2: [(2, 3), (3, 4)],   # P2: Counter 2 to Counter 3 to Counter 4
    3: [(2, 3)],           # P3: Counter 2 to Counter 3
    4: [(2, 3), (3, 4)],   # P4: Counter 2 to Counter 3 to Counter 4
    5: [(1, 5)]            # P5: Counter 1 to Counter 5
}

def generate_all_constraints():    
    print("="*80)
    print("FLEXIBLE JOB SHOP SCHEDULING - CONSTRAINT GENERATION")
    print("="*80)
    print(f"\nProblem Size: {len(PATIENTS)} Patients, {len(COUNTERS)} Counters")
    print(f"Total Operations: {sum(len(ops) for ops in P_TIME.values())}")
    print()
    constraint_count = 0

    # Equation: Y[k,j] - Y[i,j] >= P[i,j]
    print("\n" + "="*80)
    print("CONSTRAINT SET 1: Counter Capacity Constraints")
    print("Rule: Only one patient can be processed at a counter at a time")
    print("="*80)
    
    capacity_constraints = []
    for counter in COUNTERS:
        patients_on_counter = [p for p in PATIENTS if counter in P_TIME[p]]
        for i, p1 in enumerate(patients_on_counter):
            for p2 in patients_on_counter[i+1:]:
                constraint_count += 1
                constraint = f"Y[{counter},{p2}] - Y[{counter},{p1}] >= {P_TIME[p1][counter]} OR Y[{counter},{p1}] - Y[{counter},{p2}] >= {P_TIME[p2][counter]}"
                capacity_constraints.append((constraint_count, counter, p1, p2, constraint))
                print(f"C{constraint_count}: Counter {counter}, Patients {p1} & {p2}")
                print(f"   Either P{p1} before P{p2}: Y[{counter},{p2}] >= Y[{counter},{p1}] + {P_TIME[p1][counter]}")
                print(f"   Or P{p2} before P{p1}: Y[{counter},{p1}] >= Y[{counter},{p2}] + {P_TIME[p2][counter]}")
    print(f"\nTotal Capacity Constraints: {len(capacity_constraints)}")
    
    # Equation: Y[i,j] - Y[i',j] >= P[i',j]
    print("\n" + "="*80)
    print("CONSTRAINT SET 2: Patient Precedence Constraints")
    print("Rule: Each patient must complete operations in required sequence")
    print("="*80)
    
    precedence_constraints = []
    for patient in PATIENTS:
        for prev_counter, next_counter in PRECEDENCE.get(patient, []):
            constraint_count += 1
            constraint = f"Y[{next_counter},{patient}] - Y[{prev_counter},{patient}] >= {P_TIME[patient][prev_counter]}"
            precedence_constraints.append((constraint_count, patient, prev_counter, next_counter, constraint))
            print(f"C{constraint_count}: Patient {patient} must finish Counter {prev_counter} before Counter {next_counter}")
            print(f"   Y[{next_counter},{patient}] >= Y[{prev_counter},{patient}] + {P_TIME[patient][prev_counter]}")
    print(f"\nTotal Precedence Constraints: {len(precedence_constraints)}")
    
    # Equation: Cmax - Y[i,j] >= P[i,j]
    print("\n" + "="*80)
    print("CONSTRAINT SET 3: Makespan Boundary Constraints")
    print("Rule: Cmax must be >= completion time of every operation")
    print("="*80)
    
    makespan_constraints = []
    for patient in PATIENTS:
        for counter in P_TIME[patient].keys():
            constraint_count += 1
            constraint = f"Cmax - Y[{counter},{patient}] >= {P_TIME[patient][counter]}"
            makespan_constraints.append((constraint_count, patient, counter, constraint))
            print(f"C{constraint_count}: Cmax >= Y[{counter},{patient}] + {P_TIME[patient][counter]} (Patient {patient}, Counter {counter})")
    print(f"\nTotal Makespan Boundary Constraints: {len(makespan_constraints)}")
    
    # Equation: All variables >= 0
    print("\n" + "="*80)
    print("CONSTRAINT SET 4: Non-Negativity Constraints")
    print("Rule: All time variables must be non-negative")
    print("="*80)

    non_negativity_constraints = []
    
    # Cmax >= 0
    constraint_count += 1
    print(f"C{constraint_count}: Cmax >= 0")
    non_negativity_constraints.append((constraint_count, "Cmax >= 0"))
    
    # Y[i,j] >= 0 for all operations
    for patient in PATIENTS:
        for counter in P_TIME[patient].keys():
            constraint_count += 1
            constraint = f"Y[{counter},{patient}] >= 0"
            non_negativity_constraints.append((constraint_count, constraint))
            print(f"C{constraint_count}: Y[{counter},{patient}] >= 0")
    print(f"\nTotal Non-Negativity Constraints: {len(non_negativity_constraints)}")

    print("\n" + "="*80)
    print("CONSTRAINT SUMMARY")
    print("="*80)
    print(f"Set 1 - Counter Capacity:        {len(capacity_constraints)} constraints")
    print(f"Set 2 - Patient Precedence:      {len(precedence_constraints)} constraints")
    print(f"Set 3 - Makespan Boundary:       {len(makespan_constraints)} constraints")
    print(f"Set 4 - Non-Negativity:          {len(non_negativity_constraints)} constraints")
    print(f"{'-'*80}")
    print(f"TOTAL CONSTRAINTS:               {constraint_count} constraints")
    print("="*80)
    
    return {
        'capacity': capacity_constraints,
        'precedence': precedence_constraints,
        'makespan': makespan_constraints,
        'non_negativity': non_negativity_constraints,
        'total': constraint_count
    }

if __name__ == "__main__":
    constraints = generate_all_constraints()
