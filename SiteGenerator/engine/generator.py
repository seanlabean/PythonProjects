

class Generator():
    def __init__(self, file_in, target):
        self.spec = ['#','-','/','<','>','*','\n']
        self.fout = open(target+file_in.split('.')[1]+'.html', "w")
        self.f = open(file_in, "r")
        self.prev_line = ''
        self.next_line = ''
        self.style = []
        
    def open_read(self, file_in, target):
        #f = open(file_in, "r")
        #fout = open(target+file_in.split('.')[1]+'.html', "w")
        lines = self.f.readlines()
        return lines
    
    def handle_paragraph(self, i, line):
        # need to replace links and images with <href> and <figure> blocks
        if (line[0] not in self.spec): self.fout.write('<p>'+line+'</p>\n')

    def handle_list(self, i, line):
        
        if line[0] == '*' or line[0] == '-' and self.prev_line != None and self.next_line != None:
            if self.prev_line[0] != '*' or self.prev_line[0] != '-':
                self.fout.write('<ul>')
            # check for and replace link text
            self.fout.write('<li>'+line[1:]+'</li>')
            if self.next_line[0] != '*' or self.next_line[0] != '-':
                self.fout.write('</ul>')
        else:
            pass

    def handle_header(self, i, line):
        h=0
        while line[0] == '#':
            h += 1
            line = line[1:]
        if(h): self.fout.write('<h'+str(h)+'>'+line+'</h'+str(h)+'>\n')
