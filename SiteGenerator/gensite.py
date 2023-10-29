from time import time
import glob

file_in = "./demofile"

def conv_md(file_in,target,verbose=0):
    global spec
    spec = ['#','-','/','<','>','*','\n']
    f = open(file_in, "r")
    fout = open(target+file_in.split('.')[1]+'.html', "w")
    lines = f.readlines()
    # Check styling data
    # TODO: pick up style and slice away these lines
    if lines[0] != '---':
        print("No file styling given...")
        if(verbose>1): print("Include --- block at head of file!")
    # Go line by line
    for i, line in enumerate(lines):
        prev_line = lines[i-1] if i > 1 else None
        next_line = lines[i-1] if i < len(lines) else None

        # Handle regular paragraphs first.
        # TODO: put paragraph handling and sub-jobs (like list generation) in separate file.
        if (line[0] not in spec): fout.write('<p>'+line+'</p>\n')
        if line[0] == '*' or line[0] == '-' and prev_line != None and next_line != None:
            if prev_line[0] != '*' or prev_line[0] != '-':
                fout.write('<ul>')
            fout.write('<li>'+line[1:]+'</li>')
            if next_line[0] != '*' or next_line[0] != '-':
                fout.write('</ul>')
        else:
            pass
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
