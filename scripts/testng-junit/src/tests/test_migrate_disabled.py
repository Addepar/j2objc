from setup import testng2junit5

def test_migrate_enabled_false():
    original = """
@Test(enabled=false)
@User(UserRole.ADMIN)
public void secIdCreate() throws UtilsException {
"""
    expected = """
@Disabled @Test
@User(UserRole.ADMIN)
public void secIdCreate() throws UtilsException {
"""
    actual = testng2junit5.migrate_testng_annotations(original)
    assert expected == actual