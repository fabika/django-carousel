from setuptools import setup, find_packages

setup(
    name='django-carousel',
    version=__import__('carousel').__version__,
    description='Helpers to generate dynamic carousels.',
    author='Fabika Team',
    author_email='it@gmail.com',
    url='http://github.com/fabika/django-carousel',
    download_url='http://github.com/fabika/django-carousel/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
