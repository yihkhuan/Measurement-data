def testing(arg,args, **kwargs):
    print(arg)
    print(args[0])
    if kwargs.get('a') is not None:
        print(kwargs.get('a'))

tup = (77, "bb")
testing(65, tup, a = "jj")
import numpy as np
x = np.linspace(0,np.pi, 100)
y = np.sin(x)
title = None
from matplotlib import pyplot as plt
fig, ax = plt.subplots()
def pot(x, y, title,axs):
    axs.plot(x,y)
    axs.set_title(title,fontsize = 25)
    return ax, x
z = lambda x: x+x
ax, x, *r = pot(x,y,title,ax)
ax.set_xlabel("haha")
ax.set_ylabel("hahaha")
print(type(z))

plt.show()
plt.close()