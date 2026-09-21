# MarketPulse — published site

The deployed output of MarketPulse, a daily dashboard that reads the tape and
writes it up: indices, news with impact, a dividend sleeve, a war log, and an
action plan with three weighted scenarios.

**Live:** https://emrekesici.github.io/marketpulse-site/

This repository holds the built site only — `index.html` (self-contained, with
the editions embedded), `editions.json` (the archive, newest first), and
`data.json` (the editions array on its own, for other clients). The generator,
the page template, and the pipeline live in a separate private repository.

## How an edition is made

Numbers are fetched, never generated. Yields come from FRED (`DGS2`, `DGS10`,
`DGS30`, `DFII10`, `T10YIE`, `DFF`) and quotes from Yahoo Finance; the narrative
is written around those values by Claude with web search. The model has no
authority over a price — a missing value renders `n/a`, and the pipeline aborts
rather than let a gap be filled by guesswork.

`scripts/compliance_check.py` runs in CI before every deploy and blocks it on a
missing disclosure or on content that falls outside the publishing standard.

## Disclaimer — not investment advice

**This site is for informational and educational purposes only. It is not
investment advice, financial advice, trading advice, or a recommendation to buy,
sell, or hold any security or other financial instrument.**

- Nothing here — news summaries, signals, scenario probabilities, key levels, or
  the action plan — is a recommendation or a solicitation to transact in any
  security. The model portfolio is a hypothetical illustration, not a real book.
- The author is not a licensed financial adviser, broker, or dealer, and no
  fiduciary or advisory relationship is created by your use of this site. This
  is a personal project published as an outside business activity.
- Trading and investing involve substantial risk, including the total loss of
  principal. Past performance does not indicate future results.
- Content may be incomplete, delayed, stale, or wrong. Market data can be revised
  or misreported, and the AI-written narrative can misread the news even when the
  underlying numbers are correct. Editions are dated; nothing is updated in place
  after publication.
- You are solely responsible for your own investment decisions. Do your own
  research and consult a qualified, licensed financial professional who knows
  your circumstances before acting on anything you read here.
- Provided "as is", without warranty of any kind. The author accepts no liability
  for any loss or damage arising from its use.
