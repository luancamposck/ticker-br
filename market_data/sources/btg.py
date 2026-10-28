"""Read public BTG Pactual equity research data for a B3 ticker."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal

import httpx
from bs4 import BeautifulSoup


BASE_URL = "https://content.btgpactual.com/research/ativo"
USER_AGENT = "TickerBR/0.1 (public research collector)"
TICKER_PATTERN = re.compile(r"^[A-Z]{4}\d{1,2}[A-Z]?$")
MONEY_PATTERN = re.compile(r"R\$\s*([\d.]+,\d{2})")
DATE_PATTERN = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")


class BTGSourceError(RuntimeError):
    """The BTG page did not contain the expected public research fields."""


def normalize_ticker(value: str) -> str:
    ticker = value.strip().upper()
    if ticker.endswith(".SA"):
        ticker = ticker[:-3]
    if not TICKER_PATTERN.fullmatch(ticker):
        raise ValueError(f"Ticker inválido ou formato não suportado: {value!r}")
    return ticker


def _money(text: str) -> Decimal:
    match = MONEY_PATTERN.search(text)
    if not match:
        raise BTGSourceError(f"Não encontrei um valor monetário reconhecível: {text!r}")
    return Decimal(match.group(1).replace(".", "").replace(",", "."))


def _parse_date(text: str) -> date | None:
    match = DATE_PATTERN.search(text)
    if not match:
        return None
    day, month, year = (int(part) for part in match.group(1).split("/"))
    return date(year, month, day)


@dataclass(frozen=True)
class BTGTarget:
    ticker: str
    value: Decimal
    currency: str
    recommendation: str | None
    analysis_date: str | None
    page_data_date: str | None
    source_url: str

    def as_dict(self) -> dict[str, str | None]:
        result = asdict(self)
        result["value"] = format(self.value, ".2f")
        return result


class BTGScraper:
    """Fetch the target-price card from BTG's public asset page."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(
            headers={"User-Agent": USER_AGENT}, timeout=30.0, follow_redirects=True
        )
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self.client.close()

    def __enter__(self) -> BTGScraper:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def fetch_target(self, raw_ticker: str) -> BTGTarget:
        ticker = normalize_ticker(raw_ticker)
        source_url = f"{BASE_URL}/{ticker}/"
        response = self.client.get(source_url)
        if response.status_code == 404:
            raise BTGSourceError(f"O BTG não encontrou a página de {ticker}.")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        if not re.search(rf"(?<![A-Z0-9]){re.escape(ticker)}(?![A-Z0-9])", title, re.I):
            raise BTGSourceError(f"A página retornada não corresponde ao ticker {ticker}.")

        target_box = soup.select_one(".target-price")
        target_value = target_box.select_one(".target-price-present") if target_box else None
        if target_value is None:
            raise BTGSourceError(f"A página de {ticker} não exibe o campo Preço-alvo.")
        value = _money(target_value.get_text(" ", strip=True))

        analysis_date: date | None = None
        recommendation: str | None = None
        for card in soup.select(".wrv-analysis-card"):
            target = card.select_one(".wrv-analysis-card__target-value")
            if target is None:
                continue
            target_date = _parse_date(card.get_text(" ", strip=True))
            if target_date is None:
                continue
            card_value = _money(target.get_text(" ", strip=True))
            if card_value == value and (analysis_date is None or target_date > analysis_date):
                analysis_date = target_date
                rec = card.select_one(".wrv-analysis-card__recommendation")
                rec_classes = rec.get("class", []) if rec else []
                recommendation = next(
                    (
                        label
                        for class_name, label in (
                            ("recommendation--buy", "Compra"),
                            ("recommendation--neutral", "Neutro"),
                            ("recommendation--sell", "Venda"),
                        )
                        if class_name in rec_classes
                    ),
                    None,
                )

        page_data_date = None
        page_text = soup.get_text(" ", strip=True)
        consolidated = re.search(r"Dados consolidados em:\s*(\d{2}/\d{2}/\d{4})", page_text)
        if consolidated:
            page_data_date = consolidated.group(1)

        return BTGTarget(
            ticker=ticker,
            value=value,
            currency="BRL",
            recommendation=recommendation,
            analysis_date=analysis_date.isoformat() if analysis_date else None,
            page_data_date=page_data_date,
            source_url=str(response.url),
        )
