cmake_minimum_required(VERSION 3.15)
project(llama_cpp_tests)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add llama.cpp source tree as subdir to get the llama target
add_subdirectory(/home/saksham/llama.cpp llama_build)

add_executable(model_load_test model_load_test.cc)

target_link_libraries(model_load_test PRIVATE llama)

