import markdown
from glob import glob
global INCL; INCL = "./inc"
global DEST; DEST = "./site"
global NAME; NAME = "ATAVATA"
global DOMAIN; DOMAIN = "www.sc-lewis.com"
global LICENSE; LICENSE = "NULL"

def lexicon():
    return glob(INCL+"/*.md")

def init_site_file(lex_f):
    fn = lex_f.split('/')[-1]
    fn = fn.split('.')[0]
    with open(DEST+'/'+fn+'.html', 'w') as f:
        return f, fn

def parse_header(f, fn):
    with open(DEST+'/'+fn+'.html', 'w') as f:
        f.write("<!DOCTYPE html><html lang='en'>")
        f.write("<header>")
        f.write("<a href='home.html'><img src='../media/interface/logo.svg' alt='" + NAME + "' height='50'></a>")
        f.write("</header>")
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
            "<title>" + NAME + " &mdash; " +  fn + "</title>"
            )
        f.write("</head>")
        f.write("<body>")

        # header
        f.write("<header>")
        f.write("<a href='home.html'><img src='../media/interface/logo.svg' alt='" + NAME + "' height='50'></a>")
        f.write("</header>")
        f.close()

def parse_body(lex_f, fn):
    with open(lex_f) as inc:
        with open(DEST+'/'+fn+'.html', 'a') as f:
            # SLICE out and process header lines
            parse_header(f, fn)
            for line in inc.readlines():
                
                f.write(markdown.markdown(line))
            f.close()

def write_footer(fn):
    with open(DEST+'/'+fn+'.html', 'a') as f:
        f.write("<footer><hr />")
        #fpedited(f, srcpath)
        f.write("<b>Sean C. Lewis</b> © 2023 — ")
        f.write("<a href='" + LICENSE + "' target='_blank'>BY-NC-SA 4.0</a>")
        f.write("</footer>")
    
def finalize(f, fn):
    try:
        f.close()
    except:
        print(f"Error processing file {fn}")


def engine():
    lex = lexicon()
    for lex_f in lex:
        f, fn = init_site_file(lex_f)
        parse_body(lex_f, fn)
        write_footer(fn)
        finalize(f, fn)
if __name__ == "__main__":
    engine()