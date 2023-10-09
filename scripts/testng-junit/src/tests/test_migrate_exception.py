from setup import testng2junit
from setup import assert_equal_content

content = """

  @Test(expectedExceptions = IllegalArgumentException.class,
      expectedExceptionsMessageRegExp = "no last date of range without upper bound: .*")
  public void testGetLast_failUnbounded() {
    DateRangeUtil.getLast(UNBOUNDED_ABOVE);
  }

"""

expected = """
  @Test
  public void testGetLast_failUnbounded() {
	assertThrows(
        () -> {
		    DateRangeUtil.getLast(UNBOUNDED_ABOVE);
        },
        IllegalArgumentException.class,
        "no last date of range without upper bound: .*"
    );
  }
"""


def test_migrate_exceptions():
    content_new = testng2junit.migrate_exceptions(content)
    assert_equal_content(content_new, expected)
