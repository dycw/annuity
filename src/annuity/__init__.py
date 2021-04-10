from dataclasses import dataclass
from itertools import chain
from sys import stdout
from typing import Iterator
from typing import Mapping

from loguru import logger
from more_itertools import pairwise


logger.remove()
logger.add(stdout, format="{message}")


@dataclass
class Status:
    year: int
    invested: float
    redemption: float
    ann_ret: float


def analyse(
    costs: Mapping[int, float],
    deductions: Mapping[int, float],
    redemptions: Mapping[int, float],
) -> Iterator[Status]:
    """Given:
    - a set of costs (to be paid at the start of each year),
    - a set of deductions (available at the start of each year), and
    - a set of possible redemption values (available at the end of each year),
    yield for all relevant years the annualized return.
    """

    year, invested = 1, 0.0
    while year <= max(chain(costs, deductions, redemptions)):
        # start of year
        invested += costs.get(year, 0.0)
        invested -= deductions.get(year, 0.0)

        # end of year
        redemption_i = redemptions[year]
        ann_ret_i = (redemption_i / invested) ** (1 / year) - 1.0

        # yield & increment
        yield Status(
            year=year,
            invested=invested,
            redemption=redemption_i,
            ann_ret=ann_ret_i,
        )
        year += 1


def main() -> None:
    # costs
    cum_costs_usd = [7702, 15403, 23105, 30806, 38508]
    hkd_per_usd = 7.8
    costs_hkd = {
        year: hkd_per_usd * (next_ - prev)
        for year, (prev, next_) in enumerate(
            pairwise(chain([0.0], cum_costs_usd)), start=1
        )
    }

    # deductions
    max_deduction_hkd = int(60e3)
    tax_rate = 0.17
    years_deductions = 5
    deductions_hkd = {
        year: max_deduction_hkd * tax_rate
        for year in range(1, years_deductions + 1)
    }

    # redemptions
    redemptions_usd = [
        # 1-10
        1540,
        3851,
        6702,
        9287,
        12436,
        16150,
        22590,
        37919,
        39805,
        42885,
        # 11-20
        44945,
        47118,
        49411,
        51829,
        54383,
        56676,
        59092,
        61640,
        64327,
        67163,
        # 21-30
        69830,
        72648,
        75628,
        78781,
        82119,
        85729,
        89557,
        93619,
        97930,
        102512,
        # 31
        107152,
    ]
    redemptions_hkd = {
        year: hkd_per_usd * red
        for year, red in enumerate(redemptions_usd, start=1)
    }
    for status in analyse(costs_hkd, deductions_hkd, redemptions_hkd):
        logger.info(
            "  ".join(
                [
                    f"year: {status.year:02d}",
                    f"invested: {status.invested:7,.0f}",
                    f"redemption: {status.redemption:7,.0f}",
                    f"ann ret: {status.ann_ret:7.2%}",
                ]
            )
        )


if __name__ == "__main__":
    main()
