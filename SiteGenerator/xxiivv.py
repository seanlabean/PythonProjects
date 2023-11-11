import os
import time

# Constants
NAME = "100R"
DOMAIN = "https://100r.co/"
LICENSE = "https://github.com/hundredrabbits/100r.co/blob/main/LICENSE.by-nc-sa-4.0.md"
SOURCE = "https://github.com/hundredrabbits/100r.co/edit/main"

# Data structure to store file references
class Lexicon:
    def __init__(self):
        self.len = 0
        self.refs = [0] * 512
        self.files = [""] * 512

# Utility functions for string manipulation
def clca(c):
    return c.lower() if 'A' <= c <= 'Z' else c

def cuca(c):
    return c.upper() if 'a' <= c <= 'z' else c

def slen(s):
    i = 0
    while s[i]:
        i += 1
    return i

def st__(s, fn):
    i = 0
    while s[i]:
        s[i] = fn(s[i])
        i += 1
    return s

def stuc(s):
    return st__(s, cuca)

def stlc(s):
    return st__(s, clca)

def scpy(src, dst, length):
    i = 0
    while src[i] and i < length - 2:
        dst[i] = src[i]
        i += 1
    dst[i + 1] = '\0'
    return dst

def scmp(a, b):
    i = 0
    while a[i] == b[i]:
        if not a[i]:
            return 1
        i += 1
    return 0

def scsw(s, a, b):
    i = 0
    while s[i]:
        if s[i] == a:
            s[i] = b
        i += 1
    return s

def scat(dst, src):
    ptr = len(dst)
    for char in src:
        dst[ptr] = char
        ptr += 1
    dst[ptr] = '\0'
    return dst

def ssin(s, ss):
    a = 0
    b = 0
    while s[a]:
        if s[a] == ss[b]:
            if not ss[b + 1]:
                return a - b
            b += 1
        else:
            b = 0
        a += 1
    return -1

def ccat(dst, c):
    length = slen(dst)
    dst[length] = c
    dst[length + 1] = '\0'
    return dst

# Function to inject content into the HTML template
def fpinject(f, l, filepath):
    inc = None
    s = ""
    t = 0

    filepath = scsw(filepath, ' ', '_')

    try:
        inc = open(filepath, "r")
    except FileNotFoundError:
        return error("Missing include", filepath)

    s = ""
    for c in inc.read():
        if c == '}':
            t = 0
            if not fptemplate(f, l, s):
                return 0
            continue
        if c == '{':
            s = ""
            t = 1
            continue
        if slen(s) > 1023:
            return error("Templating error", filepath)
        if t:
            ccat(s, c)
        else:
            f.write(c)

    inc.close()
    return 1

# Function to generate the index page
def fpindex(f):
    d = sorted(os.listdir("src/inc"))
    f.write("<ul class='col2 capital'>")
    for filename in d:
        if filename[0] != '.':
            filepath = filename
            filename = scsw(scpy(filename, [0] * 64, 64), '_', ' ')
            f.write(f"<li><a href='{filepath}'>{filename}</a></li>")
    f.write("</ul>")
    return 1

# Function to handle errors and print error messages
def error(msg, val):
    print(f"Error: {msg}({val})")
    return 0

# Function to find a file in the Lexicon
def findf(l, f):
    filename = scat(scsw(stlc(scpy(f, [0] * 64, 64)), ' ', '_'), ".htm")
    for i in range(l.len):
        if scmp(l.files[i], filename):
            return i
    return -1

# Function to add information about the last edit in the footer
def fpedited(f, path):
    attr = os.stat(path)
    f.write("<span style='float:right'>")
    f.write("Edited on " + time.ctime(attr.st_mtime) + " ")
    f.write("<a href='" + SOURCE + path + "'>[edit]</a><br/>")
    f.write("</span>")

# Function to handle portal content
def fpportal(f, l, s, head):
    target = findf(l, s)
    srcpath = [0] * 64
    filename = [0] * 64

    if target < 0:
        return error("Missing portal", s)

    scat(scat(scat(srcpath, "src/inc/"), scpy(s, filename, 64)), ".htm")

    if head:
        f.write("<h2 id='" + scsw(filename, ' ', '_') + "'>")
        f.write("<a href='" + filename + ".html'>" + s + "</a></h2>")

    fpinject(f, l, srcpath)
    l.refs[target] += 1
    return 1

# Function to handle templated content
def fptemplate(f, l, s):
    target = None

    if s[0] == '/':
        return fpportal(f, l, s[1:], 1)

    target = findf(l, s)

    if target < 0:
        return error("Missing link", s)

    f.write("<a href='" + scsw(stlc(s), ' ', '_') + ".html' class='local'>")
    f.write(scat(scat(scat(stlc(s), '_', ' '))))

    l.refs[target] += 1
    return 1

# Function to generate the HTML content
def build(f, l, name, srcpath):
    if not f:
        return f

    # begin
    f.write("<!DOCTYPE html><html lang='en'>")
    f.write("<head>")
    f.write(
        "<meta charset='utf-8'>"
        "<meta name='thumbnail' content='" + DOMAIN + "media/services/rss.jpg' />"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<link rel='alternate' type='application/rss+xml' title='RSS Feed' "
        "href='../links/rss.xml' />"
        "<link rel='stylesheet' type='text/css' href='../links/main.css'>"
        "<link rel='shortcut icon' type='image/png' "
        "href='../media/services/shortcut.png'>"
        "<title>" + NAME + " &mdash; " + name + "</title>"
    )
    f.write("</head>")
    f.write("<body>")

    # header
    f.write("<header>")
    f.write("<a href='home.html'><img src='../media/interface/logo.svg' alt='" + NAME + "' height='50'></a>")
    f.write("</header>")

    # nav
    f.write("<nav>")
    if not fpportal(f, l, "meta.nav", 0):
        print(">>> Building failed: " + name)
    f.write("</nav>")

    # main
    f.write("<main>\n\n")
    f.write("<!-- Generated file, do not edit -->\n\n")
    f.write("<h1>" + name + "</h1>")

    if not fpinject(f, l, srcpath):
        print(">>> Building failed: " + name)

    f.write("\n\n</main>")

    # footer
    f.write("<footer><hr />")
    fpedited(f, srcpath)
    f.write("<b>Hundredrabbits</b> © 2023 — ")
    f.write("<a href='" + LICENSE + "' target='_blank'>BY-NC-SA 4.0</a>")
    f.write("</footer>")

    # end
    f.write("</body></html>\n")
    return f

# Function to generate HTML files for the Lexicon
def generate(l):
    i = 0
    srcpath = [0] * 64
    dstpath = [0] * 64
    filename = [0] * 64

    for i in range(l.len):
        scpy(l.files[i], filename, ssin(l.files[i], ".htm") + 1)
        scat(scat(scat(srcpath, "src/inc/"), filename), ".htm")
        scat(dstpath, "site/")
        scat(dstpath, filename)
        scat(dstpath, ".html")
        build(open(dstpath, "w"), l, scsw(filename, '_', ' '), srcpath)
    print("Generated " + str(i) + " files")
    return 1

# Function to index the content in the Lexicon
def index(l, d):
    while True:
        try:
            dir_entry = next(d)
        except StopIteration:
            break

        if ssin(dir_entry.name, ".htm") > 0:
            l.refs[l.len] = 0
            scpy(dir_entry.name, l.files[l.len], 128)
            l.len += 1

    print("Indexed " + str(l.len) + " terms")
    l.refs[l.len] = 0
    scpy("index.htm", l.files[l.len], 128)
    f = open("src/inc/index.htm", "w")
    fpindex(f)
    f.close()
    return 1

# Function to inspect the Lexicon for orphaned content
def inspect(l):
    for i in range(l.len):
        if not l.refs[i]:
            error("Orphaned", l.files[i])

# Main function
def main():
    lex = Lexicon()
    d = None
    lex.len = 0

    try:
        d = os.scandir("src/inc")
    except FileNotFoundError:
        return error("Open", "Missing src/inc/ folder.")

    if not index(lex, d):
        return error("Indexing", "Failed")

    if not generate(lex):
        return error("Generating", "Failed")

    inspect(lex)
    return 0

# Entry point of the script
if __name__ == "__main__":
    main()