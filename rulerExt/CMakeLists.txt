cmake_minimum_required(VERSION 2.8.9)

project(rulerExt)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/rulerExt")
set(EXTENSION_CATEGORY "extension")
set(EXTENSION_CONTRIBUTORS "UMich students (University of Michigan)")
set(EXTENSION_DESCRIPTION "This extension calculates ruler data")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/rulerExt.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/rulerExt/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(rulerLength)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
