# QF-Test imagecheck [![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)

This is a custom image comparator built on top of (or rather next to) existing `QF-Test` procedures and objects.  

Even though `QF-Test` standard library contains some procedures for image comparison, it is not possible to exclude (ignore) image regions during the process. That was the main motivation to create this procedure.  

`java` objects are used for loading into and comparing RGB arrays. This way the comparison is much faster than using `python` objects (execution time for 1024x768 px images is usually less than 1 second).

## Description
* SUT screen is compared against saved image template.  
* Images are compared pixel-by-pixel.  
* It is possible to define image subregions that are ignored during the comparison (e.g. datetime regions).  
* In case some differences are found, error is logged in the runlog together with graphical comparison of both images (`rc.checkImage` is used).
