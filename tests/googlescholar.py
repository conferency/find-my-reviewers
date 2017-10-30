import unittest
from app.modules.scrapers.googlescholar import parser


class GoogleScholarTests(unittest.TestCase):

    def verify_papers(self, expected, actual):
        actual_dict = {x['title']: x for x in actual}
        for pe in expected:
            self.assertTrue(pe.pop('citations') > 0)
            self.assertTrue(pe.pop('data_url').startswith('/citations'))
            self.assertDictContainsSubset(pe, actual_dict[pe['title']])

    def test_google_scholar_parser(self):
        actual = parser.crawl('https://scholar.google.com.hk/citations?hl=en&user=5qvdHjQAAAAJ')

        expected = {'overall_citations_list': [7569, 1799, 32, 14, 195, 37],
                    'citations_by_year': {1984: 48, 1985: 34, 1986: 82, 1987: 62, 1988: 52, 1989: 62, 1990: 52,
                                          1991: 55, 1992: 95, 1993: 57, 1994: 78, 1995: 59, 1996: 82, 1997: 63,
                                          1998: 92, 1999: 84, 2000: 88, 2001: 72, 2002: 114, 2003: 145, 2004: 219,
                                          2005: 175, 2006: 278, 2007: 335, 2008: 392, 2009: 183, 2010: 283, 2011: 257,
                                          2012: 321, 2013: 324, 2014: 362, 2015: 270, 2016: 280, 1978: 85,
                                          1979: 39, 1980: 35, 1981: 47, 1982: 36, 1983: 60},
                    'full_name': 'Theodore Dru Alison Cockerell (1866–1948)', 'labels': {
                'particular bees and scale insects': '/citations?view_op=search_authors&hl=en&mauthors=label:particular_bees_and_scale_insects',
                'Natural history': '/citations?view_op=search_authors&hl=en&mauthors=label:natural_history'},
                    'email_suffix': 'melipona.org', 'papers': [{
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:M0j1y4EgrScC',
                                                                   'citations': 224,
                                                                   'title': 'LIII.—Descriptions and records of bees.—XIX',
                                                                   'year': 1908}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:QxtoOqDH1aQC',
                                                                   'citations': 213,
                                                                   'title': 'Descriptions and records of bees, no. 74',
                                                                   'year': 1917}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:xIusEVNJREcC',
                                                                   'citations': 207,
                                                                   'title': 'LIII.—Descriptions and records of bees.—XIX',
                                                                   'year': 1908}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:BulkYocH2doC',
                                                                   'citations': 167,
                                                                   'title': 'Descriptions and records of bees. VI',
                                                                   'year': 1905}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:Ri6SYOTghG4C',
                                                                   'citations': 150,
                                                                   'title': 'LXXX.—Descriptions and records of bees.—XCIV',
                                                                   'year': 1922}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:bEWYMUwI8FkC',
                                                                   'citations': 121,
                                                                   'title': 'LXXVIII.—Descriptions and records of bees.—C',
                                                                   'year': 1924}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:UebtZRa9Y70C',
                                                                   'citations': 96,
                                                                   'title': 'Bees in the collection of the United States national museum. 1-4',
                                                                   'year': 1911}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:DrR-2ekChdkC',
                                                                   'citations': 88,
                                                                   'title': 'XVII.—Descriptions and records of bees.—LXXIX',
                                                                   'year': 1918}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:u-x6o8ySG0sC',
                                                                   'citations': 87,
                                                                   'title': 'Arthropods in Burmese amber',
                                                                   'year': 1917}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:9yKSN-GCB0IC',
                                                                   'citations': 86, 'title': 'Insects in Burmese amber',
                                                                   'year': 1916}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:-f6ydRqryjwC',
                                                                   'citations': 78,
                                                                   'title': 'XXV.—Fossil Arthropods in the British Museum.—IV',
                                                                   'year': 1920}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:ULOm3_A8WrAC',
                                                                   'citations': 75,
                                                                   'title': 'XLIII.—Descriptions and records of bees.—XXIII',
                                                                   'year': 1909}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:08ZZubdj9fEC',
                                                                   'citations': 69,
                                                                   'title': 'Fossil insects from Florissant, Colorado',
                                                                   'year': 1910}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:d1gkVwhDpl0C',
                                                                   'citations': 69,
                                                                   'title': 'The Coleoptera of New Mexico',
                                                                   'year': 1907}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:uCYQzKCmtZwC',
                                                                   'citations': 57,
                                                                   'title': 'XXVIII.—Descriptions and records of bees.—VIII',
                                                                   'year': 1906}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:vYYylRVofzEC',
                                                                   'citations': 54,
                                                                   'title': 'Monograph of the Bombycine moths of North America.',
                                                                   'year': 1914}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:2osOgNQ5qMEC',
                                                                   'citations': 54,
                                                                   'title': 'Observations on fish scales',
                                                                   'year': 1913}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:LkGwnXOMwfcC',
                                                                   'citations': 50,
                                                                   'title': 'Eocene insects from the Rocky Mountains',
                                                                   'year': 1921}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:UeHWp8X0CEIC',
                                                                   'citations': 49,
                                                                   'title': 'Some American Cretaceous fish scales, with notes on the classification and distribution of Cretaceous fishes',
                                                                   'year': 1919}, {
                                                                   'data_url': '/citations?view_op=view_citation&hl=en&user=5qvdHjQAAAAJ&citation_for_view=5qvdHjQAAAAJ:R6aXIXmdpM0C',
                                                                   'citations': 48,
                                                                   'title': 'The insects of the dipterous family Phoridae in the United States National Museum',
                                                                   'year': 1912}],
                    'occupation': 'Professor, University of Colorado'}

        # self.assertEqual(expected, actual)

        self.assertEqual(expected['full_name'], actual['full_name'])
        self.assertEqual(expected['email_suffix'], actual['email_suffix'])
        self.assertEqual(expected['occupation'], actual['occupation'])
        self.assertEqual(expected['labels'], actual['labels'])

        self.assertTrue(actual['overall_citations_list'][0] >= expected['overall_citations_list'][0])
        self.assertTrue(actual['overall_citations_list'][2] >= expected['overall_citations_list'][2])
        self.assertTrue(actual['overall_citations_list'][4] >= expected['overall_citations_list'][4])
        self.assertDictContainsSubset(expected['citations_by_year'], actual['citations_by_year'])
        self.verify_papers(expected['papers'], actual['papers'])

if __name__ == '__main__':
    unittest.main()
