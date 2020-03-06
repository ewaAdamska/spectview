import re
import os
import numpy as np


class GateInfo:

    def __init__(self, filename: str):
        self.filename = filename
        self.type_ = self.read_gate_type_from_filename()
        self.gammas_list = [int(x[1:]) for x in re.findall('g\d+', os.path.basename(self.filename))]

    def __repr__(self):
        return self.filename.split('/')[-1].split('.')[0]

    def __str__(self):
        return self.type_+' '+' - '.join([str(x) for x in self.gammas_list])

    def read_gate_type_from_filename(self):
        if 'gate' in self.filename:
            return 'gate'
        elif 'bg' in self.filename:
            return 'bg'


class DataSet:

    def __init__(self, spectrum, gate):
        self.spectrum = spectrum
        self.gate = gate

    @classmethod
    def from_txt(cls, file):
        spectrum = np.genfromtxt(file, dtype=int)
        gate = GateInfo(filename=file)
        return cls(spectrum=spectrum, gate=gate)


    @classmethod
    def from_hdf5(cls, file):  # TODO: implement it!
        pass

    def get_spectrum(self, slicing=None):
        if not slicing:
            return np.arange(0, len(self.spectrum)), self.spectrum
        else:
            return np.arange(*slicing), self.spectrum[slice(*slicing)]

    def __repr__(self):
        return 'DataSet({}, {})'.format(self.gate.read_gate_name(), self.gate.type)

