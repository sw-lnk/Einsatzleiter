import os

from .base import *

if os.environ.get("PIPELINE") == 'production':
    from .prod import *        
else:
    from .dev import *