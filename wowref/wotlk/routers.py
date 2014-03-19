class Router(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['wotlk']:
            return model._meta.app_label
