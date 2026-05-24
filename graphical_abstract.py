"""
Graphical Abstract — Heart Sound Performance-Inflation paper (BSPC)
Fixed: no overlap between heartbeat waveform and text. Large, bold, clear.
Run on Kaggle. Your own matplotlib code. Output: graphical_abstract.png 300 dpi.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'

INK='#0F0F23'; LEAK='#1A56DB'; BAD='#D32030'; GOOD='#0E7A6E'; SOFT='#3A3A4A'; PANEL='#EEF1F8'

fig, ax = plt.subplots(figsize=(13, 6.8), dpi=300)
ax.set_xlim(0, 13); ax.set_ylim(0, 6.8); ax.axis('off')
fig.patch.set_facecolor('white')

def heartbeat(ax, x0, y0, w, h, color, lw=2.8):
    n=400; x=np.linspace(0,1,n); y=np.zeros(n)
    y += 1.0*np.exp(-((x-0.45)/0.013)**2)
    y += -0.30*np.exp(-((x-0.49)/0.016)**2)
    y += 0.28*np.exp(-((x-0.72)/0.045)**2)
    # clip amplitude so it stays within its lane
    ax.plot(x0+x*w, y0+y*h, color=color, lw=lw, solid_capstyle='round', zorder=5)

# ===== TITLE =====
ax.text(6.5, 6.45, 'Same model and data \u2014 only the evaluation split changes',
        ha='center', va='center', fontsize=20, fontweight='bold', color=INK)
ax.text(6.5, 5.95, 'Heart sound (PCG) classification on PhysioNet/CinC 2016',
        ha='center', va='center', fontsize=13, color=SOFT, fontweight='bold')

# ===== THREE CARDS (taller, clear vertical lanes) =====
cards=[(0.6,'SEGMENT-LEVEL','leakage-prone','0.978',LEAK),
       (4.75,'RECORD-LEVEL','assumed safe','0.964',LEAK),
       (8.9,'CROSS-DATABASE','source-independent','0.503',BAD)]
cw,ch,cy=3.55,2.95,2.45
for x,title,sub,auc,color in cards:
    # shadow + card
    ax.add_patch(FancyBboxPatch((x+0.05,cy-0.07),cw,ch,boxstyle="round,pad=0.10",
                 linewidth=0,facecolor='#00000015',zorder=1))
    ax.add_patch(FancyBboxPatch((x,cy),cw,ch,boxstyle="round,pad=0.10",
                 linewidth=3.2,edgecolor=color,facecolor='white',zorder=2))
    # header strip
    ax.add_patch(FancyBboxPatch((x,cy+ch-0.60),cw,0.60,boxstyle="round,pad=0.10",
                 linewidth=0,facecolor=color,zorder=3))
    # LANE 1: title (in strip)
    ax.text(x+cw/2, cy+ch-0.30, title, ha='center', va='center',
            fontsize=15, fontweight='bold', color='white', zorder=4)
    # LANE 2: subtitle
    ax.text(x+cw/2, cy+ch-0.95, sub, ha='center', va='center',
            fontsize=12, color=SOFT, fontweight='bold', zorder=4)
    # LANE 3: heartbeat (own band, small amplitude, well separated)
    heartbeat(ax, x+0.55, cy+1.30, cw-1.1, 0.34, color)
    # LANE 4: label
    ax.text(x+cw/2, cy+0.82, 'record-level AUC', ha='center', va='center',
            fontsize=11.5, color=SOFT, fontweight='bold', zorder=4)
    # LANE 5: big number
    ax.text(x+cw/2, cy+0.32, auc, ha='center', va='center',
            fontsize=34, fontweight='bold', color=color, zorder=4)

# arrows
for xs in [4.32,8.47]:
    ax.add_patch(FancyArrowPatch((xs,cy+ch/2),(xs+0.38,cy+ch/2),
                 arrowstyle='-|>',mutation_scale=34,linewidth=4,color=SOFT,zorder=2))

ax.text(8.9+cw/2, cy-0.34, '\u25BC  near-chance (0.5)', ha='center', va='center',
        fontsize=14, fontweight='bold', color=BAD)

# ===== MECHANISM PANEL =====
py,ph=0.35,1.55
ax.add_patch(FancyBboxPatch((0.6,py),11.8,ph,boxstyle="round,pad=0.12",
             linewidth=0,facecolor=PANEL,zorder=0))
ax.text(1.1,py+ph-0.36,'WHY THE COLLAPSE?',ha='left',va='center',
        fontsize=15,fontweight='bold',color=INK)
ax.text(1.1,py+0.48,'The model learns the\nrecording source,\nnot the pathology',
        ha='left',va='center',fontsize=12.5,fontweight='bold',color=BAD)

metrics=[(5.1,'Source-identity\nprobe','0.997',BAD),
         (8.0,'Within-database\nmean','0.871',GOOD),
         (10.9,'External\n(PASCAL)','0.447',BAD)]
for x,label,val,color in metrics:
    ax.text(x,py+ph-0.38,label,ha='center',va='center',fontsize=12.5,fontweight='bold',color=INK)
    ax.text(x,py+0.45,val,ha='center',va='center',fontsize=25,fontweight='bold',color=color)
    if x<10:
        ax.plot([x+1.45,x+1.45],[py+0.25,py+ph-0.25],color='#C5CDDE',lw=1.5)

plt.subplots_adjust(left=0.01,right=0.99,top=0.99,bottom=0.01)
plt.savefig('graphical_abstract.png',dpi=300,bbox_inches='tight',facecolor='white',pad_inches=0.18)
print("Saved graphical_abstract.png (300 dpi)")
