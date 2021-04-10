from itertools import chain
from typing import Iterator
from typing import Mapping

from loguru import logger
from more_itertools import pairwise


HKD_PER_USD = 7.8
MAX_DEDUCTION_HKD = int(60e3)
TAX_RATE = 0.17
DEDUCTION_YEARS = 5


def analyse(
    costs: Mapping[int, float],
    deductions: Mapping[int, float],
    redemptions: Mapping[int, float],
) -> Iterator[tuple[int, float]]:
    """Given:
    - a set of costs (to be paid at the start of each year),
    - a set of deductions (available at the start of each year), and
    - a set of possible redemption values (available at the end of each year),
    yield for all relevant years the annualized return.
    """

    year, invested = 1, 0.0


CUM_COSTS_USD = [7702, 15403, 23105, 30806, 38508]
COSTS_HKD = {
    year: HKD_PER_USD * (next_ - prev)
    for year, (prev, next_) in enumerate(
        pairwise(chain([0.0], CUM_COSTS_USD)), start=1
    )
}
DEDUCTIONS_HKD = {
    year: MAX_DEDUCTION_HKD * TAX_RATE for year in range(1, DEDUCTION_YEARS + 1)
}
REDEMPTIONS_USD = [
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
REDEMPTIONS_HKD = {
    year: HKD_PER_USD * red for year, red in enumerate(REDEMPTIONS_USD, start=1)
}


if __name__ == "__main__":
    for year, ann_ret in analyse(COSTS_HKD, DEDUCTIONS_HKD, REDEMPTIONS_HKD):
        logger.info(year, ann_ret)
