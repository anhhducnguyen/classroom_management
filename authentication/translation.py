from modeltranslation.translator import TranslationOptions, register

from authentication.models import Class


@register(Class)
class ClassTranslation(TranslationOptions):
    pass