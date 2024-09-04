PyHora 3.5.0
=================
Python package containing almost all the features described in the book

Vedic Astrology - An Integrated Approach - by PVR Narasimha Rao
 
Observational Indian lunisolar calendar, horoscope and matching using the Swiss ephemeris (Hindu
Drig-ganita Panchanga).

Installation
=================
```pip install pyhora2```

Features
--------
See - package_structure.md for package structure

Using the GUI
-------------

Enter Name, and Place with country name (e.g. Chennai, IN)
If you get an error, enter latitude, longitude and time zone manually.
If you want to be precise, enter the lat/long of the exact place (e.g. hospital)
You can use google to find the latitude, longitude, time zone of the place

Type the Date in YYY,MM,DD format in the 'Date' field. Negative value for YYYY are
interpolated as proleptic Gregorian calendar (Before Christ BC).

Enter Time of birth, choose chart style, ayanamsa mode, language of display

Click Show Chart to display the birth (Raasi and Navamsam) charts

Click Show PDF to save the screen as a PDF file

Using the Code / command line
------------------------------
```
import horo_chart, panchanga, horoscope
App = QApplication(sys.argv)
chart_type = 'North'
chart = horo_chart.ChartSimple(chart_type=chart_type)
chart.language('Tamil')
chart.name('Krishna')
chart.place('Mathura,IN')
chart.date_of_birth('-3229,6,17')
chart.time_of_birth('23:59:00')
chart.time_zone('5.5')
chart.chart_type(chart_type)
chart.compute_horoscope()
chart.minimum_compatibility_score(20.0)
chart.mahendra_porutham(False)
chart.vedha_porutham(False)
chart.rajju_porutham(False)
chart.sthree_dheerga_porutham(False)
chart.show()
chart.save_as_pdf('delme.pdf')
```
Accuracy
--------

The program is as accurate as the Swiss Ephemeris installed on your system. So generally it is
accurate for years 13000 BCE to 16800 CE. The
computational speed stays the same no matter which date you enter. Required swiss ephimeres files are also /ephe/ folder of this repository.
Overall size of these files is more than 100 MB. To reduce your application size, you can restrict the dates within a range and could remove those ephimeres files from the folder.

Personal Opinion:
------------------
When using BC dates (such as mahabharatha dates) it is advised to use `SURYA_SIDHANTHA` or `SUNDAR_SS` as ayanamsa styles, as ayanamsa values of every other ayanamsa types such as `LAHIRI, KP` etc are inaccurate. 
`SUNDAR_SS` is a sine curve forcing zero ayanamsa every 3200 years from -3101 BCE and 27 degrees as peak ayanamsa.

API Documents
-------------
API are in README.md of respective folders. HTML links are provided here below: 

License
-------
See LICENSE file.
