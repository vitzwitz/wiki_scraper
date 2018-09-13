# -*- coding: utf-8 -*-
"""test cases for Wikipedia link scraping."""

import unittest
from logging import info, getLogger, INFO

from main.app.core.wiki_scraper import wiki_scraper


class Test_WikiScraper(unittest.TestCase):
    """
    These end-to-end tests are only for the wiki_scraper function in the wiki_scraper module.
    Feel free to add your own test cases as you run into edge cases.
    """

    def setUp(self):
        getLogger().setLevel(level=INFO)


    def test_science(self):
        """
        The wiki scraper should return all the Wikipedia article links
        from the first paragraph of a given Wikipedia page.
        """
        expected_links = [
            "https://en.wikipedia.org/wiki/Latin_language",
            "https://en.wikipedia.org/wiki/Knowledge",
            "https://en.wikipedia.org/wiki/Explanation",
            "https://en.wikipedia.org/wiki/Predictions",
            "https://en.wikipedia.org/wiki/Universe"
        ]
        actual_links = wiki_scraper('Science')
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Science'\n")

    def test_orange(self):
        """
        The wiki scraper should follow the first link on a disambiguation page.
        """
        expected_links = ['https://en.wikipedia.org/wiki/Color',
                          'https://en.wikipedia.org/wiki/Yellow',
                          'https://en.wikipedia.org/wiki/Red',
                          'https://en.wikipedia.org/wiki/Optical_spectrum',
                          'https://en.wikipedia.org/wiki/Visible_light',
                          'https://en.wikipedia.org/wiki/Human_eyes',
                          'https://en.wikipedia.org/wiki/Dominant_wavelength',
                          'https://en.wikipedia.org/wiki/Nanometre',
                          'https://en.wikipedia.org/wiki/Color_theory',
                          'https://en.wikipedia.org/wiki/Orange_(fruit)']

        actual_links = wiki_scraper('Orange')

        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Orange'\n")

    def test_curacao(self):
        """
        The wiki scraper should be able to handle unicode input.
        The wiki scraper should dodge internal help article links and scrape only content links.
        The wiki scraper should only return a unique list of links.
        """
        expected_links = ['https://en.wikipedia.org/wiki/Dutch_language',
                          'https://en.wikipedia.org/wiki/Papiamento_language',
                          'https://en.wikipedia.org/wiki/Lesser_Antilles',
                          'https://en.wikipedia.org/wiki/Island',
                          'https://en.wikipedia.org/wiki/Caribbean_Sea',
                          'https://en.wikipedia.org/wiki/Dutch_Caribbean',
                          'https://en.wikipedia.org/wiki/Venezuela',
                          'https://en.wikipedia.org/wiki/Kingdom_of_the_Netherlands']

        actual_links =wiki_scraper(u'Curaçao')

        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped u'Curaçao'\n")

    def test_alice_coltrane(self):
        """
        Input should not be case sensitive.
        """
        expected_links = [
            "https://en.wikipedia.org/wiki/Sanskrit",
            "https://en.wikipedia.org/wiki/Jazz",
            "https://en.wikipedia.org/wiki/Swami",
            "https://en.wikipedia.org/wiki/Impulse!_Records",
            "https://en.wikipedia.org/wiki/John_Coltrane"]

        actual_links =wiki_scraper('alice coltrane')

        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'alice coltrane'\n")

    def test_wiki(self):
        """
        Input can be the same as general path
        """
        expected_links = ["https://en.wikipedia.org/wiki/Website",
                          "https://en.wikipedia.org/wiki/Collaborative_software",
                          "https://en.wikipedia.org/wiki/Web_browser",
                          "https://en.wikipedia.org/wiki/Markup_language",
                          "https://en.wikipedia.org/wiki/Online_rich-text_editor"]

        actual_links =wiki_scraper('wiki')

        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'wiki'\n")

    def test_secondary_color(self):
        """
        Input is not case sensitive and specific path does not need each word to be capitalized
        """
        expected_links = ["https://en.wikipedia.org/wiki/Color",
                          "https://en.wikipedia.org/wiki/Color_mixing",
                          "https://en.wikipedia.org/wiki/Primary_color",
                          "https://en.wikipedia.org/wiki/Color_space"]

        actual_links =wiki_scraper("Secondary_Color")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Secondary_Color'\n")

    def test_Byte(self):
        """
        Input can be bytes and scraper converts bytes to string before it scrapes wikipedia
        """
        expected_links = ["https://en.wikipedia.org/wiki/Units_of_information",
                          "https://en.wikipedia.org/wiki/Bit",
                          "https://en.wikipedia.org/wiki/Binary_number",
                          "https://en.wikipedia.org/wiki/Character_(computing)",
                          "https://en.wikipedia.org/wiki/Address_space",
                          "https://en.wikipedia.org/wiki/Computer_memory",
                          "https://en.wikipedia.org/wiki/Computer_architecture"]

        actual_links =wiki_scraper(bytes("Byte", encoding="utf-8"))
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Byte' as bytes\n")

    def test_fake_this(self):
        """
        Input cannot be an invalid article name
        """
        with self.assertRaises(expected_exception=AssertionError):
            wiki_scraper("fakethis")
        info("Wiki Scraper 'successfully' failed to scrape 'fakethis'\n")

    def test_Main_Page(self):
        """
        Input must direct to an article page, project, or help page
        """
        with self.assertRaises(expected_exception=AssertionError):
            wiki_scraper("Main_Page")
        info("Wiki Scraper 'successfully' failed to scrape 'Main_Page'\n")


    def test_main(self):
        """
        Wiki Scraper will redirect until it finds a disambiguous page
        """
        expected_links = ['https://en.wikipedia.org/wiki/River',
                          'https://en.wikipedia.org/wiki/Germany',
                          'https://en.wikipedia.org/wiki/White_Main',
                          'https://en.wikipedia.org/wiki/Rhine',
                          'https://en.wikipedia.org/wiki/Weser',
                          'https://en.wikipedia.org/wiki/Werra',
                          'https://en.wikipedia.org/wiki/Frankfurt_am_Main',
                          'https://en.wikipedia.org/wiki/W%C3%BCrzburg']

        actual_links =wiki_scraper("main")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'main'\n")

    def test_Apple_Inc(self):
        """
        Input can contain special characters (i.e '.')
        """
        expected_links = ['https://en.wikipedia.org/wiki/Multinational_corporation',
                          'https://en.wikipedia.org/wiki/Technology_company',
                          'https://en.wikipedia.org/wiki/Cupertino,_California',
                          'https://en.wikipedia.org/wiki/Consumer_electronics',
                          'https://en.wikipedia.org/wiki/Software',
                          'https://en.wikipedia.org/wiki/Computer_hardware',
                          'https://en.wikipedia.org/wiki/IPhone',
                          'https://en.wikipedia.org/wiki/IPad',
                          'https://en.wikipedia.org/wiki/Macintosh',
                          'https://en.wikipedia.org/wiki/IPod',
                          'https://en.wikipedia.org/wiki/Apple_Watch',
                          'https://en.wikipedia.org/wiki/Apple_TV',
                          'https://en.wikipedia.org/wiki/HomePod',
                          'https://en.wikipedia.org/wiki/MacOS',
                          'https://en.wikipedia.org/wiki/IOS',
                          'https://en.wikipedia.org/wiki/ITunes',
                          'https://en.wikipedia.org/wiki/Safari_(web_browser)',
                          'https://en.wikipedia.org/wiki/ILife',
                          'https://en.wikipedia.org/wiki/IWork',
                          'https://en.wikipedia.org/wiki/Final_Cut_Pro',
                          'https://en.wikipedia.org/wiki/Logic_Pro',
                          'https://en.wikipedia.org/wiki/Xcode',
                          'https://en.wikipedia.org/wiki/ITunes_Store',
                          'https://en.wikipedia.org/wiki/App_Store_(iOS)',
                          'https://en.wikipedia.org/wiki/Mac_App_Store',
                          'https://en.wikipedia.org/wiki/Apple_Music',
                          'https://en.wikipedia.org/wiki/ICloud']
        actual_links =wiki_scraper("Apple_Inc.")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Apple_Inc'\n")

    def test_IPod(self):
        """
        Wiki core will return content links from the actual first paragraph (in terms of English syntax/language)
        """
        expect_links = ['https://en.wikipedia.org/wiki/Portable_media_player',
                        'https://en.wikipedia.org/wiki/Pocket_computer',
                        'https://en.wikipedia.org/wiki/Apple_Inc.',
                        'https://en.wikipedia.org/wiki/IPod_Classic#1st_generation',
                        'https://en.wikipedia.org/wiki/ITunes',
                        'https://en.wikipedia.org/wiki/IPod_Touch']
        actual_links =wiki_scraper("IPod")
        self.assertEqual(expect_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'IPod'\n")

    def test_Ipad(self):
        """
        Input is *fully* case insensitive - any letter can be any case
        """
        expected_links = ['https://en.wikipedia.org/wiki/Tablet_computer',
                          'https://en.wikipedia.org/wiki/Apple_Inc.',
                          'https://en.wikipedia.org/wiki/IOS',
                          'https://en.wikipedia.org/wiki/IPad_(2018)',
                          'https://en.wikipedia.org/wiki/IPad_Pro',
                          'https://en.wikipedia.org/wiki/User_interface',
                          'https://en.wikipedia.org/wiki/Multi-touch',
                          'https://en.wikipedia.org/wiki/Virtual_keyboard',
                          'https://en.wikipedia.org/wiki/Wi-Fi',
                          'https://en.wikipedia.org/wiki/Cellular_network']
        actual_links =wiki_scraper("Ipad")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Ipad'\n")

    def test_fake_article(self):
        """
        Input can refer to a page that redirects to another page
        The wiki scraper only collect Wikipedia pages
        Wiki Scraper can still detect the first paragraph even if the full title does not exist in bold
        """
        expected_links = ['https://en.wikipedia.org/wiki/Reference_work',
                          'https://en.wikipedia.org/wiki/Dictionary',
                          'https://en.wikipedia.org/wiki/Encyclopedia',
                          'https://en.wikipedia.org/wiki/Trap_street',
                          'https://en.wikipedia.org/wiki/Phantom_settlement',
                          'https://en.wikipedia.org/wiki/Phantom_island',
                          'https://en.wikipedia.org/wiki/Ghost_word']

        actual_links =wiki_scraper("fake_article")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'fake_article'\n")

    def test_Joker(self):
        """
        The Wiki Scraper looks for all words outside of parentheses in bold and all words in parentheses as a link
         (except disambiguation) to determine which paragraph to scrape
        """
        expected_links = ['https://en.wikipedia.org/wiki/Playing_card',
                          'https://en.wikipedia.org/wiki/Suit_(cards)',
                          'https://en.wikipedia.org/wiki/United_States',
                          'https://en.wikipedia.org/wiki/American_Civil_War',
                          'https://en.wikipedia.org/wiki/Trump_(card_games)',
                          'https://en.wikipedia.org/wiki/Euchre',
                          'https://en.wikipedia.org/wiki/Card_game',
                          'https://en.wikipedia.org/wiki/Wild_card_(card_games)',
                          'https://en.wikipedia.org/wiki/French_pack']

        actual_links =wiki_scraper("Joker")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Joker'\n")

    def test_Mercury(self):
        """
        Another test to verify an ambiguous page will redirect to first option
                - to ensure scraper handles html format differences
        """
        expected_links = ['https://en.wikipedia.org/wiki/Chemical_element',
                          'https://en.wikipedia.org/wiki/Atomic_number',
                          'https://en.wikipedia.org/wiki/Heavy_metal_(chemistry)',
                          'https://en.wikipedia.org/wiki/D-block',
                          'https://en.wikipedia.org/wiki/Standard_conditions_for_temperature_and_pressure',
                          'https://en.wikipedia.org/wiki/Bromine',
                          'https://en.wikipedia.org/wiki/Caesium',
                          'https://en.wikipedia.org/wiki/Gallium',
                          'https://en.wikipedia.org/wiki/Rubidium',
                          'https://en.wikipedia.org/wiki/Room_temperature']
        actual_links =wiki_scraper("Mercury")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Mercury'\n")

    def test_WikipediaArticle_titles(self):
        """
        Input can should only refer to articles and no page that just discusses a rule, help, etc for Wikipedia
        """
        with self.assertRaises(AssertionError):
            wiki_scraper("Wikipedia:Article_titles")
        info("Wiki Scraper 'successfully' failed to scrape 'Wikipedia:Article_titles'\n")

    def test_Ball_association_football(self):
        """
        Input can contain '(' and not automatically be assumed as a disambiguation page
        """
        expected_links = ['https://en.wikipedia.org/wiki/Association_football',
                          'https://en.wikipedia.org/wiki/Names_for_association_football',
                          'https://en.wikipedia.org/wiki/Laws_of_the_Game_(association_football)',
                          'https://en.wikipedia.org/wiki/International_Football_Association_Board',
                          'https://en.wikipedia.org/wiki/FIFA']
        actual_links =wiki_scraper("Ball_(association_football)")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Ball_(association_football)'\n")

    def test_Football_disambiguation(self):
        """
        Input can contain '(' and specifically '(disambiguation)' and will use it as a shortcut to find link to redirect
         to and will not be assumed as a disambiguation page
        """
        expected_links = ["https://en.wikipedia.org/wiki/Team_sport",
                          "https://en.wikipedia.org/wiki/Kick_(football)",
                          "https://en.wikipedia.org/wiki/Football_(ball)",
                          "https://en.wikipedia.org/wiki/Goal_(sport)",
                          "https://en.wikipedia.org/wiki/Football_(word)",
                          "https://en.wikipedia.org/wiki/Association_football",
                          "https://en.wikipedia.org/wiki/Gridiron_football",
                          "https://en.wikipedia.org/wiki/American_football",
                          "https://en.wikipedia.org/wiki/Canadian_football",
                          "https://en.wikipedia.org/wiki/Australian_rules_football",
                          "https://en.wikipedia.org/wiki/Rugby_football",
                          "https://en.wikipedia.org/wiki/Rugby_league",
                          "https://en.wikipedia.org/wiki/Rugby_union",
                          "https://en.wikipedia.org/wiki/Gaelic_football"]
        actual_links =wiki_scraper("Football_(disambiguation)")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Football_(disambiguation)'\n")

    def Online_richtext_editor(self):
        """
        Input can contain hyphens
        """
        expected_links = ['https://en.wikipedia.org/wiki/Formatted_text',
                          'https://en.wikipedia.org/wiki/Web_browser',
                          'https://en.wikipedia.org/wiki/WYSIWYG',
                          'https://en.wikipedia.org/wiki/HTML_element']
        actual_links =wiki_scraper("Online_rich-text_editor")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Online_rich-text_editor'\n")

    def test_National_Trust_for_Places_of_Historic_Interest_or_Natural_Beauty(self):
        """
        Input is case insensitive for each word inside it
        Input can be a disambiguation page and it does not need any parentheses to determine where the first paragraph
         is
        """
        expected_links = ['https://en.wikipedia.org/wiki/Building_Preservation_and_Conservation_Trusts_in_the_UK',
                          'https://en.wikipedia.org/wiki/England',
                          'https://en.wikipedia.org/wiki/Wales',
                          'https://en.wikipedia.org/wiki/Northern_Ireland']

        actual_links =wiki_scraper("National_Trust_for_Places_of_Historic_Interest_or_Natural_Beauty")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'National_Trust_for_places_of_historic_Interest_Or_Natural_Beauty'\n")

    def test_Cupertino_California(self):
        """
         Input can contain ',' commas
         Wiki scraper will only search for first word before comma in bold and the rest through the entire paragraph
        """
        expected_links = ['https://en.wikipedia.org/wiki/Santa_Clara_County,_California',
                          'https://en.wikipedia.org/wiki/San_Jose,_California',
                          'https://en.wikipedia.org/wiki/Santa_Clara_Valley',
                          'https://en.wikipedia.org/wiki/Santa_Cruz_Mountains',
                          'https://en.wikipedia.org/wiki/Apple_Inc.']

        actual_links =wiki_scraper("Cupertino,_California")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'Cupertino,_California'\n")

    def test_c3_organization(self):
        """
        Input can contain numbers
        Input can contain '(' and ')' that does not apply as its definition or topic
        Input can contain '_' and ' ' simultaneously
        """
        expected_links = ['https://en.wikipedia.org/wiki/Internal_Revenue_Code',
                          'https://en.wikipedia.org/wiki/United_States_Code',
                          'https://en.wikipedia.org/wiki/501(c)_organization',
                          'https://en.wikipedia.org/wiki/Nonprofit_organizations']
        actual_links =wiki_scraper("501(c)(3)_organization")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped '501(c)(3)_organization'\n")

    def test_1(self):
        """
        Input can be single number
        """
        expected_links = ["https://en.wikipedia.org/wiki/Number",
                          "https://en.wikipedia.org/wiki/Numeral_(linguistics)",
                          "https://en.wikipedia.org/wiki/Glyph",
                          "https://en.wikipedia.org/wiki/Unit_(measurement)",
                          "https://en.wikipedia.org/wiki/Counting",
                          "https://en.wikipedia.org/wiki/Measurement",
                          "https://en.wikipedia.org/wiki/Line_segment",
                          "https://en.wikipedia.org/wiki/Length",
                          "https://en.wikipedia.org/wiki/Sequence_(mathematics)",
                          "https://en.wikipedia.org/wiki/Natural_number",
                          "https://en.wikipedia.org/wiki/2"]
        actual_links =wiki_scraper("1")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped '1'\n")

    def test_r(self):
        """
        Input can be single number
        """
        expected_links = ["https://en.wikipedia.org/wiki/English_alphabet#Letter_names",
                          "https://en.wikipedia.org/wiki/Letter_(alphabet)",
                          "https://en.wikipedia.org/wiki/English_alphabet",
                          "https://en.wikipedia.org/wiki/ISO_basic_Latin_alphabet"]
        actual_links =wiki_scraper("r")
        self.assertEqual(first=expected_links, second=actual_links)
        info("Wiki Scraper successfully scraped 'r'\n")
