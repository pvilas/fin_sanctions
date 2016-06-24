# fin_sanctions

Interface for query the lists of UN, EU and US persons, groups and entities subject to financial sanctions.

The project aims to compliment the EU regulations in the sense of detect similitudes between a given name and the lists.

We use the Levenshtein distance in order to detect matches. We can pass the distance on the *distance* parameter of the query.



## Lists
- [EU](http://eeas.europa.eu/cfsp/sanctions/consol-list/index_en.htm)
- [UN](https://www.un.org/sc/suborg/en/sanctions/un-sc-consolidated-list)
- [US](https://www.treasury.gov/ofac/downloads/consolidated/consolidated.xml)


