# CMake entry point
cmake_minimum_required (VERSION 2.8)
project ("openGLES 2.0 for Raspberry Pi tutorials")

SET(PROJECT_HOME /home/christian/projects/pilotage-fpv)

SET(COMPILE_DEFINITIONS -Werror)

# this one is important
SET(CMAKE_SYSTEM_NAME Linux)
#this one not so much
SET(CMAKE_SYSTEM_VERSION 1)

# specify the cross compiler
SET(CMAKE_C_COMPILER   ${PROJECT_HOME}/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin/arm-linux-gnueabihf-gcc)
SET(CMAKE_CXX_COMPILER ${PROJECT_HOME}/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin/arm-linux-gnueabihf-g++)

# where is the target environment 
SET(CMAKE_FIND_ROOT_PATH  ${PROJECT_HOME}/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian)

# search for programs in the build host directories
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# for libraries and headers in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

include_directories(
    ${PROJECT_HOME}/tools/vc/include
    ${PROJECT_HOME}/tools/vc/include/interface/vcos/pthreads
    ${PROJECT_HOME}/tools/vc/include/interface/vmcs_host/linux
    ${PROJECT_HOME}/tools/vc/userland
    ${PROJECT_HOME}/tools/vc/userland/interface/vcos
    ${PROJECT_HOME}/tools/vc/userland/interface/vcos/pthreads
    ${PROJECT_HOME}/tools/vc/userland/interface/vmcs_host/linux
    ${PROJECT_HOME}/tools/vc/userland/host_applications/linux/libs/bcm_host/include
    ${PROJECT_HOME}/tools/vc/userland/interface/vmcs_host/khronos/
    ${PROJECT_HOME}/tools/vc/userland/interface/khronos/include	
    ../libs/ilclient
    .
)

set(RPi_LIBS
# Raspberry Pi - Broadcom
    libbcm_host.so
    libvcos.so
)

set(CAM_LIBS
# camera
    libmmal_core.so
    libmmal_util.so
    libmmal_vc_client.so
)

set(GL_LIBS
# openGLES
    GLESv2
    EGL
)

set(ILC_LIBS
# ilclient
    ilclient
    openmaxil
)

link_directories(../libs/ilclient ${PROJECT_HOME}/tools/vc/lib)

# OSD
add_executable(../osd/osd
    osd/osd_paint.cpp
    osd/Drawable.cpp
    osd/Vertex.cpp
    osd/Shape.cpp
    osd/Triangle.cpp
    osd/Rectangle.cpp
    common/startScreen.cpp
    common/LoadShaders.cpp
    common/LoadShaders.h
)
target_link_libraries(../osd/osd
    ${RPi_LIBS}
    ${GL_LIBS}
)


# Tutorial 1
add_executable(../tutorial01_first_screen/tutorial01_first_screen
    tutorial01_first_screen/tutorial01.cpp
    common/startScreen.cpp
)
target_link_libraries(../tutorial01_first_screen/tutorial01_first_screen
        ${RPi_LIBS}
        ${GL_LIBS}
)

# playground
add_executable(../playground/playground
    playground/playground.cpp
    common/startScreen.cpp
)
target_link_libraries(../playground/playground
        ${RPi_LIBS}
        ${GL_LIBS}
)


# Tutorial 2
add_executable(../tutorial02_red_triangle/tutorial02_red_triangle
    tutorial02_red_triangle/tutorial02.cpp
    common/startScreen.cpp
    common/LoadShaders.cpp
    common/LoadShaders.h
)
target_link_libraries(../tutorial02_red_triangle/tutorial02_red_triangle
        ${RPi_LIBS}
        ${GL_LIBS}
)

# Tutorial 2a
add_executable(../tutorial02a_modelspace/tutorial02a_modelspace
    tutorial02a_modelspace/tutorial02a.cpp
    common/startScreen.cpp
    common/LoadShaders.cpp
    common/LoadShaders.h
)
target_link_libraries(../tutorial02a_modelspace/tutorial02a_modelspace
        ${RPi_LIBS}
        ${GL_LIBS}
)

set (CMAKE_C_FLAGS "-DOMX_SKIP64BIT")

