import netCDF4
import numpy.ma as ma
import numpy as np
class CheckingNetCDFDataProxy(object):
    """A reference to the data payload of a single NetCDF file variable."""

    __slots__ = ('shape', 'dtype', 'path', 'variable_name', 'fill_value', 'safety_check_done', 'fatal_fail')

    def __init__(self, shape, dtype, path, variable_name, fill_value, do_safety_check=False):
        self.safety_check_done = do_safety_check
        self.shape = shape
        self.dtype = dtype
        self.path = path
        self.variable_name = variable_name
        self.fill_value = fill_value
        self.fatal_fail = None

    @property
    def ndim(self):
        return len(self.shape)

    def check(self):
        try:
            dataset = netCDF4.Dataset(self.path)
        except OSError:
            self.fatal_fail = "no such file %s" % self.path
            self.safety_check_done = True
            return
        
        try:
            variable = dataset.variables[self.variable_name]
        except KeyError:
            self.fatal_fail = "no variable %s in file %s" % (self.variable_name, self.path)
            self.safety_check_done = True
            return

        if list(variable.shape) != list(self.shape):
            self.fatal_fail = "Shape of data %s doesn't match expected %s" %(variable.shape, self.shape)
            self.safety_check_done = True
            return
        
        # TODO check variables???
        
        self.safety_check_done = True
        
        
    def  _null_data(self, keys):
        print('Returning null data (%s:%s):%s because %s' % (self.path.split('/')[-1], self.variable_name, keys, self.fatal_fail))
        null_data = np.ones(self.shape)[keys] * self.fill_value
        return null_data
        
    def __getitem__(self, keys):
        print('__getitem__ (%s:%s)' % (self.path.split('/')[-1], self.variable_name), keys)
        
        if not self.safety_check_done:
            self.check()
            
        if self.fatal_fail:
            return self._null_data(keys)
            
        try:
            dataset = netCDF4.Dataset(self.path)
            variable = dataset.variables[self.variable_name]
            # Get the NetCDF variable data and slice.
            var = variable[keys]
        finally:
            if dataset:
                dataset.close()
        return np.asanyarray(var)

    def __repr__(self):
        fmt = '<{self.__class__.__name__} shape={self.shape}' \
              ' dtype={self.dtype!r} path={self.path!r}' \
              ' variable_name={self.variable_name!r}>'
        return fmt.format(self=self)

    def __getstate__(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def __setstate__(self, state):
        for key, value in six.iteritems(state):
            setattr(self, key, value)