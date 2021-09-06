

# LG4X: lmfit GUI for XPS

## Introduction

LG4X provides a graphical user interface for [XPS](https://en.wikipedia.org/wiki/X-ray_photoelectron_spectroscopy) curve fitting analysis based on the [lmfit](https://pypi.org/project/lmfit/) package, which provides the non-linear least-square minimization method for Python. LG4X facilitates the curve fitting analysis for python beginners. LG4X was developed on [Python 3](https://www.python.org/) and [PyQt5](https://pypi.org/project/PyQt5/) was used for its graphical interface design. [Shirley](https://doi.org/10.1103/PhysRevB.5.4709) and [Tougaard](https://doi.org/10.1002/sia.740110902) iterated methods are implemented as a supplementary code for XPS background subtraction. LG4X tidies up all fitting parameters with their bound conditions in tables. Fitting parameters can be imported and exported as a preset file before and after analysis to streamline the fitting procedures. Fitting results are also exported as a text for parameters and csv file for spectral data. In addition, LG4X simulates the curve without importing data and evaluates the initial parameters over the data plot prior to optimization.


## Methods
### Installation

Download and install [Python 3](https://www.python.org/) and additional packages.

> `brew install python3`
>
> `pip3 install lmfit`
>
> `pip3 install pandas`
>
> `pip3 install matplotlib`
>
> `pip3 install PyQt5`

The OS dependence of installation of python, pip, and brew is described in the [link](https://appdividend.com/2020/04/22/how-to-upgrade-pip-in-mac-update-pip-on-windows-and-linux/).

### Update package if necessary

> `pip3 install --upgrade lmfit`

### Supplementary code for XPS analysis

[xpspy.py](https://github.com/heitler/LG4X/blob/master/Python/xpspy.py) should be located in the same directory as [main.py](https://github.com/heitler/LG4X/blob/master/Python/main.py) for XPS energy range selection for background (BG) subtraction in Shirley and Tougaard methods, which are taken from codes by [Kane O'Donnell](https://github.com/kaneod/physics/blob/master/python/specs.py) and [James Mudd](https://warwick.ac.uk/fac/sci/physics/research/condensedmatt/surface/people/james_mudd/igor/).

[vamas.py](https://github.com/heitler/LG4X/blob/master/Python/vamas.py) and [vamas_export.py](https://github.com/heitler/LG4X/blob/master/Python/vamas_export.py) are also necessary for importing ISO [VAMAS](https://doi.org/10.1002/sia.740130202) format file. vamas.py is a modifed class of VAMAS format from [Kane O'Donnell](https://github.com/kaneod/physics/blob/master/python/vamas.py).

### Start LG4X

> `python3 main.py`

### Testing and developing environment

* Python 3.9.5
* asteval==0.9.23
* lmfit==1.0.2
* matplotlib==3.4.3
* numpy==1.20.3
* pandas==1.3.2
* PyQt5==5.15.4
* scipy==1.6.3
* uncertainties==3.1.5

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
    - Simulate the curves if no data file is selected in the File list.
1. Fit curve
    - Adjust parameters and bounds until they become converged
1. Export results
    - Export csv file for curves
    - Export text file for parameters
    - Save parameters as a preset for next analysis

## Interface design

An initial gui concept is taken from [here](http://songhuiming.github.io/pages/2016/05/31/read-in-csv-and-plot-with-matplotlib-in-pyqt4/) and [there](https://stackoverflow.com/questions/47964897/how-to-graph-from-a-csv-file-using-matpotlib-and-pyqt5).

![LG4X interface cencept](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-24%20at%2021.24.14.png "GUI")

### Buttons

#### Evaluate
You can evaluate the fitting parameters without fitting optimization on data spectrum. If you have not imported the data, it works for simulation mode in the range you specify.

#### Fit
You can optimize the fitting parameters by least-square method, and parameters in the table are updated after optimization.

#### Export
LG4X exports fitting results in two different files. One is a text file for fitting conditions(`_fit.txt`), the other is a csv format file for data(`_fit_csv`), which is saved at the same directory of the former file.

#### Add and rem peak
You can add and remove peak at the end of column from the Fit table.

### Drop-down menus

#### Importing data
LG4X imports csv format or tab separated text files. A data file should contain two columns. First column is energy and second column is spectral intensity. LG4X skips first row, because it is typically used for column names. Energy and instensiy are calibrated in the Excel XPS macro ([EX3ms](https://github.com/hidecode221b/xps-excel-macro)) prior to the analysis for convenience. The method of energy calibration is discussed in the [link](https://doi.org/10.1016/j.pmatsci.2019.100591). 

**Update**: VAMAS file format can also be imported in LG4X by decomposing a VAMAS file into the tab separated text files based on the block and sample idenfitifers. Exported tab separated text files are available in the same directory as the VAMAS file. You can just use LG4X to convert the VAMAS file into tab separated text files for the other program you prefer. Note that the binding energy scale is automatically created from VAMAS for XPS and UPS data.

Imported data is displayed in the figure and listed in the file list. You can also open the directory to import all csv and text files in the file list. 

#### File list
Imported file path is added in the list. You can choose the path to import a data file again from the list once you import the data file.

#### Fitting preset
Fitting condition can be created in the BG and Fit tables. From fitting preset drop-down menu, you can generate the most simple single-peak condition from `New`. If you have a preset previously saved, you can `load` a preset file, which will be listed in the fitting preset. Default conditions for XPS `C1s` and `C K edge` are also available from the list as examples. A preset filename is ended with `_pars.dat`, and parameters include in the preset file as a list in the following way.

> `[*BG type index*, [*BG table parameters*], [*Fit table parameters*]]`

#### BG types (`Shirley BG` to be shown as a default)
You can choose the BG type to be subtracted from the raw data as listed below. Shirley and Tougaard BG iteration functions are available from xpypy.py, which should be located with main.py. From lmfit [built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html), 3rd-order polynomial and 3 step functions are implemented. Fermi-Dirac (ThermalDistributionModel) is used for the Fermi edge fitting, and arctan and error functions (StepModel) for NEXAFS K edge BG. Polynomial function is added to the other BG models configured in the BG table, so polynomial parameters have to be taken into account for all BG optimization. You can turn off polynomial parameters by filling all zeros with turning on checkbox. Valence band maximum and secondary electron cutoff can be fitted with the 4th polynomial function for the density of states or edge jump at the onset. 

| No. | String | BG model | Parameters |
| --- | --- | --- | --- |
| 0 | | | x_min, x_max for fitting region in spectrum |
| 1 | | Shirley BG | Initial, max iteration, # of points for simulation |
| 2 | | Tougaard BG | B, C, C', D |
| 3 | pg | Polynomial BG | c0, c1, c2, c3 |
| 4 | bg | Fermi-Dirac BG | amplitude, center, kt |
| 5 | bg | Arctan BG | amplitude, center, sigma |
| 6 | bg | Error BG | amplitude, center, sigma |
| 7 | bg | VBM/cutoff | center, d1, d2, d3, d4 |

### Tables

#### BG table
You can specify the range for fitting region in the first row of BG table. Checkbox works as a constraint at the value beside. Range and polynomial rows are independent from the drop-down menu selection for background.

#### Fit table
All conditions are based on the lmfit [built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html) listed in the Fit table. Peak models are listed below. For standard XPS analysis, amplitude ratios(`amp_ratio`) and peak differences(`ctr_diff`) can be setup from their referenced peak(`amp_ref` and `ctr_ref`, respectively) from drop-down menu in each column. The number of peaks can be varied with `add peak` and `rem peak` buttons. Checkbox can be used for either fixing values or bound conditions if you check beside value. Empty cells do not effect to the optimization.

| No. | String | Peak model | Parameters |
| --- | --- | --- | --- |
| 1 | g | GaussianModel | amplitude(`amp`), center(`ctr`), sigma(`sig`) |
| 2 | l | LorentzianModel | amplitude, center, sigma |
| 3 | v | VoigtModel | amplitude, center, sigma, gamma(`gam`) |
| 4 | p | PseudoVoigtModel | amplitude, center, sigma, fraction(`frac`) |
| 5 | e | ExponentialGaussianModel | amplitude, center, sigma, gamma |
| 6 | s | SkewedGaussianModel | amplitude, center, sigma, gamma |
| 7 | a | SkewedVoigtModel | amplitude, center, sigma, gamma, `skew` |
| 8 | b | BreitWignerModel | amplitude, center, sigma, `q` |
| 9 | n | LognormalModel | amplitude, center, sigma |
| 10 | d | DoniachModel | amplitude, center, sigma, gamma |

##### Amplitude ratio and energy difference
XPS doublet peaks are splitted by the spin-orbit coupling based on the atomic theory. Spin-orbit interaction depends on the atomic element and its orbit. The energy separation of doublet corresponds to the spin-orbit constant. Amplitude ratio of doublet is based on the degeneracy (2*j*+1) of each total angular quantum number (*j*). LG4X constrains `amp_ratio` and `ctr_diff` from a reference peak (`amp_ref` and `ctr_ref`) selected by dropdown menus. For example, Ag3*d* has *j*=5/2 and 3/2, and their amplitude ratio corresponds to 3:2. You can setup second peak amplitude ratio by selecting the first peak at *j*=5/2 and `amp_ratio` = 0.67. This means that amplitude of second peak at *j*=3/2 is constrained by a factor of 0.67 against that of first peak. Peak difference parameter also works in a way that second peak position is away from first peak(`ctr_ref`) by `ctr_diff` = 6 eV as shown in the figure below. 

Note that amplitude used in the lmfit package is equivalent to the peak area that is propoertional to the amount of element in analytical area and depth by XPS. The atomic ratio is evaluated by the peak area normalized by the sensitivity factor. The ratio of sensitivity factors on doublet peaks is the same as that in multiplicity, so the normalized peak area of one doublet peak is the same as that in other one.

A comprehensive review on XPS technique and analytical procedures is available in link below.

> ["X-ray photoelectron spectroscopy: Towards reliable binding energy referencing" G. Greczynski and L. Hultman, Progress in Materials Science 107, 100591 (2020).](https://doi.org/10.1016/j.pmatsci.2019.100591)

## Examples

![XPS C1s spectrum](https://github.com/heitler/LG4X/blob/master/Images/Capture.PNG "XPS C1s spectrum")

![XPS Ag3d spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-27%20at%2023.14.49.png "XPS Ag3d spectrum")

![NEXAFS C K edge spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-22%20at%201.45.37.png "NEXAFS C K edge spectrum")

![UPS Fermi-edge spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-21%20at%2020.11.36.png "UPS Fermi-edge spectrum")

![Simulated spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-22%20at%201.15.35.png "Simulated spectrum")

You can find the VAMAS format data of various spectra from [Spectroscopy Hub](https://spectroscopyhub.com/measurements).





