import re
from testng2junit import *

content = """

  @Test(expectedExceptions = IllegalArgumentException.class,
      expectedExceptionsMessageRegExp = "no last date of range without upper bound: .*")
  public void testGetLast_failUnbounded() {
    DateRangeUtil.getLast(UNBOUNDED_ABOVE);
  }

"""

print(migrate_exceptions(content))
