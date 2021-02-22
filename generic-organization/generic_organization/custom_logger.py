from pprint import pformat, pprint
import logging
import re


class ImageMaskingFilter(logging.Filter):
    """Demonstrate how to filter sensitive data:"""

    def filter(self, record):
        #print("RECORD IS TYPE"+type(record))
        # The call signature matches string interpolation: args can be a tuple or a lone dict
        if isinstance(record.args, dict):
            record.args = self.sanitize_dict(record.args)
        else:
            record.args = tuple(self.sanitize_dict(i) for i in record.args)

        return True

    @staticmethod
    def sanitize_dict(d):
        #print("************D TYPE IS " + str(type(d)))

        if isinstance(d, str):
            d_filtered = re.sub(r'9j([^\"]*)\'', '*** image base64 data ***', d)
            return d_filtered

        if not isinstance(d, dict):
            return d

        if any(i for i in d.keys() if 'selfie_img' in i):
            d = d.copy()  # Ensure that we won't clobber anything critical

            for k, v in d.items():
                if 'selfie_img' in k:
                    d[k] = '*** image base64 data ***'

        return d


def recursive_items(d):
    for key, value in d.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)


class CustomFormatter(logging.Formatter):
    def format(self, record):
        res = super(CustomFormatter, self).format(record)

        if hasattr(record, 'request'):
            filtered_request = ImageMaskingFilter.sanitize_dict(record.request)
            res += '\n\t' + pformat(filtered_request, indent=4).replace('\n', '\n\t')
        return res
