import os
import random
import re
import sys
import numpy

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #print("-------------------------")
    #print("transition_model:")
    #print("page: ", page)
    pages = dict()
    d = damping_factor * 1000
    sum = 0
    for filename in corpus:
        if filename == page:
            continue
        #print(f"if filename is in page: filename={filename}")
        if filename in corpus[page]:
            percentage = ((d / len(corpus[page])) + ((1000 - d) / (len(corpus) - 1))) / 1000
            sum += percentage
            #print(f"percentage = ({d} / {len(corpus[page])}) + (100 - {d} / {(len(corpus) - 1)})")

            #print(f"adding page: {filename} : {percentage}, len(corpus[filename])={len(page)}, corpus[filename]={page}")
            pages[filename] = percentage

        elif not corpus[page]:
            percentage = 1 / (len(corpus) - 1)
            sum += percentage

            pages[filename] = percentage

        else: 
            percentage = ((1000 -d) / (len(corpus) - 1)) / 1000
            sum += percentage

            #print(f"adding page: {filename} : {percentage}")
            pages[filename] = percentage
        #print("")
                
    #print("")
    #print("transition_model return:",pages)
    #print("sum = ", sum)
    #print("-------------------------")
    return pages



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print("++++++++++++++++++++++++++++++++++++++++++")
    #print("corpus: ", corpus)
    samples = dict()
    firstsample = random.choice(list(corpus.items()))
    #print("first sample: ",firstsample[0])
    parent = firstsample[0]

    for i in range(n):
        if parent in samples:
            samples[parent] += 1
        else:
            samples[parent] = 1 
        parent_links = transition_model(corpus,parent,damping_factor)
        parent_links_probability = list()
        parent_links_items = list()
        for link in parent_links:
            parent_links_probability.append(parent_links[link])
            parent_links_items.append(link)
        parent = numpy.random.choice(parent_links_items, p=parent_links_probability)
    for page in samples:
        samples[page] = ((samples[page] * 10000) / n) / 10000
    #print("++++++++++++++++++++++++++++++++++++++++++")    
    return samples

    
        

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print("++++++++++++++++++++++++++++++++++++++++++")
    #print("corpus = ",corpus )
    #print("")
    page_rank = dict()
    d = damping_factor

    #all pages have equal PR()
    for page in corpus:
        page_rank[page] = 1 / len(corpus)
    #print("page_rank = ",page_rank)

    prsum = 0
    old_page_rank = 2
    new_page_rank = 1

    for n in range(sys.maxsize**999): 
        for page in page_rank:
            #print("page = ",page)
            old_page_rank = page_rank[page]

            #all pages that links to page
            page_link = set()

            for p in corpus:
                #print("corpus[p] = ", corpus[p])
                if page in corpus[p]:
                    page_link.add(p)
                elif not corpus[p]:
                    page_link.add(p)

            #print("page_link = ", page_link)
            #print("")
            
            #print("second condition")
            sec_cond = set()
            #the PR() of every page devided by its numlinks()
            for p in page_link:
                #print("p = ", p)
                if corpus[p]:
                    sec_cond.add(page_rank[p] / (len(corpus[p]) )* d)
                else:
                    sec_cond.add(page_rank[p] / (len(corpus) )* d)
                    
            #print("")

            
            #print("updating page_rank")
            first_codition = (1 - d) / len(corpus)
            #print("first_codition = ", f"(1 - {d}) / {len(corpus)}"," = " ,first_codition)
            #print("sum(sec_cond) = ", sum(sec_cond))
            new_page_rank = first_codition + sum(sec_cond)
            page_rank[page] = first_codition + sum(sec_cond)
            #print("")
            prsum = 0
            for pr in page_rank:
                prsum += page_rank[pr]
           #print("prsum = ", prsum)
            if round(prsum, 15) == 1  and ((old_page_rank - new_page_rank) < 0.001 or (old_page_rank - new_page_rank) > -0.001):
                return page_rank
        #print("page_rank = ", page_rank)
        #print("ºººººººººººººººººººººººººººººººººººººººº")
          
    #print("++++++++++++++++++++++++++++++++++++++++++")
    return page_rank


if __name__ == "__main__":
    main()
