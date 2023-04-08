from time import time
import markdown
import glob

file_in = "./demofile"

def conv_md(file_in,target,verbose=0):
    global spec
    spec = ['#','-','/','<','>','*','\n']
    f = open(file_in, "r")
    fout = open(target+file_in.split('.')[1]+'.html', "w")
    lines = f.readlines()
    # Check styling data
    if lines[0] != '---':
        print("No file styling given...")
        if(verbose>1): print("Include --- block at head of file!")
    # Go line by line
    for line in lines:
        # Handle regular paragraphs first.
        if(line[0] not in spec): fout.write('<p>'+line+'</p>\n')
        # Headers
        h=0
        while line[0] == '#':
            h += 1
            line = line[1:]
        if(h): fout.write('<h'+str(h)+'>'+line+'</h'+str(h)+'>\n')

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
