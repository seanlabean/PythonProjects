from time import time
import glob
from engine.generator import Generator

file_in = "./demofile"

def conv_md(file_in,target,verbose=0):
    g = Generator(file_in, target)
    fout = g.fout
    lines = g.open_read(file_in, target)
    # Check styling data
    # TODO: pick up style and slice away these lines
    if lines[0] != '---':
        print("No file styling given...")
        if(verbose>1): print("Include --- block at head of file!")
    else:
        # call get_styling()
        # set g.style = [...,...,...]
        pass
    for i, line in enumerate(lines):
        if line[:3] == '---': continue
        g.prev_line = lines[i-1] if i > 2 else None
        g.next_line = lines[i-1] if i < len(lines) else None

        g.handle_paragraph(i, line)
        g.handle_list(i, line)
        g.handle_header(i, line)

def main(src,target,verbose=0):
    tick = time()
    files = glob.glob(src+'*.md')
    for f in files:
        if(verbose>0): print(f)
        conv_md(f,target,verbose)
    tock = time()
    if(verbose>0): print('Converted all files in '+src+' to HTML in {:.2f}s.'\
                         .format(tock-tick))

if __name__ == "__main__":
    main('./','./site',verbose=1)
