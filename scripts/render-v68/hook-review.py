"""Review the explicitly requested snap hook at the native recessed mount."""
import os,runpy
from pathlib import Path
os.environ['BOP_RENDER_MODE']='setup';g=runpy.run_path(str(Path(__file__).resolve().parent/'native-studio.py'));globals().update(g)
palette({'number':8,'body':'#bccc72','accent':'#19344c'});s.frame_set(6);s.render.resolution_x=1200;s.render.resolution_y=1100;camera((.073,-.12,.185),(.041,0,.155),.045);s.render.filepath=os.environ.get('BOP_HOOK_REVIEW_OUT',str(ROOT/'docs/v68/snap-hook-render.png'));bpy.ops.render.render(write_still=True)
