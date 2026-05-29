class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self, filters=None, order_by=None):
        qs = self.model.objects.all()

        if filters:
            qs = qs.filter(**filters)

        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def get_by_id(self, id, prefetch_related=None, select_related=None):
        qs = self.model.objects

        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)

        if select_related:
            qs = qs.select_related(*select_related)

        return qs.filter(id=id).first()

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, entity, **kwargs):
        for key, value in kwargs.items():
            setattr(entity, key, value)
        entity.save()
        return entity

    def delete(self, entity):
        entity.delete()

    def exists(self, id):
        return self.model.objects.filter(id=id).exists()

    def count(self, filters=None):
        if filters:
            return self.model.objects.filter(**filters).count()
        return self.model.objects.count()