# Vessel-Involvement-Quantifier

# Installation and Setup

The VesselInvolvementQuantifier has been tested on MacOS (Monterey, Version 12.6) and Windows 11. We do not provide support for other operating systems.

The VesselInvolvementQuantifier does not require a GPU. 

We very strongly recommend you install the VesselInvolvementQuantifier in a virtual environment.

Python 2 is deprecated and not supported. Please make sure you are using Python 3.

For more information about the VesselInvolvementQuantifier, please read the following paper:

TODO: add citation here

Please also cite this paper if you are using the VesselInvolvementQuantifier for your research!

Follow these steps to run the VesselInvolvementQuantifier:

1. Install the VesselInvolvementQuantifier
```
 git clone https://github.com/PHAIR-Amsterdam/Vessel-Involvement-Quantifier.git
 cd Vessel-Involvement-Quantifier
 pip install -e .
```
2. The VesselInvolvementQuantifier needs to know which vessel segments to analyze and which degree and resectability categories to use. For this you need to set a variables in ```settings.py``` :

    2.1 Save the key file (xlsx) in the ```Vessel-Involvement-Quantifier``` folder. The key file has the name ```db_vessels.xlsx``` and contains the patient identifiers (column numbber) and the ground truth involement classifcations for each vessel segment you intend to analayze.

    2.2 Save the segmentation masks you intend to analyze in the ```Vessel-Involvement-Quantifier/test_data``` folder. The filenames must contain the patient identifier used in your key file. The file must be of type **.nii.gz** or **.nrrd*.
    
    2.3 Set the vessel segment names as used in the column headers of your key file in ```settings.py``` under ```vessels```. Set the segment index in you segmentation mask under ```vessels_id```. 

    2.4 Set the degree classifcations provided by your radiologist under in ```settings.py``` under ```degrees_id```. 

    2.5 Set the resectability classifcations provided by your radiologist under in ```settings.py``` under ```resectability_id```. 
    

```
VesselInvolvementQuantifier
├── test_data
│   └── patient1.nrrd
│   └── patient2.nrrd
├── db_vessels.xlsx
├── main.py
├── settings.py
├── plot.py
├── quantify.py
├── utils.py

```

# Analyzing
 
After following the instruction under Installation (2) to store your test data and key file, run the function ```main.py```. The VesselInvolvementQuantifier will store results in ```results.csv``` and will create a boxplot under the name ```boxplot.png```.
