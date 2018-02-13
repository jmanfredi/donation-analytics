from contextlib import contextmanager
import numpy as np

def calc_percentile(values,percent):
        '''Given a list of values and a percent value, calculate the percentile using the nearest-rank method.'''
        index = int(np.ceil((float(percent)/100)*len(values)))
        return sorted(values)[index-1]

@contextmanager
def smart_open(filename, mode='r'):
    '''This function returns an error condition if there is a problem opening the file.'''
    try:
        f = open(filename, mode)
    except IOError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()
                                                    
