import os
import sys

sys.path.append(os.path.join(os.getcwd(), "paper", "figures"))
from pycore.tikzeng import *
from pycore.blocks import *

PLOTNN_DIR = os.path.join(os.getcwd(), "paper", "figures")

#%%

arch = [
    to_head(PLOTNN_DIR),
    to_cor(),
    to_begin(),
    # input
    to_input(os.path.join(PLOTNN_DIR, "bedmap2_preview.png"), to="(-1.5,0,0)", width=3, height=3),
    # Input Convolutions
    to_Conv(name="x", s_filer=10, n_filer=32, offset="(0,0,0)", to="(0,0,0)", width=1.6, height=10, depth=10),
    to_Conv(name="w1", s_filer=10, n_filer=32, offset="(0,3,0)", to="(0,0,0)", width=1.6, height=10, depth=10),
    to_Conv(name="w2", s_filer=10, n_filer=32, offset="(0,-3,0)", to="(0,0,0)", width=1.6, height=10, depth=10),
    to_Conv(name="concat", s_filer=8, n_filer=96, offset="(1.2,0,0)", to="(x-east)", width=4.8, height=8, depth=8, caption="Concat-enated Inputs"),
    to_connection(of="x", to="concat"),
    to_connection(of="w1", to="concat"),
    to_connection(of="w2", to="concat"),
    # RRDB Blocks
    to_Conv(name="pre-residual", s_filer=8, n_filer=64, offset="(1.2,0,0)", to="(concat-east)", width=3.2, height=8, depth=8, caption="Pre-residual"),
    to_connection(of="concat", to="pre-residual"),
    to_Pool(name="ghost-skip1", offset="(0.4,0,0)", to="(pre-residual-east)", width=0, height=0.1, depth=0.1, opacity=0.0),

    to_Conv(name="block1", s_filer=8, n_filer=64, offset="(0.8,0,0)", to="(pre-residual-east)", caption="Block 1", width=8, height=8, depth=8),
    to_connection(of="pre-residual", to="block1"),
    to_Conv(name="block2", s_filer=8, n_filer=64, offset="(0.8,0,0)", to="(block1-east)", caption="Block 2", width=8, height=8, depth=8),
    to_connection(of="block1", to="block2"),
    to_Conv(name="blockB", s_filer=8, n_filer=64, offset="(0.8,0,0)", to="(block2-east)", caption="Block B", width=8, height=8, depth=8),
    to_connection(of="block2", to="blockB"),
    # Post-RRDB Layers
    to_Conv(name="post-residual", s_filer=8, n_filer=64, offset="(0.8,0,0)", to="(blockB-east)", width=3.2, height=8, depth=8, caption="Post-residual"),
    to_connection(of="blockB", to="post-residual"),
    to_Pool(name="ghost-skip2", offset="(0.4,0,0)", to="(post-residual-east)", width=0, height=0.1, depth=0.1, opacity=0.0),

    to_skip(of="ghost-skip1", to="ghost-skip2", pos=75),

    to_UnPool(name="upsample1", offset="(1.2,0,0)", to="(post-residual-east)", width=1.6, height=16, depth=16),
    to_connection(of="post-residual", to="upsample1"),
    to_UnPool(name="upsample2", offset="(0.3,0,0)", to="(upsample1-east)", width=1.6, height=24, depth=24, caption="Pixel-Shuffle Blocks 1\&2"),
    to_connection(of="upsample1", to="upsample2"),

    to_Conv(name="final-conv-block", s_filer=32, n_filer=32, offset="(1.2,0,0)", to="(upsample2-east)", width=1.6, height=24, depth=24, caption="Final Conv Block"),
    to_connection(of="upsample2", to="final-conv-block"),

    to_Conv(name="deepbedmap-dem", s_filer=32, n_filer=1, offset="(1.2,0,0)", to="(final-conv-block-east)", width=0.5, height=24, depth=24, caption="Deep-BedMap-DEM"),
    to_connection(of="final-conv-block", to="deepbedmap-dem"),

    to_end(),
]

to_generate(arch, os.path.join(PLOTNN_DIR, "deepbedmap_architecture.tex"))
!pdflatex -output-dir {PLOTNN_DIR} {os.path.join(PLOTNN_DIR, 'deepbedmap_architecture.tex')}
