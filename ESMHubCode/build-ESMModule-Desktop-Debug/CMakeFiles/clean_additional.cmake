# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\ESMModule_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\ESMModule_autogen.dir\\ParseCache.txt"
  "ESMModule_autogen"
  )
endif()
