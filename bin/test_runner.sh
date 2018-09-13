#!/usr/bin/env bash
this_program="$0"
dirname="`dirname $this_program`"
python3 -m unittest test.test_wiki_scraper.Test_WikiScraper 2> results.xunit