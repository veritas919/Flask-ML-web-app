import pprint
from typing import Dict, Union, List


def format_dict(d: Union[Dict, List]) -> str:
    """
    FORMAT A DICT OR A LIST INTO A NICE OBJECT THAT CAN BE PRINTED IN HTML
    :param d: THE DICT OR LIST
    :return: A HTML-FORMATTED STRING
    """
    return pprint.pformat(d, indent=4).replace(',\n', ',<br>').replace('\n', '<br>').replace(' ', '&nbsp')