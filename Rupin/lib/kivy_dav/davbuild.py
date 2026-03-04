#Codint:utf-8

import sys
try:
	from .box import box
	from .anchor import anchor
	from .stack import stack
	from .grid import grid
	from .scroll import scroll,scroll_new
	from .float_l import float_l
	from .wid import *
	from .layout import layout
	from .Calen import *
	from .Custom_Thread import *
	from .relative import relative
	from . import decos
	from .recycle import (MyItem,MyRecycleLayout,vscroll,MyHorizontalItem,MyHorizontalRecycleLayout,
			hscroll)
	from .button import but as custom_but
	from .metrics import dp,sp
	#from .draw import *
except ImportError:
	from box import box
	from anchor import anchor
	from stack import stack
	from grid import grid
	from scroll import scroll,scroll_new
	from float_l import float_l
	from wid import *
	from layout import layout
	from Calen import *
	from Custom_Thread import *
	from relative import relative
	import decos
	from button import but as custom_but
	from metrics import dp,sp
	from recycle import (MyItem,MyRecycleLayout,vscroll,MyHorizontalItem,MyHorizontalRecycleLayout,
			hscroll)
	#from draw import *

from kivy.graphics import Line,Color,Ellipse
import asyncio
import random
from operator import itemgetter

from kivy.clock import Clock
from functools import partial


