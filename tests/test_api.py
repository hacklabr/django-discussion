import factory
from rest_assured.testcases import ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase
from django.contrib.auth.models import User
from discussion.models import Category


# class TestUser(factory.DjangoModelFactory):
#
#     class Meta:
#         model = User
#         exclude = ('raw_password',)
#
#     first_name = 'Robert'
#     last_name = factory.Sequence(lambda n: 'Paulson the {0}'.format(n))
#     email = factory.sequence(lambda n: 'account{0}@example.com'.format(n))
#     username = 'mayhem'
#     raw_password = '123'
#     password = factory.PostGenerationMethodCall('set_password', raw_password)
#     is_active = True


class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Category


class CategoryAPITestCase(ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase):

    base_name = 'category'
    factory_class = CategoryFactory
    update_data = {'title': 'Title changed', 'description': 'Changed Changed'}

    def setUp(self):

        self.user = User.objects.create_user(username='jacob', email='jacob@asfsfd.com', password='top_secret')
        self.client.force_authenticate(self.user)
        super(CategoryAPITestCase, self).setUp()

    # def get_object(self, factory):
    #     return factory.create(user=[self.user])

    def get_create_data(self):
        # import pdb;pdb.set_trace()
        return {'title': 'Title',
                # 'slug': 'slug_test',
                'description': 'Test text Test text Test text Test text Test text',
                'author': self.user.pk
                }
