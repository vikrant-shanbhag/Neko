# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10

# Utility rule file for pch_Generate_opencv_test_ocl.

# Include the progress variables for this target.
include modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/progress.make

modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl: modules/ocl/test_precomp.hpp.gch/opencv_test_ocl_RELEASE.gch

modules/ocl/test_precomp.hpp.gch/opencv_test_ocl_RELEASE.gch: modules/ocl/test/test_precomp.hpp
modules/ocl/test_precomp.hpp.gch/opencv_test_ocl_RELEASE.gch: modules/ocl/test_precomp.hpp
modules/ocl/test_precomp.hpp.gch/opencv_test_ocl_RELEASE.gch: lib/libopencv_test_ocl_pch_dephelp.a
	$(CMAKE_COMMAND) -E cmake_progress_report /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating test_precomp.hpp.gch/opencv_test_ocl_RELEASE.gch"
	cd /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl && /usr/bin/cmake -E make_directory /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/test_precomp.hpp.gch
	cd /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl && /usr/lib64/ccache/c++ -O3 -DNDEBUG -DNDEBUG -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/test" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/video/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/features2d/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/highgui/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/imgproc/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/flann/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/core/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/highgui/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ts/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/video/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/objdetect/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ml/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/calib3d/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/features2d/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/highgui/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/imgproc/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/flann/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/core/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/src" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/include" -isystem"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/3rdparty/include/opencl/1.2" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/video/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/objdetect/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ml/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/calib3d/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/features2d/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/highgui/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/imgproc/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/flann/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/core/include" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/src" -I"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/include" -isystem"/home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10" -isystem"/usr/include/eigen3" -fsigned-char -W -Wall -Werror=return-type -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wno-narrowing -Wno-delete-non-virtual-dtor -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -msse -msse2 -msse3 -ffunction-sections -x c++-header -o /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/test_precomp.hpp.gch/opencv_test_ocl_RELEASE.gch /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/test_precomp.hpp

modules/ocl/test_precomp.hpp: modules/ocl/test/test_precomp.hpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating test_precomp.hpp"
	cd /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl && /usr/bin/cmake -E copy /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/test/test_precomp.hpp /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/test_precomp.hpp

pch_Generate_opencv_test_ocl: modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl
pch_Generate_opencv_test_ocl: modules/ocl/test_precomp.hpp.gch/opencv_test_ocl_RELEASE.gch
pch_Generate_opencv_test_ocl: modules/ocl/test_precomp.hpp
pch_Generate_opencv_test_ocl: modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/build.make
.PHONY : pch_Generate_opencv_test_ocl

# Rule to build all files generated by this target.
modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/build: pch_Generate_opencv_test_ocl
.PHONY : modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/build

modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/clean:
	cd /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl && $(CMAKE_COMMAND) -P CMakeFiles/pch_Generate_opencv_test_ocl.dir/cmake_clean.cmake
.PHONY : modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/clean

modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/depend:
	cd /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10 /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10 /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl /home/andrew/Projects/computer_vision/car_detection/Neko/haarTraining/src/opencv-2.4.10/modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/ocl/CMakeFiles/pch_Generate_opencv_test_ocl.dir/depend

