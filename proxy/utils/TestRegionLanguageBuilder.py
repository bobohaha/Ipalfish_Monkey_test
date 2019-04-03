# -*- encoding: utf-8 -*-
from proxy import param


class TestRegionLanguageBuilder:
    def __init__(self):
        pass

    @staticmethod
    def get_test_region_language(device_name=None, package_name=None):
        test_region_language = {}
        test_region = TestRegionLanguageBuilder.get_test_region(device_name=device_name,
                                                                package_name=package_name)
        test_language = TestRegionLanguageBuilder.get_test_language(test_region=test_region)
        if test_region is not None:
            test_region_language.setdefault(param.TEST_REGION_KEY, test_region)
        if test_language is not None:
            test_region_language.setdefault(param.TEST_LANGUAGE_KEY, test_language)

        return test_region_language

    @staticmethod
    def get_test_region(device_name=None, package_name=None):
        if device_name is None and package_name is None:
            return param.TEST_REGION_DEFAULT
        test_region = None
        if device_name is not None:
            for region in param.TEST_REGION_DEVICE.keys():
                if device_name in param.TEST_REGION_DEVICE[region]:
                    return region

        if package_name is not None:
            for region in param.TEST_REGION_PACKAGE.keys():
                if package_name in param.TEST_REGION_PACKAGE[region]:
                    return region

        return test_region

    @staticmethod
    def get_test_language(test_region=None, package_name=None):
        if test_region is None and package_name is None:
            return param.TEST_LANGUAGE_DEFAULT
        test_language = None
        if test_region is not None:
            if test_region in param.TEST_REGION_LANGUAGE.keys():
                return param.TEST_REGION_LANGUAGE[test_region]

        return test_language

    @staticmethod
    def get_target_region_language(language, region):
        target_region_language = {}
        if language is not None and language != "None" and language != "":
            if "（" in language:
                language = language.replace("（", " \(")
            elif "(" in language and "\(" not in language:
                language = language.replace("(", " \(")
            if "）" in language:
                language = language.replace("）", "\)")
            elif ")" in language and "\)" not in language:
                language = language.replace(")", "\)")
            language_pieces = language.split()
            if len(language_pieces) > 1:
                _language = ""
                for piece in language_pieces:
                    _language += piece + "\ "
                language = _language[:-2]
            language = "\"{}\"".format(language)
            target_region_language.setdefault(param.TEST_TARGET_LANGUAGE_KEY, language)

        if region is not None and region != "None" and region != "":
            target_region_language.setdefault(param.TEST_TARGET_REGION_KEY, region)

        return target_region_language
