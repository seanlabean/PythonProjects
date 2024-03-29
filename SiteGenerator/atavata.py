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

def parse_header(f, fn, head, cat_dict):
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
        for line in head:
            f.write(line)
        f.close()

def parse_body(lex_f, fn, cat_dict):
    with open(lex_f) as inc:
        # SLICE out and process header lines
        inc_lines = inc.readlines()
        ind_head = [i for i, x in enumerate(inc_lines) if x == '---\n']
        if len(ind_head) == 2:
            # we have a header
            head = inc_lines[ind_head[0] + 1:ind_head[1]]
            body_lines = inc_lines[ind_head[1] + 1:]
        else:
            # no or erroneous head
            head = []
            body_lines = inc_lines
        inc.close()
    with open(DEST+'/'+fn+'.html', 'a') as f:
        parse_header(f, fn, head, cat_dict)
        for line in body_lines:
            f.write(markdown.markdown(line))
        f.close()

def write_footer(fn):
    with open(DEST+'/'+fn+'.html', 'a') as f:
        f.write("<footer><hr />")
        #fpedited(f, srcpath)
        f.write("<b>Sean C. Lewis</b> © 2023 — ")
        f.write("<a href='" + LICENSE + "' target='_blank'>BY-NC-SA 4.0</a>")
        f.write("</footer>")

def toc_dict(files):
    # generate table of contents dictionary
    return
def preparse_header(lex_f, fn, categories):
    with open(lex_f) as inc:
        # SLICE out and process header lines
        inc_lines = inc.readlines()
        ind_head = [i for i, x in enumerate(inc_lines) if x == '---\n']
        if len(ind_head) == 2:
            # we have a header
            head = inc_lines[ind_head[0] + 1:ind_head[1]]
            cat = [i for i, x in enumerate(head) if x.split(':')[0] == 'category']
            this_cat = head[cat[0]].split(':')[-1].strip()
            categories.setdefault(this_cat, [])
            #categories[fn] = head[cat[0]].split(':')[-1].strip()
            categories[head[cat[0]].split(':')[-1].strip()].append(fn)
        else:
            # no or erroneous head
            head = []
        inc.close()
    return categories
    
def finalize(f, fn):
    try:
        f.close()
    except:
        print(f"Error processing file {fn}")

def engine():
    lex = lexicon()
    # preprocess loop to get table of contents (which files belong to which catagories)
    categories = {}
    for lex_f in lex:
        f, fn = init_site_file(lex_f)
        preparse_header(lex_f, fn, categories)
    print(categories)
    # main processing loop
    for lex_f in lex:
        f, fn = init_site_file(lex_f)
        parse_body(lex_f, fn, categories)
        write_footer(fn)
        finalize(f, fn)
if __name__ == "__main__":
    engine()