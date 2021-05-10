"""
Module contains custom extensions for assertpy lib
"""
from assertpy.assertpy import AssertionBuilder, add_extension, assert_that, soft_assertions


def _has_status(self: AssertionBuilder, status: str) -> AssertionBuilder:
    actual_status = self.val.get('status')
    if actual_status != status:
        self.error(
            f'Invalid status for \'{self.val.get("method")}\'. Expected <{status}>, but was <{actual_status}>'
        )
    return self


def is_success(self: AssertionBuilder) -> AssertionBuilder:
    return _has_status(self, 'success')


def is_failure(self: AssertionBuilder) -> AssertionBuilder:
    return _has_status(self, 'failure')


add_extension(is_success)
add_extension(is_failure)

softly = soft_assertions
check = assert_that
