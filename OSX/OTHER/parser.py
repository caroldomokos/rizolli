#!/usr/bin/python
import scraperwiki
wikipedia_utils = scraperwiki.swimport("wikipedia_utils")

title = "OS X"

val = wikipedia_utils.GetWikipediaPage(title)
res = wikipedia_utils.ParseTemplates(val["text"])
print res               # prints everything we have found in the text
infobox_osx = dict(res["templates"]).get("Infobox osx")
print infobox_osx    # prints just the ukcave infobox
