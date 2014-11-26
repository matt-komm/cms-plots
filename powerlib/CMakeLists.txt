project(PowerLib)
cmake_minimum_required(VERSION 2.6)
set(CMAKE_MODULE_PATH  "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_MODULE_PATH}")
include_directories(${PROJECT_SOURCE_DIR})
include_directories(${PROJECT_BINARY_DIR})
find_package(ROOT)
include(FindFreetype)
#cmake_policy(SET CMP0015 NEW)
include_directories(${ROOT_INCLUDE_DIR} ${FREETYPE_INCLUDE_DIRS})
link_directories(${ROOT_LIBDIR})

set(CLASSHEADERS 
    Projector.hpp
    FontMetrics.hpp
)
set_source_files_properties(${PROJECT_BINARY_DIR}/dict.C PROPERTIES GENERATED TRUE)
add_custom_target(generatedicts ALL ${ROOTCINT_EXECUTABLE} 
    -f ${PROJECT_BINARY_DIR}/dict.C 
    -c ${CLASSHEADERS} LinkDef.h 
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(powerlib MODULE 
    Projector.cpp 
    FontMetrics.cpp
    dict.C
)
target_link_libraries(powerlib Core Tree TreePlayer graph freetype)
add_dependencies(powerlib generatedicts)
