

# LG4X: lmfit gui for xps

## Introduction

LG4X provides a graphical user interface for XPS curve fitting analysis based on the lmfit package, which provides the non-linear least-square minimization method for Python. LG4X facilitates the curve fitting analysis for python beginners. LG4X was developed on Python 3.6 and PyQt5 was used for its graphical interface design. Shirley and Tougaard iterated methods are implemented as a supplementary code for XPS background subtraction. LG4X tidies up all fitting parameters with their bound conditions in tables. Fitting parameters can be imported and exported as a preset file before and after analysis to streamline the fitting procedures. Fitting results are also exported as a text for parameters and csv file for spectral data. In addition, LG4X simulates the curve without importing data and evaluates the initial parameters over the data plot prior to optimization.


## Methods
### Installation

Download and install [Python 3](https://www.python.org/)

> pip install [lmfit](https://lmfit.github.io/lmfit-py/installation.html)

> pip install pandas

> pip install matplotlib

> pip install PyQt5


Update package if necessary
> pip install --upgrade lmfit

Supplementary code for XPS analysis

xpspy.py should be located at the same directory as main.py for XPS energy range selection for background subtraction in Shirley and Tougaard methods.

Start LG4X
> python main.py

Testing and developing environment

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

* Import csv data
* Setup background and peak parameters with their types
* Evaluate parameters
* Fit curve
* Save parameters as a preset for next analysis
* Export results

## Interface design
### Buttons

#### Importing csv
LG4X imports csv format or tab separated text files. File should contain two columns. First column is energy and second column is spectral intensity. LG4X skips first row, because it is typically used for column names. Imported data is displayed in the figure and listed in the file list.

#### Evaluation
You can evaluate the fitting parameters without fitting optimization on data spectrum. If you have not imported the data, it works for simulation mode in the range you specify.

#### Fit
You can optimize the fitting parameters by least-square method, and parameters in the table are updated after optimization.

#### Export
LG4X exports fitting results in two different files. One is a text file for fitting conditions, the other is a csv format file for data, which is saved at the same directory of the former file.

#### Add and rem peak
You can add and remove peak at the end of column from the Fit table.

### Drop-down menus

#### File list
Imported file path is added in the list. You can choose the path to import file from the list once you import a data file.

#### Fitting preset
Fitting condition can be created in the BG and Fit tables. From fitting preset drop-down menu, you can generate the most simple single-peak condition from New. If you have a preset previously saved, you can load a preset file, which will be listed in the fitting preset. Default conditions for XPS C1s and C K edge are also available from the list as examples.

#### Background (BG) types
You can choose the type of background to be subtracted from the raw data as listed below. Shirley and Tougaard background iteration functions are available from xpypy.py, which should be located with main.py. From lmfit [built-in models](https://lmfit.github.io/lmfit-py/builtin_models.html), 3rd-order polynomial and 5 step functions are implemented. Fermi-Dirac (ThermalDistributionModel) is used for the Fermi edge fitting, and arctan and error functions (StepModel) for NEXAFS K edge. Polynomial function is added to the other background models configured in the BG table.

| No. | Background | Parameters |
| --- | --- | --- |
| 1 | Shirley BG | Initial, max iteration |
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

| No. | String | Model | Parameters |
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

## Examples

![XPS C1s spectrum](https://github.com/heitler/LG4X/blob/master/Images/Capture.PNG "C1s")

### NEXAFS C K edge spectrum

### UPS Fermi-edge spectrum









