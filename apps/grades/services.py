from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

from apps.academics.models import AcademicPeriod, GroupEnrollment


AVERAGE_SCALE = Decimal("0.01")
STATUS_OK = "OK"
STATUS_INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


@dataclass(frozen=True)
class AverageResult:
    """Result of the institutional average rule.

    The current rule gives every valid assessment the same weight, excludes
    invalid assessments, and rounds the arithmetic mean to two decimals using
    ROUND_HALF_UP. No valid assessment produces INSUFFICIENT_DATA and None.
    """

    average: Decimal | None
    count: int
    status: str


def calculate_average(values: Iterable[Decimal], minimum_count: int = 1) -> AverageResult:
    """Calculate the equal-weight average for already-filtered valid grades."""
    values = list(values)
    if len(values) < minimum_count:
        return AverageResult(None, len(values), STATUS_INSUFFICIENT_DATA)

    total = sum(values, Decimal("0"))
    average = (total / Decimal(len(values))).quantize(AVERAGE_SCALE, rounding=ROUND_HALF_UP)
    return AverageResult(average, len(values), STATUS_OK)


def average_for_enrollment_period(
    enrollment: GroupEnrollment, period: AcademicPeriod
) -> AverageResult:
    """Return the average using only valid grades from the selected period."""
    if enrollment.period_id != period.pk:
        return AverageResult(None, 0, STATUS_INSUFFICIENT_DATA)

    values = enrollment.grades.filter(is_valid=True).values_list("value", flat=True)
    return calculate_average(values)

