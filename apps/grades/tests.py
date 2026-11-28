from decimal import Decimal
from unittest.mock import Mock

from django.test import SimpleTestCase

from .services import (
    STATUS_INSUFFICIENT_DATA,
    STATUS_OK,
    average_for_enrollment_period,
    calculate_average,
)


class AverageRuleTests(SimpleTestCase):
    def test_average_uses_equal_weights_and_rounds_half_up(self):
        result = calculate_average([Decimal("4.00"), Decimal("3.00"), Decimal("2.00")])

        self.assertEqual(result.average, Decimal("3.00"))
        self.assertEqual(result.count, 3)
        self.assertEqual(result.status, STATUS_OK)

    def test_average_rounds_half_up_to_two_decimals(self):
        result = calculate_average([Decimal("1.00"), Decimal("1.01"), Decimal("1.02")])

        self.assertEqual(result.average, Decimal("1.01"))

    def test_no_valid_grades_returns_defined_status(self):
        result = calculate_average([])

        self.assertIsNone(result.average)
        self.assertEqual(result.count, 0)
        self.assertEqual(result.status, STATUS_INSUFFICIENT_DATA)

    def test_minimum_count_is_enforced(self):
        result = calculate_average([Decimal("4.50")], minimum_count=2)

        self.assertIsNone(result.average)
        self.assertEqual(result.status, STATUS_INSUFFICIENT_DATA)

    def test_selected_period_queries_only_valid_grades(self):
        enrollment = Mock(period_id=7)
        period = Mock(pk=7)
        enrollment.grades.filter.return_value.values_list.return_value = [
            Decimal("4.00"), Decimal("3.00")
        ]

        result = average_for_enrollment_period(enrollment, period)

        enrollment.grades.filter.assert_called_once_with(is_valid=True)
        self.assertEqual(result.average, Decimal("3.50"))

    def test_different_selected_period_returns_insufficient_data(self):
        enrollment = Mock(period_id=7)
        period = Mock(pk=8)

        result = average_for_enrollment_period(enrollment, period)

        enrollment.grades.filter.assert_not_called()
        self.assertEqual(result.status, STATUS_INSUFFICIENT_DATA)

