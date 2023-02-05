Semantic Versioning
===================
_Applies to Releases Only_

Semantic Versioning (SemVer) is a widely used standard for software versioning. It provides a simple and consistent method for versioning software projects and helps communicate version changes to stakeholders.

SemVer consists of three parts:

**Major version number:** This number changes when there are breaking changes to the software. Breaking changes are any changes that would require existing software to be modified or upgraded to work with the new version.

**Minor version number:** This number changes when new features are added to the software. The features are non-breaking and should not impact existing functionality.

**Patch version number:** This number changes when bug fixes are made to the software. These changes should not affect the functionality of the software.

SemVer uses the format of **Major.Minor. Patch.** For example, **2.0.0 or 1.1.3.**



Automated Regolith Sintering Stand
This repository contains the code responsible for controlling an automated regolith sintering stand. The stand is used to sinter regolith, which is a mixture of solid particles that form the surface of a planet or a moon, into solid structures.

Requirements
Python 3.6 or higher
NumPy 1.16 or higher
PySerial 3.4 or higher
Getting Started
Clone this repository to your local machine using git clone https://github.com/<username>/regolith-sintering-stand.git.
Install the required packages using pip install -r requirements.txt.
Connect the regolith sintering stand to your computer using a serial cable.
Run the code using python sintering_stand_controller.py to start controlling the stand.
Usage
The code provides a command-line interface that allows you to control the regolith sintering stand. The following commands are available:

start: start the sintering process
stop: stop the sintering process
status: display the current status of the sintering process
exit: exit the program
Contributions
Contributions are welcome. If you find a bug or have an idea for a new feature, please open an issue or a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
