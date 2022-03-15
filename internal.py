################################################################################
# Filename: internal.py                                                        #
# Created by: Venceslas Duet                                                   #
# Created at: 04-05-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: Collection of check functions                                   #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

def correct_tuple(element, tuple_type, length=-1):
    if not (isinstance(element, tuple) or
            isinstance(element, list)):
        return False
    length = length if length > 0 else len(element)
    if len(element) != length:
        return False
    for i in range(length):
        if type(element[i]) != tuple_type:
            return False
    return True
