 class DBPediaParser:

    def __init__(self):
        # handles URL redirection; key=redirect_title, val=canonical_title
        self.redirect_map = {};
        # key=article_title, val=outlink_titles
        self.links = {};
        # key=article_title, val=abstract_text
        self.abstracts = {};

    # parse the redirect file and build out the redirect_map
    def parse_redirects(self, filepath):
        print("TODO");

    # parse the wikilinks file, strip the links to titles (resolve redirects via parse_redirects) and build out the links map
    def parse_links(self, filepath):
        print("TODO");

    # parse the abstracts file to populate the abstract map
    def parse_abstracts(self, filepath):
        print("TODO");

    # helper method to convert a URI to it's subject matter
    # EX: <http://dbpedia.org/resource/John_Lennon> would return the subject: "John_Lennon"
    def _strip_uri(self, uri_string):
        print("TODO");
        return "TODO";

    # helper method to decode the raw text from RDF format
    def _strip_literal(self, literal_string):
        print("TODO");
        return "TODO";

    # helper method to resolve redirects. it checks if title exists in redirects, and if it does it will return the canonical title
    def _resolve(self, title):
        print("TODO");
        return "TODO";

