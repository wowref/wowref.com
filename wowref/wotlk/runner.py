from django.test.runner import DiscoverRunner

from wotlk.dbc import load_dbc_data


class ManagedModelRunner(DiscoverRunner):
    """
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run, so that one doesn't need
    to execute the SQL manually to create them.
    """

    load_dbc_data()

    def setup_test_environment(self, *args, **kwargs):
        from django.db.models.loading import get_models
        self.unmanaged_models = [m for m in get_models()
                                 if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(ManagedModelRunner, self).setup_test_environment(*args,
                                                               **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(ManagedModelRunner, self).teardown_test_environment(*args,
                                                                  **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False
