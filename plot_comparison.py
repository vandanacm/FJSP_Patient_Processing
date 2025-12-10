
import matplotlib.pyplot as plt
import numpy as np

patients = ['P1', 'P2', 'P3', 'P4', 'P5']
unscheduled = [20, 40, 20, 38, 30]  
paper_ga =    [16, 33, 20, 38, 26]  
our_milp =    [16, 33, 15, 33, 26]  
x = np.arange(len(patients))
width = 0.25
fig, ax = plt.subplots(figsize=(10, 6))

rects1 = ax.bar(x - width, unscheduled, width, label='Unscheduled (Survey)', color='#d6d6d6', hatch='//')
rects2 = ax.bar(x, paper_ga, width, label='Paper GA (Heuristic)', color='#6baed6')
rects3 = ax.bar(x + width, our_milp, width, label='Our MILP (Exact)', color='#08519c')

ax.set_ylabel('Processing Time (minutes)', fontsize=12)
ax.set_title('Methodology Comparison: Processing Time per Patient', fontsize=14, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(patients, fontsize=11)
ax.legend(loc='upper right')
ax.yaxis.grid(True, linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

def autolabel(rects, is_improvement=False):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
autolabel(rects1)
autolabel(rects2)
autolabel(rects3, is_improvement=True)

ax.set_ylim(0, 50)
ax.annotate('25% Less', xy=(x[2]+width, 18), xytext=(x[2]+width, 24),
            arrowprops=dict(facecolor='black', arrowstyle='->'),
            ha='center', fontsize=9, color='#d62728', fontweight='bold')
ax.annotate('13% Less', xy=(x[3]+width, 36), xytext=(x[3]+width, 42),
            arrowprops=dict(facecolor='black', arrowstyle='->'),
            ha='center', fontsize=9, color='#d62728', fontweight='bold')

plt.tight_layout()
plt.savefig('comparison_plot.png', dpi=300)
print("Plot generated: comparison_plot.png")