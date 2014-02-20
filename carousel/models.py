from itertools import chain, groupby
import random
import datetime

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _

from utils import shuffled


class Carousel(models.Model):

    class DISTRIBUTIONS(object):
        SEQUENTIAL = 1
        RANDOM = 2
        WEIGHTED_RANDOM = 3
        CLUSTER_RANDOM = 4

        choices = [
            (SEQUENTIAL, _("sequential")),
            (RANDOM, _("random")),
            (WEIGHTED_RANDOM, _("weighted random")),
            (CLUSTER_RANDOM, _("cluster random"))
        ]

    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)
    distribution = models.PositiveSmallIntegerField(_('distribution'),
                                                    choices=DISTRIBUTIONS.choices,
                                                    default=DISTRIBUTIONS.SEQUENTIAL)

    def __init__(self, *args, **kwargs):
        super(Carousel, self).__init__(*args, **kwargs)
        self.__elements_cache = {}

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('carousel')
        verbose_name_plural = _('carousels')
        ordering = ('name', )

    def get_elements(self, seed=None, clear_cache=False):
        """
        Returns the list of elements for this carousel.
        The order in which they are returned depends on the `distribution` field.
        """
        if clear_cache:
            self.__elements_cache = {}
        if self.distribution not in self.__elements_cache:
            if seed is not None:
                random.seed(seed)
            fn = {
                self.DISTRIBUTIONS.SEQUENTIAL: self._get_elements_sequential,
                self.DISTRIBUTIONS.RANDOM: self._get_elements_random,
                self.DISTRIBUTIONS.WEIGHTED_RANDOM: self._get_elements_weighted_random,
                self.DISTRIBUTIONS.CLUSTER_RANDOM: self._get_elements_cluster_random
            }.get(self.distribution)
            self.__elements_cache[self.distribution] = list(fn())
        return self.__elements_cache[self.distribution]

    def _get_elements(self):
        return self.elements.active()

    def _get_elements_sequential(self):
        """
        Elements are sorted according to their `position` attribute.
        """
        return self._get_elements().order_by('position')

    def _get_elements_random(self):
        """
        Elements are simply shuffled randomly.
        """
        return shuffled(self._get_elements())

    def _get_elements_weighted_random(self):
        """
        Elements are shuffled semi-randomly.
        The `position` attribute of each element act as a weight for the randomization.
        Elements that are "heavier" are more likely to be at the beginning of the list.
        """
        return shuffled(self._get_elements(), weight=lambda e: e.position)

    def _get_elements_cluster_random(self):
        """
        Elements are grouped according to their `position` attribute.
        Each group is then shuffled randomly.
        """
        qs = self._get_elements().order_by('position')
        grouped = groupby(qs, key=lambda e: e.position)
        return chain.from_iterable(shuffled(elements) for _, elements in grouped)

    def elements_count(self, *args, **kwargs):
        count = len(self.get_elements(*args, **kwargs))
        return count


class CarouselElementQuerySet(QuerySet):

    def published(self):
        return self.filter(published=True)

    def active(self):
        return self.published().filter(
            Q(start_date__isnull=True) | Q(start_date__lte=datetime.datetime.now()),
            Q(end_date__isnull=True) | Q(end_date__gte=datetime.datetime.now())
        )


class CarouselElementManager(models.Manager):

    def get_query_set(self):
        return CarouselElementQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_query_set().published()

    def active(self):
        return self.get_query_set().active()


class CarouselElement(models.Model):
    POSITION_HELP_TEXT = _("The position of the element in the sequence or "
                           "the weight of the element in the randomization "
                           "process (depending on the carousel's distribution).")
    START_DATE_HELP_TEXT = _("If this field is filled show starts with a specified date")
    END_DATE_HELP_TEXT = _("If this field is filled show ending with a specified date")
    carousel = models.ForeignKey(Carousel, verbose_name=_('carousel'),
                                 related_name='elements')
    name = models.CharField(_('name'), max_length=50)
    image = models.ImageField(_('image'), upload_to='carousel_uploads')
    url = models.URLField(_('URL'), blank=True)
    position = models.PositiveIntegerField(_('position'), default=1,
                                           help_text=POSITION_HELP_TEXT)
    published = models.BooleanField(_('published'), default=1)
    start_date = models.DateTimeField(_('start date'), blank=True, null=True, help_text=START_DATE_HELP_TEXT)
    end_date = models.DateTimeField(_('end date'), blank=True, null=True, help_text=END_DATE_HELP_TEXT)

    objects = CarouselElementManager()

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('carousel element')
        verbose_name_plural = _('carousel elements')
        ordering = ('position', 'name')
