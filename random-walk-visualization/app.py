import matplotlib.pyplot as plt
import random
import gradio as gr
import numpy as np
import pandas as pd

from single_agent_2D import generate_random_walk

iters = gr.Number(value=1e6,label="How many random steps?")
step_size = gr.Number(value=1,label="Step size")
random_seed = gr.Number(value=42,label="Random seed. Delete it to go full random mode, keep it for reproducibility")
    
iface = gr.Interface(fn=generate_random_walk, inputs=[iters, step_size, random_seed], outputs=["image","file"], title="2-D Random Walk", description="Uniform steps along NEWS directions only")
iface.launch()
