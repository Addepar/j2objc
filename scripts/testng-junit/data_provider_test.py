import re
from testng2junit import *

content = """

  @DataProvider(name = BAD_CHAR_NAMES)
  public Object[][] provideBadCharNames() {
    return new Object[][]{
        {""},
        {"hello!world"}
    };
  }
  
  @Test(dataProvider = BAD_CHAR_NAMES, expectedExceptions = IllegalArgumentException.class)
  public void testReserved(String name) {
    JsonApiNaming.checkName(name);
  }

  @Test(dataProvider = "args")
  public void testIsDoubleZero(double val, boolean expected, boolean ignore1, boolean ignore2) {
    assertThat("expected isDoubleZero() for + " + val + " to be " + expected,
        EqualityUtils.isDoubleZero(val), is(expected));
  }

  @DataProvider(name = "args")
  public Object[][] getArgs() {
    return new Object[][] {
        {0d, true, true, true},
        {1E-10, true, true, true},
        {1E-8, false, true, true},
        {1E-4, false, false, true},
        {1E-2, false, false, false}
    };
  }
  
"""

print(migrate_data_providers(content))
