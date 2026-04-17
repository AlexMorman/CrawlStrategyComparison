import re, bz2
from collections import defaultdict

class DBPediaParser:

    def __init__(self):
        # handles URL redirection; key=redirect_title, val=canonical_title
        self.redirect_map = {};
        # key=article_title, val=outlink_titles
        self.links = {};
        # key=article_title, val=abstract_text
        self.abstracts = {};

    # helper method to convert a URI to it's subject matter
    # EX: <http://dbpedia.org/resource/John_Lennon> would return the subject: "John_Lennon"
    def _strip_uri(self, uri_string):
        PREFIX = "http://dbpedia.org/resource/"
        return uri_string.removeprefix(PREFIX).replace("_", " ")

    # helper method to decode the raw text from RDF format
    def _strip_literal(self, literal_string):
        literal_regex = re.compile(r'^"(.*)"@\w+$', re.DOTALL)
        m = literal_regex.match(literal_string)
        return m.group(1) if m else literal_string

    # helper method to resolve redirects. it checks if title exists in redirects, and if it does it will return the canonical title
    def _resolve(self, title):
        return self.redirect_map.get(title, title)

    def _iter_triples(self, filepath):
        triple_re = re.compile(r'^<([^>]+)>\s+<([^>]+)>\s+(.+?)\s*\.\s*$')

        with bz2.open(filepath, "rt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("@") or line.startswith("#"):
                    continue
                m = triple_re.match(line)
                if m:
                    yield m.group(1), m.group(2), m.group(3)

    # parse the redirect file and build out the redirect_map
    def parse_redirects(self, filepath):
        PREDICATE = "http://dbpedia.org/ontology/wikiPageRedirects"
        raw = {}

        # For each entry
        for s, p, o in self._iter_triples(filepath):
            # If its a redirect entry
            if p == PREDICATE and o.startswith("<") and o.endswith(">"):
                src = self._strip_uri(s)
                dst = self._strip_uri(o[1:-1])
                raw[src] = dst

        # Resolve redir chains. ex: A -> B -> C becomes A -> C
        def resolve_chain(title, recorded=None):
            recorded = recorded or set()
            if title in recorded:
                return title  # cycle guard
            recorded.add(title)
            target = raw.get(title)
            return resolve_chain(target, recorded) if target else title

        self.redirect_map = {src: resolve_chain(src) for src in raw}
        print(f"Redirects loaded: {len(self.redirect_map):,}")

    # parse the wikilinks file, strip the links to titles (resolve redirects via parse_redirects) and build out the links map
    def parse_links(self, filepath):
        PREDICATE = "http://dbpedia.org/ontology/wikiPageWikiLink"
        SKIP_PREFIXES = ("Category:", "File:", "Template:", "Wikipedia:") # Not-articles which can be ignored.
        links = defaultdict(list)

        for s, p, o in self._iter_triples(filepath):
            if p == PREDICATE and o.startswith("<") and o.endswith(">"):
                src = self._resolve(self._strip_uri(s))
                dst = self._resolve(self._strip_uri(o[1:-1]))
                if any(dst.startswith(p) for p in SKIP_PREFIXES):
                    continue
                links[src].append(dst)

        self.links = dict(links)
        print(f"Links loaded: {len(self.links):,} articles")

    def parse_abstracts(self, filepath):
        PREDICATE = "http://www.w3.org/2000/01/rdf-schema#comment"

        for s, p, o in self._iter_triples(filepath):
            if p == PREDICATE and o.endswith("@en"):
                title = self._resolve(self._strip_uri(s))
                self.abstracts[title] = self._strip_literal(o)

        print(f"Abstracts loaded: {len(self.abstracts):,}")


