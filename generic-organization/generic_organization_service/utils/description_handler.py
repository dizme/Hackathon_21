import logging
import os
import configparser
import copy
from enum import Enum
from generic_organization_service.interfaces.responses.generic_response import Description
from antidote import register
from generic_organization.settings import BASE_CODE_FOLDER, TEMPLATE_FOLDER_LIST
logger = logging.getLogger(__name__)


class DescriptionMessagesCodes:

    UNDEFINED = -1
    VERIFY_EXECUTED_SUCCESSFULLY = 1
    PROCESSING_ERROR = 2

    ERROR_DURING_ISSUE_CONTACT_SUPPORT = 97
    ERROR_DURING_VERIFY_CONTACT_SUPPORT = 98
    ERROR_DURING_VERIFY = 99


@register(singleton=True)
class DescriptionHandler:

    def __init__(self):
        self.descriptions = dict()
        self.unaivalable_description = list()
        self.unaivalable_description.append(Description("it", "Descrizione errore non disponibile"))
        self.unaivalable_description.append(Description("en", "Error description not available"))
        descriptions_path = os.getenv('I18N_PATH', None)
        self.__load_descriptions(descriptions_path)

        for root, dirs, files in os.walk(BASE_CODE_FOLDER, topdown=False,
                                         followlinks=False):
            if root.endswith("i18n") and not self.__is_template(root):
                logger.info("Add description from folder: %s", root)
                self.__load_descriptions(root)

    def __is_template(self, folder):
        for template in TEMPLATE_FOLDER_LIST:
            if template in folder:
                return True
        return False

    def __load_descriptions(self, descriptions_path):
        if descriptions_path:
            for filename in os.listdir(descriptions_path):
                config = configparser.ConfigParser()
                if filename.endswith(".lang"):
                    path_join = os.path.join(descriptions_path, filename)
                    config.read(path_join, encoding='utf-8')
                    for section in config.sections():
                        for key in config[section]:
                            description_elements = self.descriptions.get(key, None)

                            if not description_elements:
                                description_elements = list()
                                description_element = self.descriptions.get(key, None)
                                if not description_element:
                                    self.descriptions[key] = description_elements
                                else:
                                    logger.error("The key: %s is already present and it will not be added", key)

                            desc = Description(section, config[section][key])
                            description_elements.append(desc)

    def get_descriptions(self, description_message_code: DescriptionMessagesCodes, *args):
        description_list = self.descriptions.get(str(description_message_code), None)
        if args:
            description_list = copy.deepcopy(description_list)
            if description_list:
                for description in description_list:
                    try:
                        description.message = description.message.format(*args)
                    except IndexError as ie:
                        logger.error("String formatting error for description_message_code: %s - "
                                     "description: %s, provided format list values: %s",
                                     str(description_message_code), description, *args)
            else:
                logger.warning("Description not found for error code: %s", str(description_message_code))
                description_list = self.unaivalable_description
        return description_list