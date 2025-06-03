

# LG4X: lmfit GUI for XPS

## Preface
The extended version (LG4X-V2) is available from [here](https://github.com/Julian-Hochhaus/LG4X-V2) upgraded by [Julian Hochhaus](https://github.com/Julian-Hochhaus/). 
Furthermore, the advanced version (LG4X-V3) is available from [here](https://github.com/KherveFitting/KherveFitting/) developed by [Gwilherm Kerherve](https://www.linkedin.com/in/gwilherm-kerherve-3588b978/).
After the WFH period under the covid situation, I have no time to develop further this code (28 Mar. 2023).


## Introduction

**LG4X** provides a graphical user interface for [XPS](https://en.wikipedia.org/wiki/X-ray_photoelectron_spectroscopy) curve fitting analysis based on the [lmfit](https://pypi.org/project/lmfit/) package, which is the non-linear least-square minimization method on python platform. **LG4X** facilitates the curve fitting analysis for python beginners. **LG4X** was developed on [Python 3](https://www.python.org/), and [PyQt5](https://pypi.org/project/PyQt5/) was used for its graphical interface design. [Shirley](https://doi.org/10.1103/PhysRevB.5.4709) and [Tougaard](https://doi.org/10.1002/sia.740110902) iterated methods are implemented as a supplementary code for XPS background subtraction. **LG4X** tidies up all fitting parameters with their bound conditions in table forms. Fitting parameters can be imported and exported as a preset file before and after analysis to streamline the fitting procedures. Fitting results are also exported as a text for parameters and csv file for spectral data. In addition, **LG4X** simulates the curve without importing data and evaluates the initial parameters over the data plot prior to optimization.


## Methods
### Installation

Install [Python 3](https://www.python.org/) or [brew](https://brew.sh/), and [pip](https://pip.pypa.io/en/stable/installation/) additional packages.
```
brew install python3
pip3 install lmfit
pip3 install pandas
pip3 install matplotlib
pip3 install PyQt5
```
The OS dependence of installation of python, pip, and brew is described in the [link](https://appdividend.com/2020/04/22/how-to-upgrade-pip-in-mac-update-pip-on-windows-and-linux/).

#### Update package if necessary

```
pip3 install --upgrade lmfit
```

#### Miniconda3

If you have Miniconda3, you can create the environment to install lmfit from [conda-forge](https://github.com/conda-forge/lmfit-feedstock). Below is an example for environment name *vpy3.9* on python version 3.9 ([YouTube video](https://youtu.be/cEbo6ZHlK-U)). 

```
conda config --add channels conda-forge
conda config --set channel_priority strict
conda create -n vpy3.9 python=3.9
conda activate vpy3.9
conda install lmfit
conda install matplotlib
conda install pandas
python main.python
```


#### Supplementary codes for XPS analysis

[xpspy.py](https://github.com/heitler/LG4X/blob/master/Python/xpspy.py) should be located in the same directory as [main.py](https://github.com/heitler/LG4X/blob/master/Python/main.py) for XPS energy range selection for background (BG) subtraction in Shirley and Tougaard methods, which are taken from codes by [Kane O'Donnell](https://github.com/kaneod/physics/blob/master/python/specs.py) and [James Mudd](https://warwick.ac.uk/fac/sci/physics/research/condensedmatt/surface/people/james_mudd/igor/).

[vamas.py](https://github.com/heitler/LG4X/blob/master/Python/vamas.py) and [vamas_export.py](https://github.com/heitler/LG4X/blob/master/Python/vamas_export.py) are also necessary for importing ISO [VAMAS](https://doi.org/10.1002/sia.740130202) format file. vamas.py is a modifed class of VAMAS format from [Kane O'Donnell](https://github.com/kaneod/physics/blob/master/python/vamas.py).

[periodictable.py](https://github.com/heitler/LG4X/blob/master/Python/periodictable.py) and [periodictableui.py](https://github.com/heitler/LG4X/blob/master/Python/periodictableui.py) are the periodic table window to identify the peak elements. The codes are based on and revised from [clusterid](https://github.com/BrendanSweeny/clusterid).

[elements.py](https://github.com/heitler/LG4X/blob/master/Python/elements.py) and [elementdata.py](https://github.com/heitler/LG4X/blob/master/Python/elementdata.py) are the class for peak energy and sensitivity used in the priodic table above. The codes are based on and revised from [clusterid](https://github.com/BrendanSweeny/clusterid).

### Start LG4X

```
python3 main.py
```

#### Testing and developing environment

* Python 3.9.5
* asteval==0.9.31
* lmfit==1.2.2
* matplotlib==3.5.3
* numpy==1.21.6
* pandas==1.3.5
* PyQt5==5.15.2
* scipy==1.7.3
* uncertainties==3.1.6

### Usage

1. Import data
    - Import csv, text, or vamas (.vms/.npl) file format.
    - All csv and text files in a directory.
    - Choose data from file list if it was already imported.
1. Setup background and peak parameters with their types
    - Select energy range of spectrum for optimization.
    - Setup initial BG parameters including polynomial coefficients.
    - Setup peak model and its parameters.
    - Increase and decrease the number of peaks.
    - Load a preset file if available.
1. Evaluate parameters
    - Plot the curves without optimization.
    - Simulate the curves based on the range and peaks if no data file is selected in the File list.
1. Fit curve
    - Adjust parameters and bounds until they become converged
1. Export results
    - Export csv file for curves
    - Export text file for parameters
    - Save parameters as a preset for next analysis

#### Home directory to import data

You can change the HOME directory in the main.py edited in a way below. `#` makes a line comment out. 

```
# Home directory
self.filePath = QtCore.QDir.homePath()
# self.filePath = '/Users/hidekinakajima/Desktop/WFH2021_2/lg4x/LG4X-master/Python/'
```


## Citing

[https://doi.org/10.5281/zenodo.3901523](https://doi.org/10.5281/zenodo.3901523)

## Video

[YouTube: Introduction of LG4X](https://youtu.be/cDXXXBfWU1w)

[YouTube: Installation of LG4X in miniconda3 environment](https://youtu.be/cEbo6ZHlK-U)


## Database reference
X-ray data booklet for binding energy
- http://xdb.lbl.gov/

"Hartree-Slater subshell photoionization cross-sections at 1254 and 1487 eV"
J. H. Scofield, Journal of Electron Spectroscopy and Related Phenomena, 8129-137 (1976).
- http://dx.doi.org/10.1016/0368-2048(76)80015-1
- https://a-x-s.org/research/cross-sections/

"Calculated Auger yields and sensitivity factors for KLL-NOO transitions with 1-10 kV primary beams"
S. Mroczkowski and D. Lichtman, J. Vac. Sci. Technol. A 3, 1860 (1985).
- http://dx.doi.org/10.1116/1.572933
- http://www.materialinterface.com/wp-content/uploads/2014/11/Calculated-AES-yields-Matl-Interface.pdf

(Electron beam energy at 1, 3, 5, and 10 keV for relative cross section and derivative factors)


## Interface design

An initial gui concept is taken from [here](http://songhuiming.github.io/pages/2016/05/31/read-in-csv-and-plot-with-matplotlib-in-pyqt4/) and [there](https://stackoverflow.com/questions/47964897/how-to-graph-from-a-csv-file-using-matpotlib-and-pyqt5).

![LG4X interface cencept](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-24%20at%2021.24.14.png "GUI")

### Buttons

#### Evaluate
You can evaluate the fitting parameters without fitting optimization on data spectrum. If you do not select the data, it works as simulation mode in the range you specify in BG table (`x_min`, `x_max`, the number of data points `pt`).

#### Fit
You can optimize the fitting parameters by least-square method, and parameters in the table are updated after optimization.

#### Export
**LG4X** exports fitting results in two different files. One is a text file for fitting conditions `_fit.txt`, the other is a csv format file for data `_fit_csv`, which is saved at the same directory of the former file.

#### Add and rem peak
You can add and remove peak at the end of column from the Fit table.

### Drop-down menus

#### Importing data
**LG4X** imports csv format or tab separated text files. A data file should contain two columns. First column is energy and second column is spectral intensity. **LG4X** skips first row, because it is typically used for column names. Example data files are available in [Example](https://github.com/hidecode221b/LG4X/tree/master/Example). Energy and instensiy are calibrated in the Excel XPS macro ([EX3ms](https://github.com/hidecode221b/xps-excel-macro)) prior to the analysis for convenience. The method of energy calibration is discussed in the [link](https://doi.org/10.1016/j.pmatsci.2019.100591). 

VAMAS file format can also be imported in **LG4X** by decomposing a VAMAS file into the tab separated text files based on the block and sample idenfitifers. Exported tab separated text files are available in the same directory as the VAMAS file. You can just use **LG4X** to convert the VAMAS file into tab separated text files for the other program you prefer. Note that the binding energy scale is automatically created from VAMAS for XPS and UPS data.

Imported data is displayed in the figure and listed in the file list. You can also open the directory to import all csv and text files in the file list. 

#### File list
Imported file path is added in the list. You can choose the path to import a data file again from the list once you import the data file. Fitting parameters are loaded from `Fitting preset` menu below.

#### Fitting preset
Fitting condition can be created in the BG and Fit tables. From fitting preset drop-down menu, you can create the most simple single-peak preset from `New`. If you have a preset previously saved, you can `load` a preset file, which will be listed in the `Fitting preset`. Typical conditions for XPS `C1s` and `C K edge` are also available from the list as examples. A preset filename is ended with `_pars.dat`, and parameters include in the preset file as a list in the following way.

> [*BG type index*, [*BG table parameters*], [*Fit table parameters*]]

`Periodic table` is available to identify the peak position and relative intensity based on XPS Al K&#945; excitation source (1486.6 eV). If you change the excitation energy `hn` and work function `wf`, the core-level and Auger peak energies are revised according to the equation below.

> BE = hn - wf - KE

`BE` represents the binding energy, and `KE` kinetic energy. The database reference and example usage of periodic table are shown below. `Refresh` button enables us to display elements in the other dataset, and `Clear` button removes all elements.

#### BG types (`Shirley BG` to be shown as a default)
You can choose the BG type to be subtracted from the raw data as listed below. Shirley and Tougaard BG iteration functions are available from xpypy.py, which should be located with main.py. From lmfit [built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html), 3rd-order polynomial and 3 step functions are implemented. Fermi-Dirac (ThermalDistributionModel) is used for the Fermi edge fitting, and arctan and error functions (StepModel) for NEXAFS K edge BG. Polynomial function is added to the other BG models configured in the BG table, so polynomial parameters have to be taken into account for all BG optimization. You can turn off polynomial parameters by filling all zeros with turning on checkbox. Valence band maximum and secondary electron cutoff can be fitted with the 4th polynomial function for the density of states or edge jump at the onset. 

| No. | String | BG model | Parameters |
| --- | --- | --- | --- |
| 0 | | | `x_min`, `x_max` for fitting range, data points in simulation `pt`, `hn`, `wf` |
| 1 | | Shirley BG | Initial `cv`, max iteration number `it` |
| 2 | | Tougaard BG | `B`, `C`, `C'`, `D` |
| 3 | pg | [Polynomial BG](https://lmfit.github.io/lmfit-py/builtin_models.html#polynomialmodel) | c0, c1, c2, c3 |
| 4 | bg | [Fermi-Dirac BG](https://lmfit.github.io/lmfit-py/builtin_models.html#thermaldistributionmodel) | amplitude, center, kt |
| 5 | bg | [Arctan BG](https://lmfit.github.io/lmfit-py/builtin_models.html#stepmodel) | amplitude, center, sigma |
| 6 | bg | [Error BG](https://lmfit.github.io/lmfit-py/builtin_models.html#stepmodel) | amplitude, center, sigma |
| 7 | bg | VBM/cutoff | center, d1, d2, d3, d4 |

### Tables

#### BG table
You can specify the range for fitting region in the first row of BG table. Checkbox works as a constraint at the value beside. Range and polynomial rows are independent from the drop-down menu selection for background.

#### Fit table
All conditions are based on the lmfit [built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html) listed in the Fit table. Peak models are listed below. For standard XPS analysis, amplitude ratios `amp_ratio` and peak differences `ctr_diff` can be setup from their referenced peak `amp_ref` and `ctr_ref`, respectively from drop-down menu in each column. The number of peaks can be varied with `add peak` and `rem peak` buttons. Checkbox can be used for either fixing values or bound conditions if you check beside value. Empty cells do not effect to the optimization.

| No. | String | Peak model | Parameters |
| --- | --- | --- | --- |
| 1 | g | [GaussianModel](https://lmfit.github.io/lmfit-py/builtin_models.html#gaussianmodel) | amplitude`amp`, center`ctr`, sigma`sig` |
| 2 | l | [LorentzianModel](https://lmfit.github.io/lmfit-py/builtin_models.html#lorentzianmodel) | amplitude, center, sigma |
| 3 | v | [VoigtModel](https://lmfit.github.io/lmfit-py/builtin_models.html#voigtmodel) | amplitude, center, sigma, gamma`gam` |
| 4 | p | [PseudoVoigtModel](https://lmfit.github.io/lmfit-py/builtin_models.html#pseudovoigtmodel) | amplitude, center, sigma, fraction`frac` |
| 5 | e | [ExponentialGaussianModel](https://lmfit.github.io/lmfit-py/builtin_models.html#exponentialgaussianmodel) | amplitude, center, sigma, gamma |
| 6 | s | [SkewedGaussianModel](https://lmfit.github.io/lmfit-py/builtin_models.html#skewedgaussianmodel) | amplitude, center, sigma, gamma |
| 7 | a | [SkewedVoigtModel](https://lmfit.github.io/lmfit-py/builtin_models.html#skewedvoigtmodel) | amplitude, center, sigma, gamma, `skew` |
| 8 | b | [BreitWignerModel](https://lmfit.github.io/lmfit-py/builtin_models.html#breitwignermodel) | amplitude, center, sigma, `q` |
| 9 | n | [LognormalModel](https://lmfit.github.io/lmfit-py/builtin_models.html#lognormalmodel) | amplitude, center, sigma |
| 10 | d | [DoniachModel](https://lmfit.github.io/lmfit-py/builtin_models.html#doniachmodel) | amplitude, center, sigma, gamma |

##### Amplitude ratio and energy difference
XPS doublet peaks are splitted by the spin-orbit coupling based on the atomic theory. Spin-orbit interaction depends on the atomic element and its orbit. The energy separation of doublet corresponds to the spin-orbit constant. Amplitude ratio of doublet is based on the degeneracy (2*j*+1) of each total angular quantum number (*j*). **LG4X** constrains `amp_ratio` and `ctr_diff` from a reference peak `amp_ref` and `ctr_ref` selected by dropdown menus. For example, Ag3*d* has *j*=5/2 and 3/2, and their amplitude ratio corresponds to 3:2. You can setup second peak amplitude ratio by selecting the first peak at *j*=5/2 and `amp_ratio` = 0.67. This means that amplitude of second peak at *j*=3/2 is constrained by a factor of 0.67 against that of first peak. Peak difference parameter also works in a way that second peak position is away from first peak `ctr_ref` by `ctr_diff` = 6 eV as shown in the figure below. 

Note that amplitude used in the lmfit package is equivalent to the peak area that is propoertional to the amount of element in analytical area and depth by XPS. The atomic ratio is evaluated by the peak area normalized by the sensitivity factor. The ratio of sensitivity factors on doublet peaks is the same as that in multiplicity, so the normalized peak area of one doublet peak is the same as that in other one.

A comprehensive review on XPS technique and analytical procedures is available in link below.

> ["X-ray photoelectron spectroscopy: Towards reliable binding energy referencing" G. Greczynski and L. Hultman, Progress in Materials Science 107, 100591 (2020).](https://doi.org/10.1016/j.pmatsci.2019.100591)

## Examples

![XPS C1s spectrum](https://github.com/heitler/LG4X/blob/master/Images/Capture.PNG "XPS C1s spectrum")

![XPS Ag3d spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-27%20at%2023.14.49.png "XPS Ag3d spectrum")

![NEXAFS C K edge spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-22%20at%201.45.37.png "NEXAFS C K edge spectrum")

![UPS Fermi-edge spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-21%20at%2020.11.36.png "UPS Fermi-edge spectrum")

![Simulated spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-22%20at%201.15.35.png "Simulated spectrum")

![Survey scan](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202021-10-07%20at%200.03.56.png "Survey scan with periodic table")

You can find the VAMAS format data of various spectra from [Spectroscopy Hub](https://spectroscopyhub.com/measurements).




