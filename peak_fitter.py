import matplotlib.pyplot as plt
from numpy import linspace, random, arange

from lmfit import Minimizer, Parameters
from lmfit.lineshapes import gaussian, lorentzian
from lmfit.printfuncs import report_fit, fit_report


class Peak:
    def __init__(self, centroid, amp):
        self.centroid = centroid
        self.amp = amp

    def __repr__(self):
        return f'Peak(cen={self.centroid:.2f}, amp={self.amp:.2f})'


class PeakFitter:
    ith_fit = 0

    def __init__(self, data_x, data_y, peaks):
        self.data_x = data_x
        self.data_y = data_y
        self.peaks = peaks
        self.result = None
        self.init = None
        self.fit = None

        self.params = Parameters()
        self._initialize_params()

    def _initialize_params(self):
        # initialize params for gaussian curves
        for i, peak in enumerate(self.peaks):
            self.params.add(name=f'amp_{i}', value=peak.amp)
            self.params.add(name=f'cen_{i}', value=peak.centroid)
            self.params.add(name=f'wid_{i}', value=1)

        # initialize params for linear background
        self.params.add(name='line_slope', value=0.0)
        self.params.add(name='line_off', value=0.0)

    def _gaussian_peaks(self, params, data_x):
        return sum(
            gaussian(data_x, params[f'amp_{i}'], params[f'cen_{i}'], params[f'wid_{i}'])
            for i, peak in enumerate(self.peaks)
        )

    def _linear_background(self, params, data_x):
        slope = params['line_slope']
        offset = params['line_off']
        return offset + data_x * slope

    def residual(self, params, data_x, sigma=None, data_y=None):
        model = self._gaussian_peaks(params, data_x) + self._linear_background(params, data_x)

        if data_y is None:
            return model
        if sigma is None:
            return model - data_y
        return (model - data_y) / sigma

    def fit_all(self):
        PeakFitter.ith_fit += 1

        myfit = Minimizer(self.residual, self.params,
                          fcn_args=(self.data_x,), fcn_kws={'data_y': self.data_y},
                          scale_covar=True)

        self.result = myfit.leastsq()
        self.init = self.residual(self.params, self.data_x)
        self.fit = self.residual(self.result.params, self.data_x)

        report_fit(self.result)

    def get_result(self):
        x = arange(self.data_x[0], self.data_x[-1], 0.1)
        return x, self.residual(self.result.params, x)


    def generate_fit_report(self):
        report = f'\n\n{"="*10}\nFIT REPORT\n{"="*10}\n\n'
        return report + fit_report(self.result.params)

