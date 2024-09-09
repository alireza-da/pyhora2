#  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  #
#  PyHora - Based on the book Vedic Astrology - An Integrated Approach, PVR Narasimha Rao        #
#  Copyright © 2022 Sundar Sundaresan <Sundaram.Sundaresan@gmail.com>.                           #
#                                                                                                #
#  This program is free software: you can redistribute it and/or modify it under the terms of    #
#  the GNU General Public License as published by the Free Software Foundation, either version   #
#  3 of the License, or (at your option) any later version.                                      #
#                                                                                                #
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;     #
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.     #
#  See the GNU General Public License for more details.                                          #
#  																								 #
#  Vedic Astrology was givem to us by our ancient sages without any commerical benefits.         #
#  Let us also do the same without any commercial benfits and distribute this free. THANK YOU    #
#  You should have received a copy of the GNU General Public License along with this program.    #
#  If not, see <http://www.gnu.org/licenses/>.                                                   #
#  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  #

name = "pyhora2"

version = "3.6.2"

author = "Alireza Davoodi"

author_email = "alirezadavoodi1378@gmail.com"

description = "A Python package for generating Indian style calendar, panchang, horoscope and compatibility. Advanced, clean, and well-packaged version of PyHora"

url = "https://github.com/naturalstupid/pyhora"

project_urls = {
    "Source Code": "https://github.com/alireza-da/pyhora2",
    "Documentation": "https://github.com/alireza-da/pyhora2",
}

install_requires = ['pyswisseph','geopy','pytz','PyQt6','img2pdf','geocoder','timezonefinder',
                    'pandas', 'numpy', 'pillow', 'requests']

#extras_require = { }

package_data = {
    '': ["*"]
}

classifiers = [
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
