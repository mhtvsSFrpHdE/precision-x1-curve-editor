# precision-x1-curve-editor
<img width="1032" src="https://raw.githubusercontent.com/mhtvsSFrpHdE/precision-x1-curve-editor/main/Resource/Demo.png"/>
Underclock, environment friendly, your GPU will start to counting sheep.

## What is this
MSI Afterburner have decent VF curve editor, but when click on Apply,  
the curve is always messed up and applied frequency is inaccurate.  
EVGA PRECISION X1 `1.3.7` won't mess up curve and apply accurate frequency,  
however the curve editor is crap:
- Does not support edit multiple points
- Does not support edit exact value, can only be drag by mouse

So I made this tool to generate VF curve for PRECISION X1.

## Why
Underclock a GPU usually cause less power consumption,  
which is good for electronic component life and world environment.  
However, GPU like Nvidia 1080 Ti run at high frequency,  
even if current GPU load is pretty low (23%, 1555 MHz for example).

Without using VF curve, you can only reduce frequency by 200 to 1354 MHz,  
instead of 709 MHz to let GPU load go up to about 80%.  
However, current available VF curve tool does not fit.

## How to use
See [Wiki](https://github.com/mhtvsSFrpHdE/precision-x1-curve-editor/wiki) for more details.
