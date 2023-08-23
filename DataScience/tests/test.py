import sys
sys.path.insert(0,'../')
from interp import LinearInterpolator
import numpy as np

rng = np.random.default_rng(42)
xx = rng.uniform(0,2*np.pi,20)
yy = np.sin(xx)
li = LinearInterpolator(xx,yy)
print(li(2))
