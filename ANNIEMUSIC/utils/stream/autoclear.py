#
# Copyright (C) 2024 by Moonshining1@Github, < https://github.com/Moonshining1 >.
#
# This file is part of < https://github.com/Moonshining1/ANNIE-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/Moonshining1/ANNIE-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#

import os

from config import autoclean


async def auto_clean(popped):
    try:
        rem = popped["file"]
        autoclean.remove(rem)
        count = autoclean.count(rem)
        if count == 0:
            if "vid_" not in rem or "live_" not in rem or "index_" not in rem:
                try:
                    os.remove(rem)
                except:
                    pass
    except:
        pass
