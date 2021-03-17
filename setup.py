import setuptools

setuptools.setup(
    name='eryx_dash',
    version='0.0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pandas', 'dash', 'dash-bootstrap-components', 'millify'],
    python_requires='>=3.6',
    zip_safe=False
)
