import matplotlib.pyplot as plt
import random
import gradio as gr
import numpy as np
import pandas as pd

from single_agent_2D import generate_random_walk
from multi_agent_2D import multi_agent_walk

iters_single = gr.Number(value=1e6,label="How many random steps?")
iters_multi = gr.Number(value=1e6,label="How many random steps?")

step_size_single = gr.Number(value=1,label="Step size")
step_size_multi = gr.Number(value=1,label="Step size")

agent_count = gr.Number(value=3, label = "Number of agents")

random_seed_single = gr.Number(value=42,label="Random seed. Delete it to go full random mode, keep it for reproducibility")
random_seed_multi = gr.Number(value=42,label="Random seed. Delete it to go full random mode, keep it for reproducibility")
    
iface1 = gr.Interface(
                      fn=generate_random_walk, 
                      inputs=[iters_single, step_size_single, random_seed_single], 
                      outputs=["image","file"], 
                      title="2-D Random Walk", 
                      description="Uniform steps along NEWS directions only",
                     )
iface2 = gr.Interface(
                      fn=multi_agent_walk, 
                      inputs=[agent_count,iters_multi, step_size_multi, random_seed_multi], 
                      outputs=["image","file"], 
                      title="Multi-Agent 2D Random Walk",
                     )

combinedinterface = gr.TabbedInterface([iface1,iface2],['Single Particle Random Walk', 'Multi-Particle Random Walk'])
combinedinterface.launch()
