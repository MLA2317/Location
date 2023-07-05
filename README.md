# Location

1. pip install pipwin
2. pipwin install refresh
3. pipwin install gdal
4. append to setting INSTALLED_APP - 'django.contrib.gis'
5. append to setting GDAL_LIBRARY_PATH = r'C:\Users\user\Desktop\Location Api\venv\Lib\site-packages\osgeo\gdal304.dll'
6. install Postgres and PostGis program
7. Create Postgres database
8. append to setting DATABASE -  'ENGINE': 'django.contrib.gis.db.backends.postgis',
