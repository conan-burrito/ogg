cmake_minimum_required(VERSION 3.6)
project(PackageTest VERSION 1.0.0 LANGUAGES C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(Ogg REQUIRED CONFIG)

add_executable(example example.c)
target_link_libraries(example Ogg::ogg)
set_target_properties(example PROPERTIES OUTPUT_NAME "test")
