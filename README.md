

# LG4X: lmfit gui for xps

## Introduction

LG4X provides a graphical user interface for [XPS](https://en.wikipedia.org/wiki/X-ray_photoelectron_spectroscopy) curve fitting analysis based on the [lmfit](https://lmfit.github.io/lmfit-py/installation.html) package, which provides the non-linear least-square minimization method for Python. LG4X facilitates the curve fitting analysis for python beginners. LG4X was developed on [Python 3](https://www.python.org/) and PyQt5 was used for its graphical interface design. Shirley and Tougaard iterated methods are implemented as a supplementary code for XPS background subtraction. LG4X tidies up all fitting parameters with their bound conditions in tables. Fitting parameters can be imported and exported as a preset file before and after analysis to streamline the fitting procedures. Fitting results are also exported as a text for parameters and csv file for spectral data. In addition, LG4X simulates the curve without importing data and evaluates the initial parameters over the data plot prior to optimization.


## Methods
### Installation

Download and install [Python 3](https://www.python.org/)

> pip install lmfit

> pip install pandas

> pip install matplotlib

> pip install PyQt5


### Update package if necessary

> pip install --upgrade lmfit

### Supplementary code for XPS analysis

xpspy.py should be located in the same directory as main.py for XPS energy range selection for background subtraction in Shirley and Tougaard methods, which are taken from codes by [Kane O'Donnell](https://github.com/kaneod/physics/blob/master/python/specs.py) and [James Mudd](https://warwick.ac.uk/fac/sci/physics/research/condensedmatt/surface/people/james_mudd/igor/).

### Start LG4X

> python main.py

### Testing and developing environment

* Python 3.8.3
* asteval==0.9.18
* lmfit==1.0.1
* matplotlib==3.2.1
* numpy==1.18.4
* pandas==1.0.3
* PyQt5==5.14.2
* scipy==1.4.1
* uncertainties==3.1.2

### Usage

1. Import csv data
1. Setup background and peak parameters with their types
1. Evaluate parameters
1. Fit curve
1. Save parameters as a preset for next analysis
1. Export results

## Interface design

An initial gui concept is taken from [here](http://songhuiming.github.io/pages/2016/05/31/read-in-csv-and-plot-with-matplotlib-in-pyqt4/) and [there](https://stackoverflow.com/questions/47964897/how-to-graph-from-a-csv-file-using-matpotlib-and-pyqt5).

![LG4X interface cencept](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-24%20at%2021.24.14.png "GUI")

### Buttons

#### Evaluation
You can evaluate the fitting parameters without fitting optimization on data spectrum. If you have not imported the data, it works for simulation mode in the range you specify.

#### Fit
You can optimize the fitting parameters by least-square method, and parameters in the table are updated after optimization.

#### Export
LG4X exports fitting results in two different files. One is a text file for fitting conditions, the other is a csv format file for data, which is saved at the same directory of the former file.

#### Add and rem peak
You can add and remove peak at the end of column from the Fit table.

### Drop-down menus

#### Importing data
LG4X imports csv format or tab separated text files. A data file should contain two columns. First column is energy and second column is spectral intensity. LG4X skips first row, because it is typically used for column names. Imported data is displayed in the figure and listed in the file list. You can also open the directory to import all csv and text files in the file list. 

#### File list
Imported file path is added in the list. You can choose the path to import file from the list once you import a data file.

#### Fitting preset
Fitting condition can be created in the BG and Fit tables. From fitting preset drop-down menu, you can generate the most simple single-peak condition from New. If you have a preset previously saved, you can load a preset file, which will be listed in the fitting preset. Default conditions for XPS C1s and C K edge are also available from the list as examples.

#### Background (BG) types
You can choose the type of background to be subtracted from the raw data as listed below. Shirley and Tougaard background iteration functions are available from xpypy.py, which should be located with main.py. From lmfit [built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html), 3rd-order polynomial and 3 step functions are implemented. Fermi-Dirac (ThermalDistributionModel) is used for the Fermi edge fitting, and arctan and error functions (StepModel) for NEXAFS K edge background. Polynomial function is added to the other background models configured in the BG table, so polynomial parameters have to be taken into account for all background optimization. You can turn off polynomial parameters by filling all zeros with turning on checkbox.

| No. | Background | Parameters |
| --- | --- | --- |
| 1 | Shirley BG | Initial, max iteration, # of points for simulation |
| 2 | Tougaard BG | B, C, C', D |
| 3 | Polynomial BG | c0, c1, c2, c3 |
| 4 | Fermi-Dirac BG | amplitude, center, kt |
| 5 | Arctan BG | amplitude, center, sigma |
| 6 | Error BG | amplitude, center, sigma |


### Tables

#### Background configuration table
You can specify the range for fitting region in the first row of BG table. Checkbox works as a constraint at the value beside. Range and polynomial rows are independent from the drop-down menu selection for background.

#### Peak configuration table
All conditions are based on the lmfit [built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html) listed in the Fit table. Peak shapes are listed below. For standard XPS analysis, peak differences and amplitude ratios can be setup from their referenced peak from drop-down menu in each column. The number of peaks can be varied with add and rem buttons. Checkbox can be used for either fixing values or bound conditions if you check beside value. Empty cells do not effect to the optimization.

| No. | String | Peak model | Parameters |
| --- | --- | --- | --- |
| 1 | g | GaussianModel | amplitude, center, sigma |
| 2 | l | LorentzianModel | amplitude, center, sigma |
| 3 | v | VoigtModel | amplitude, center, sigma, gamma |
| 4 | p | PseudoVoigtModel | amplitude, center, sigma, fraction |
| 5 | e | ExponentialGaussianModel | amplitude, center, sigma, gamma |
| 6 | s | SkewedGaussianModel | amplitude, center, sigma, gamma |
| 7 | a | SkewedVoigtModel | amplitude, center, sigma, gamma, skew |
| 8 | b | BreitWignerModel | amplitude, center, sigma, q |
| 9 | n | LognormalModel | amplitude, center, sigma |
| 10 | d | DoniachModel | amplitude, center, sigma, gamma |

##### Amplitude ratio and energy difference
XPS doublet peaks are splitted by the spin-orbit coupling based on the atomic theory. Spin-orbit interaction depends on the atomic element and its orbit. The energy separation of doublet corresponds to the spin-orbit constant. Amplitude ratio of doublet is based on the [multiplicity](https://en.wikipedia.org/wiki/Multiplicity_(chemistry)) (2j+1) of each total angular quantum number (j). LG4X constrains amp ratio and energy diff from a reference peak selected by dropdown menus. For example, Ag3d has j=5/2 and 3/2, and their amp ratio corresponds to 3:2. You can setup second peak amp ratio by selecting the first peak at j=5/2 and amp ratio = 0.67. This means that amplitude of second peak at j=3/2 is constrained by a factor of 0.67 against that of first peak. Energy diff parameter also works in a way that second peak position is away from first peak by the ctr diff = 6 eV as shown in the figure below.

Note that amplitude used in the lmfit package is equivalent to the peak area that is propoertional to the amount of element in analytical area and depth by XPS. The atomic ratio is evaluated by the peak area normalized by the sensitivity factor. The ratio of sensitivity factors on doublet peaks is the same as that in multiplicity, so the normalized peak area of one doublet peak is the same as that in other one.

## Examples

![XPS C1s spectrum](https://github.com/heitler/LG4X/blob/master/Images/Capture.PNG "XPS C1s spectrum")

![XPS Ag3d spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-27%20at%2023.14.49.png "XPS Ag3d spectrum")

![NEXAFS C K edge spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-22%20at%201.45.37.png "NEXAFS C K edge spectrum")

![UPS Fermi-edge spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-21%20at%2020.11.36.png "UPS Fermi-edge spectrum")

![Simulated spectrum](https://github.com/heitler/LG4X/blob/master/Images/Screen%20Shot%202020-05-22%20at%201.15.35.png "Simulated spectrum")







