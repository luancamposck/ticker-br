"""Read BTG target prices without saving anything to a database."""

import json

from django.core.management.base import BaseCommand, CommandError

from market_data.sources.btg import BTGScraper, BTGSourceError, normalize_ticker


class Command(BaseCommand):
    help = "Read BTG Pactual target prices for one or more tickers; writes no database rows."

    def add_arguments(self, parser):
        parser.add_argument("tickers", nargs="+", help="Ticker(s), e.g. PETR4 or PETR4.SA")

    def handle(self, *args, **options):
        results = []
        try:
            with BTGScraper() as scraper:
                for raw_ticker in options["tickers"]:
                    try:
                        target = scraper.fetch_target(raw_ticker)
                        results.append(
                            {
                                "input": raw_ticker,
                                "normalized_ticker": normalize_ticker(raw_ticker),
                                "status": "found",
                                "result": target.as_dict(),
                            }
                        )
                    except (ValueError, BTGSourceError) as exc:
                        results.append(
                            {
                                "input": raw_ticker,
                                "status": "not_found_or_unparseable",
                                "error": str(exc),
                            }
                        )
        except Exception as exc:
            raise CommandError(f"Falha ao consultar o BTG: {exc}") from exc

        self.stdout.write(json.dumps(results, ensure_ascii=False, indent=2))
