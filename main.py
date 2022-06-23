import os
import pygame
from Executor import *
from instance_viz import *

"""
TODO:
Modularize the stuff
"""

ex_state = ['clear red','clear blue','clear yellow','handempty','on blue orange', 'ontable red','ontable orange','ontable yellow', 'holding cyan']
goal_state = ['on orange blue']
plan = ['unstack blue orange','put-down blue','pick-up orange','stack orange blue']


pygame.init()
pygame.font.init()

frame_count = 0
exiting = False
init_state = ex_state

encoded_objects =   {"a": "red block", "b": "blue block", "c": "orange block", "d": "yellow block",
   "e": "white block", "f": "magenta block", "g": "black block", "h": "cyan block",
   "i": "green block", "j": "violet block", "k": "silver block", "l": "gold block" }
output_file = "outputs/task1_reasoning.txt"
rev_encoded_objects = dict([(value,key) for key,value in encoded_objects.items()])
def get_plan(inst_lines):
    flag=False
    plan = []
    for line in inst_lines:
        if "[PLAN END]" in line:
            flag=False
        if flag:
            action, objects = line.split('the')[0].strip(),[i.split('block')[0].strip() for i in line.split('the')[1:]]
            action = action.strip().replace(' ','-')
            objects = [rev_encoded_objects[i+' block'] for i in objects]
            plan.append(action+'_'+'_'.join(objects))
        if "--- GPT3 response" in line:
            flag=True
    return plan

with open(output_file) as f:
    lines = f.readlines()
    gpt3_instances = {}
    instance = ""
    curr_inst = ""
    for i in lines:
        if "Instance " in i:
            curr_inst+=i
        if "SUCCESS" in i or "FAILURE" in i:
            path = curr_inst.split('\n')[1].split(' ')[2].strip()
            instance = ""
            curr_inst = ""
        elif "==============" in i:
            #print(instance)
            gpt3_instances[path]=get_plan(instance.split('\n'))
        instance+=i

def decode_objects(states):
    flag=False
    if not isinstance(states, list):
        flag=True
        states = [states]
    modified_states = []
    for state in states:
        modified_state = []
        for pred in state:
            new_pred = pred.split('_')
            new_pred = new_pred[0]+' '+' '.join([encoded_objects[i].replace('block','').strip() for i in new_pred[1:]])
            modified_state.append(new_pred)
        modified_states.append(modified_state)
    if flag:
        return modified_states[0]
    else:
        return modified_states


domain = './instances/generated_domain.pddl'
single_inst = list(gpt3_instances.keys())[0]
executor = Executor(domain,single_inst)
goal_state = decode_objects(executor.goal_state)
all_states = decode_objects(executor.get_all_states(executor.init_state, gpt3_instances[single_inst]))
print("GOAL",goal_state)
for j in all_states:
    print(j)
viz_loc = f"./visualizations/{single_inst.split('/')[-1].split('.')[0]}/"
os.makedirs(viz_loc, exist_ok=True)

ins_viz = Instance_Viz()
for ind,state in enumerate(all_states):
    ins_viz.get_state_viz(state, goal_state, ind)
    pygame.display.update()
    pygame.image.save(ins_viz.screen, viz_loc+str(ind)+".jpg")
    ins_viz.screen.fill((0,0,0))

import imageio
images = []
for filename in sorted(os.listdir(viz_loc)):
    if 'gif' in filename:
        continue
    images.append(imageio.imread(viz_loc+filename))
imageio.mimsave(viz_loc+"gpt3.gif", images, duration=1)
