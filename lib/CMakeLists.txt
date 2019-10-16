# Copyright 2011,2012,2016 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})

list(APPEND Mercurial_SDR_sources
)

set(Mercurial_SDR_sources "${Mercurial_SDR_sources}" PARENT_SCOPE)
if(NOT Mercurial_SDR_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT Mercurial_SDR_sources)

add_library(gnuradio-Mercurial_SDR SHARED ${Mercurial_SDR_sources})
target_link_libraries(gnuradio-Mercurial_SDR ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-Mercurial_SDR PROPERTIES DEFINE_SYMBOL "gnuradio_Mercurial_SDR_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-Mercurial_SDR PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-Mercurial_SDR RUNTIME_COMPONENT "Mercurial_SDR_runtime" DEVEL_COMPONENT "Mercurial_SDR_devel")

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_Mercurial_SDR_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_Mercurial_SDR.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_Mercurial_SDR.cc
)

add_executable(test-Mercurial_SDR ${test_Mercurial_SDR_sources})

target_link_libraries(
  test-Mercurial_SDR
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  gnuradio-Mercurial_SDR
)

GR_ADD_TEST(test_Mercurial_SDR test-Mercurial_SDR)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")

