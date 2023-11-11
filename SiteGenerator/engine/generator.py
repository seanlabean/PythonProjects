

class Generator():
    def __init__(self, file_in, target):
        self.spec = ['#','-','/','<','>','*','\n']
        self.lspec = {'**': 'b', '*': 'i'}
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
        if (line[0] not in self.spec):
            line = self.parse_line(i, line)
            self.fout.write('<p>'+line+'</p>\n')

    def handle_list(self, i, line):
        in_list = False  # Track if we are inside a list
        if (line[0] == '*' or line[0] == '-') and self.prev_line is not None and self.next_line is not None:
            if self.prev_line[0] != '*' and self.prev_line[0] != '-':
                self.fout.write('<ul>')
                in_list = True
            # Check for and replace link text
            line = self.parse_line(i, line)
            self.fout.write('<li>' + line[1:] + '</li>')
            if self.next_line[0] != '*' and self.next_line[0] != '-':
                self.fout.write('</ul>')
                in_list = False
        else:
            if not in_list:
                self.fout.write('<p>' + line + '</p>')

    def handle_header(self, i, line):
        h=0
        while line[0] == '#':
            h += 1
            line = line[1:]
        if(h): self.fout.write('<h'+str(h)+'>'+line+'</h'+str(h)+'>\n')

    def parse_line(self, i, line):
        n = line
        for s, tag in self.lspec.items():
            segments = n.split(s)
            if len(segments) > 1:
                n = ""
                for i, seg in enumerate(segments):
                    if i % 2 == 0:
                        n += seg
                    else:
                        n += f"<{tag}>{seg}</{tag}>"
        return n

