# Synthetic Data Generator for FJSP Hospital Patient Processing. Reproduces the exact data set from the research paper (Table 1)

import random
import json

class HospitalDataGenerator:
    def __init__(self, seed=42):
    # Initialize with random seed for reproducibility"""
        random.seed(seed)
        
    def generate_paper_exact_data(self):     
        patients = [1, 2, 3, 4, 5]
        counters = [1, 2, 3, 4, 5]
        
        processing_times = {
            1: {1: 11, 2: 5},
            2: {2: 5, 3: 10, 4: 18},
            3: {2: 5, 3: 10},
            4: {2: 5, 3: 10, 4: 18},
            5: {1: 11, 5: 15}
        }
        
        precedence = {
            1: [(1, 2)],
            2: [(2, 3), (3, 4)],
            3: [(2, 3)],
            4: [(2, 3), (3, 4)],
            5: [(1, 5)]
        }
        
        counter_info = {
            1: {"name": "Registration/Admission", "typical_time": 11},
            2: {"name": "Initial Consultation", "typical_time": 5},
            3: {"name": "Diagnostic Testing", "typical_time": 10},
            4: {"name": "Specialist Consultation", "typical_time": 18},
            5: {"name": "Pharmacy/Discharge", "typical_time": 15}
        }
        
        patient_flow_descriptions = {
            1: "New patient: Registration to Basic consultation",
            2: "Complex case: Consultation to Diagnostics to Specialist",
            3: "Follow-up: Consultation to Diagnostics",
            4: "Complex case: Consultation to Diagnostics to Specialist",
            5: "Simple case: Registration to Pharmacy"
        }
        
        unscheduled_times = {
            1: 20,
            2: 40,
            3: 20,
            4: 38,
            5: 30
        }
        
        optimized_times_paper = {
            1: 16,
            2: 33,
            3: 15,
            4: 33,
            5: 26
        }
        
        return {
            'patients': patients,
            'counters': counters,
            'processing_times': processing_times,
            'precedence': precedence,
            'counter_info': counter_info,
            'patient_flow': patient_flow_descriptions,
            'unscheduled_times': unscheduled_times,
            'expected_optimized_times': optimized_times_paper,
            'total_operations': 12,
            'data_source': 'Survey from 3 private hospitals in Rajshahi, Bangladesh'
        }
    
    def generate_synthetic_variation(self, num_patients=5, num_counters=5, 
                                     time_variability=0.2):
        # Generate synthetic data with variations while maintaining paper structure
        base_times = {
            1: 11,
            2: 5,
            3: 10,
            4: 18,
            5: 15
        }
        
        patients = list(range(1, num_patients + 1))
        counters = list(range(1, num_counters + 1))
        processing_times = {}
        precedence = {}
        
        for patient in patients:
            num_ops = random.randint(2, 3)
            
            if random.random() < 0.8:
                ops = [2]
            else:
                ops = [random.choice(counters)]
            
            while len(ops) < num_ops:
                next_counter = random.choice([c for c in counters if c not in ops])
                ops.append(next_counter)
            
            ops.sort()
            
            processing_times[patient] = {}
            for counter in ops:
                base_time = base_times.get(counter, 10)
                variation = random.uniform(-time_variability, time_variability)
                time = int(base_time * (1 + variation))
                processing_times[patient][counter] = max(5, time)
            
            precedence[patient] = [(ops[i], ops[i+1]) for i in range(len(ops)-1)]
        
        return {
            'patients': patients,
            'counters': counters,
            'processing_times': processing_times,
            'precedence': precedence,
            'total_operations': sum(len(ops) for ops in processing_times.values()),
            'data_source': 'Synthetically generated with variability',
            'variability_factor': time_variability
        }
    
    def print_data_table(self, data):
        print("\n" + "="*80)
        print("SCHEDULE INFORMATION (Table 1 Format)")
        print("="*80)
        print("\nProcessing Time Matrix (P[i,j] in minutes):")
        print("(Includes transportation time between counters)")
        print("-"*80)
        
        header = f"{'Patient':>10}"
        for counter in data['counters']:
            header += f"{'C' + str(counter):>8}"
        header += f"{'Operations':>15}{'Sequence':>30}"
        print(header)
        print("-"*80)
        
        for patient in data['patients']:
            row = f"P{patient:>9}"
            
            for counter in data['counters']:
                if counter in data['processing_times'][patient]:
                    row += f"{data['processing_times'][patient][counter]:>8}"
                else:
                    row += f"{'—':>8}"
            
            ops = ', '.join([f"C{c}" for c in sorted(data['processing_times'][patient].keys())])
            row += f"{ops:>15}"
            
            seq = ' → '.join([f"C{c}" for c in sorted(data['processing_times'][patient].keys())])
            row += f"{seq:>30}"
            
            print(row)
        
        print("-"*80)
        print(f"Total Operations: {data['total_operations']}")
        print(f"Data Source: {data['data_source']}")
        print("="*80)
    
    def export_to_json(self, data, filename='hospital_data.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nData exported to: {filename}")
    
    def validate_data(self, data):
        # Validate that data meets paper constraints
        print("\n" + "="*80)
        print("DATA VALIDATION")
        print("="*80)
        
        validations = []
        
        if len(data['patients']) == 5:
            validations.append(("✓", "Number of patients = 5 (matches paper)"))
        else:
            validations.append(("✗", f"Number of patients = {len(data['patients'])} (paper uses 5)"))
        
        if len(data['counters']) == 5:
            validations.append(("✓", "Number of counters = 5 (matches paper)"))
        else:
            validations.append(("✗", f"Number of counters = {len(data['counters'])} (paper uses 5)"))
        
        if data['total_operations'] == 12:
            validations.append(("✓", "Total operations = 12 (matches paper)"))
        else:
            validations.append(("✗", f"Total operations = {data['total_operations']} (paper uses 12)"))
        
        all_positive = all(
            time > 0 
            for patient_times in data['processing_times'].values() 
            for time in patient_times.values()
        )
        if all_positive:
            validations.append(("✓", "All processing times are positive"))
        else:
            validations.append(("✗", "Some processing times are not positive"))
        
        precedence_valid = True
        for patient in data['patients']:
            ops = sorted(data['processing_times'][patient].keys())
            expected_precedence = [(ops[i], ops[i+1]) for i in range(len(ops)-1)]
            if data['precedence'][patient] != expected_precedence:
                precedence_valid = False
                break
        
        if precedence_valid:
            validations.append(("✓", "Precedence constraints match operation sequences"))
        else:
            validations.append(("✗", "Precedence constraints do not match operation sequences"))
        
        for symbol, message in validations:
            print(f"{symbol} {message}")
        
        print("="*80)
        
        return all(symbol == "✓" for symbol, _ in validations)


if __name__ == "__main__":
    generator = HospitalDataGenerator(seed=42)
    
    print("="*80)
    print("SYNTHETIC DATA GENERATOR FOR FJSP HOSPITAL SCHEDULING")
    print("="*80)
    
    print("\n[1] Generating EXACT data from research paper...")
    paper_data = generator.generate_paper_exact_data()
    generator.print_data_table(paper_data)
    
    is_valid = generator.validate_data(paper_data)
    
    generator.export_to_json(paper_data, 
                            '/Users/vmansur/Projects/FJSS_Patient_Processing/paper_exact_data.json')
    
    print("\n" + "="*80)
    print("EXPECTED RESULTS FROM PAPER")
    print("="*80)
    print(f"{'Patient':>10} {'Unscheduled (min)':>20} {'Optimized (min)':>20} {'Reduction (min)':>20}")
    print("-"*80)
    
    for patient in paper_data['patients']:
        unsch = paper_data['unscheduled_times'][patient]
        opt = paper_data['expected_optimized_times'][patient]
        reduction = unsch - opt
        print(f"P{patient:>9} {unsch:>20} {opt:>20} {reduction:>20}")
    
    total_unsch = sum(paper_data['unscheduled_times'].values())
    total_opt = sum(paper_data['expected_optimized_times'].values())
    total_reduction = total_unsch - total_opt
    
    print("-"*80)
    print(f"{'TOTAL':>10} {total_unsch:>20} {total_opt:>20} {total_reduction:>20}")
    print(f"{'AVERAGE':>10} {total_unsch/5:>20.1f} {total_opt/5:>20.1f} {total_reduction/5:>20.1f}")
    print("="*80)
    
    print("\n[2] Generating synthetic variation (20% variability)...")
    synthetic_data = generator.generate_synthetic_variation(num_patients=5, 
                                                           num_counters=5,
                                                           time_variability=0.2)
    generator.print_data_table(synthetic_data)
    generator.export_to_json(synthetic_data,
                            '/Users/vmansur/Projects/FJSS_Patient_Processing/synthetic_variation_data.json')
