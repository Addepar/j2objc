from setup import testng2junit5
from setup import assert_equal_content


content_1 = """

    @Guice(modules = SomeModule.class)
    public class SomeTest {

      @BeforeAll
      public void someTest() {

      }
    }

"""

expected_1 = """

    @TestInstance(Lifecycle.PER_CLASS)
    public class SomeTest {

      private final Injector injector = Guice.createInjector(new SomeModule());

      @BeforeAll
      @SuppressWarnings("ProhibitedExceptionCaught")
      public void someTest() {
        try {
          injector.injectMembers(this);
        } catch (Exception e) {
        }
      }
    }
"""

content_2 = """

    @Guice
    public class SomeTest {

      @BeforeAll
      public void someTest() {

      }
    }

"""

expected_2 = """

    @TestInstance(Lifecycle.PER_CLASS)
    public class SomeTest {

      private final Injector injector = Guice.createInjector();

      @BeforeAll
      @SuppressWarnings("ProhibitedExceptionCaught")
      public void someTest() {
        try {
          injector.injectMembers(this);
        } catch (Exception e) {
        }
      }
    }
"""

content_3 = """

    @Guice(modules = {TestModuleA.class,
        Test.ModuleB.class})
    public class SomeTest {

      @BeforeAll
      public void someTest() {

      }
    }

"""

expected_3 = """

    @TestInstance(Lifecycle.PER_CLASS)
    public class SomeTest {

      private final Injector injector = Guice.createInjector(new TestModuleA(), new Test.ModuleB());

      @BeforeAll
      @SuppressWarnings("ProhibitedExceptionCaught")
      public void someTest() {
        try {
          injector.injectMembers(this);
        } catch (Exception e) {
        }
      }
    }
"""


def test_migrate_guice_annotation():
    assert_equal_content(testng2junit5.migrate_guice_annotation(content_1), expected_1)
    assert_equal_content(testng2junit5.migrate_guice_annotation(content_2), expected_2)
    assert_equal_content(testng2junit5.migrate_guice_annotation(content_3), expected_3)
