# U.S. drawing tablet sales

A historical sample of advertised U.S. prices and promotions for Wacom, Huion, and XPPen, with observations from April 2022 through November 23, 2026.

| File | Rows | What it contains |
| --- | ---: | --- |
| [campaigns.json](campaigns.json) | 108 | Named campaigns and dated observations, with stated windows where available. One contextual campaign has an unspecified market. |
| [model-offers.json](model-offers.json) | 540 | U.S. offers for specific models or bundles, with sale and reference prices in USD where available. |

Both files are UTF-8 JSON arrays. Each row has a source URL, source type, and evidence notes. Some have an alternate URL. Records preserve the workbook data, including unknowns. The campaign `label` and offer `event` are descriptions, not unique join keys.

Black Friday/Cyber was the broadest window found, but the median advertised discount was about 20% both in and outside that window. Across the 460 comparable pen-tablet and pen-display offers, the middle half was 16.0%–26.3%. Track a target price for the exact model: a sale name is not a guarantee of the lowest price.

Browse the [source index](SOURCES.md) for direct links by year. See [methodology](METHODOLOGY.md) for how sources were found and compared, and [the analysis script](analyze-offers.py) to reproduce the discount statistics.
