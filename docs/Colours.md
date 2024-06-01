# Colours.md

Unfortunately you can't just include the whole Colours library like this:-

```
from Colours import *
```
You code is being run in a call to exec() and Python doesn't like it. However, you can do this:-

```
from Colours import RED,GREEN,BLUE,CYAN,YELLOW,PURPLE,MAGENTA,WHITE,BLACK
```

Alternatively to use your own colours just specify the colour as an RGB tuple. That way, you don't need to import anything from Colours.




