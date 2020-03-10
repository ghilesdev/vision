import os
import shutil
from pathlib import Path

"""
    copies all files in subdir into dir and renames them
"""
dest = "dataset\\nodefects"
count = 0
for src, dir, files in os.walk("dataset\\noDefect"):
    print(src)

    for file in files:
        path = os.path.join(src, file)

        # if os.path.isfile(path):
        #     print(dest+path)

        count += 1
        # print(paths)
        new_path = shutil.copy(path, dest)
        p = Path(new_path)
        p.rename(Path(p.parent, f"{p.stem}_{count}_{p.suffix}"))
        # print('new path', new_path)
        # shutil.move(new_path,  new_path[-1]+str(count))
        # print(name)
