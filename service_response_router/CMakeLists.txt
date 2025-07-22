cmake_minimum_required(VERSION 3.20)
project(ServiceResponseRouter)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(unofficial-uwebsockets CONFIG REQUIRED)

add_executable(server main.cc)
target_link_libraries(server PRIVATE unofficial::uwebsockets::uwebsockets)