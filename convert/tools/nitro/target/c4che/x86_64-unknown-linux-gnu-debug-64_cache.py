APPNAME = 'nitro'
AR = '/usr/bin/ar'
ARFLAGS = 'rcs'
BINDIR = '/home/andrew/.virtualenvs/cardet/bin'
BUILD_PACKAGES = {}
CC = ['/usr/lib64/ccache/gcc']
CCLNK_SRC_F = []
CCLNK_TGT_F = ['-o']
CC_NAME = 'gcc'
CC_SRC_F = []
CC_TGT_F = ['-c', '-o']
CC_VERSION = ('4', '8', '2')
CFLAGS = ['-fPIC', '-Wall', '-g', '-m64']
CFLAGS_LIBJPEG = []
CFLAGS_MACBUNDLE = ['-fPIC']
CFLAGS_PYEMBED = ['-fno-strict-aliasing', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fno-strict-aliasing']
CFLAGS_PYEXT = ['-pthread', '-fno-strict-aliasing', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fno-strict-aliasing']
CFLAGS_THREAD = ['-D_REENTRANT']
CFLAGS_cshlib = ['-fPIC']
COMPILER_CC = 'gcc'
COMPILER_CXX = 'g++'
CPPPATH_ST = '-I%s'
CXX = ['/usr/lib64/ccache/g++']
CXXFLAGS = ['-fPIC', '-Wall', '-g', '-m64']
CXXFLAGS_MACBUNDLE = ['-fPIC']
CXXFLAGS_PYEMBED = ['-fno-strict-aliasing', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fno-strict-aliasing']
CXXFLAGS_PYEXT = ['-pthread', '-fno-strict-aliasing', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fexceptions', '-fstack-protector', '-m64', '-mtune=generic', '-fPIC', '-fwrapv', '-fno-strict-aliasing']
CXXFLAGS_THREAD = ['-D_REENTRANT']
CXXFLAGS_cxxshlib = ['-fPIC']
CXXLNK_SRC_F = []
CXXLNK_TGT_F = ['-o']
CXX_NAME = 'gcc'
CXX_SRC_F = []
CXX_TGT_F = ['-c', '-o']
DEFINES = ['HAVE_INTTYPES_H=1', 'HAVE_UNISTD_H=1', 'HAVE_GETOPT_H=1', 'HAVE_MALLOC_H=1', 'HAVE_SYS_TIME_H=1', 'HAVE_DLFCN_H=1', 'HAVE_FCNTL_H=1', 'HAVE_MEMORY_H=1', 'HAVE_STRING_H=1', 'HAVE_STRINGS_H=1', 'HAVE_STDBOOL_H=1', 'HAVE_STDLIB_H=1', 'HAVE_STDDEF_H=1', 'HAVE_LOCALTIME_R=1', 'HAVE_GMTIME_R=1', 'HAVE_MMAP=1', 'HAVE_MEMMOVE=1', 'HAVE_STRERROR=1', 'HAVE_BCOPY=1', 'HAVE_SIZE_T=1', 'HAVE_CONST=1', 'HAVE_UNSIGNED_SHORT=1', 'HAVE_UNSIGNED_CHAR=1', 'HAVE_ERF=1', 'HAVE_ERFF=1', 'HAVE_GETTIMEOFDAY=1', 'HAVE_CLOCK_GETTIME=1', 'USE_CLOCK_GETTIME', 'HAVE_GETPAGESIZE=1', 'HAVE_GETOPT=1', 'HAVE_GETOPT_LONG=1', 'HAVE_ISNAN=1', 'SIZEOF_LONG_LONG=8', 'SIZEOF_LONG=8', 'BIGENDIAN=0', 'SIZEOF_DOUBLE=8', 'SIZEOF_SHORT=2', 'SIZEOF_INT=4', 'SIZEOF_FLOAT=4', '_FILE_OFFSET_BITS=64', '_LARGEFILE_SOURCE', '__POSIX', 'PYTHONDIR="/home/andrew/.virtualenvs/cardet/lib/python2.7/site-packages"', 'PYTHONARCHDIR="/home/andrew/.virtualenvs/cardet/lib64/python2.7/site-packages"', 'HAVE_PYTHON_H=1']
DEFINES_PYEMBED = ['_GNU_SOURCE', 'NDEBUG', '_GNU_SOURCE']
DEFINES_PYEXT = ['_GNU_SOURCE', 'NDEBUG', '_GNU_SOURCE']
DEFINES_ST = '-D%s'
DELIVER_SOURCE = False
DEST_BINFMT = 'elf'
DEST_CPU = 'x86_64'
DEST_OS = 'linux'
DETECTED_BUILD_PY = True
HAVE_ANT = None
INCLUDES_PYEMBED = ['/usr/include/python2.7']
INCLUDES_PYEXT = ['/usr/include/python2.7']
INCLUDES_UNITTEST = ['/home/andrew/Projects/computer_vision/car_detection/Neko/convert/tools/nitro/c++/include']
IS64BIT = True
LIBDIR = '/home/andrew/.virtualenvs/cardet/lib'
LIBPATH_PYEMBED = ['/usr/lib64']
LIBPATH_PYEXT = ['/usr/lib64']
LIBPATH_PYTHON2.7 = ['/usr/lib64']
LIBPATH_ST = '-L%s'
LIB_CLOCK_GETTIME = ['rt']
LIB_DL = ['dl']
LIB_MATH = ['m', 'm']
LIB_NSL = ['nsl']
LIB_PTHREAD = ['pthread']
LIB_PYEMBED = ['python2.7']
LIB_PYEXT = ['python2.7']
LIB_PYTHON2.7 = ['python2.7']
LIB_RT = ['rt']
LIB_ST = '-l%s'
LIB_THREAD = ['pthread']
LIB_TYPE = 'stlib'
LINKFLAGS = ['-Wl,-E', '-fPIC', '-m64']
LINKFLAGS_MACBUNDLE = ['-bundle', '-undefined', 'dynamic_lookup']
LINKFLAGS_PYEMBED = ['-Wl,-z,relro']
LINKFLAGS_PYEXT = ['-Wl,-z,relro', '-pthread', '-Wl,-z,relro']
LINKFLAGS_cshlib = ['-shared']
LINKFLAGS_cstlib = ['-Wl,-Bstatic']
LINKFLAGS_cxxshlib = ['-shared']
LINKFLAGS_cxxstlib = ['-Wl,-Bstatic']
LINK_CC = ['/usr/lib64/ccache/gcc']
LINK_CXX = ['/usr/lib64/ccache/g++']
PLATFORM = 'x86_64-unknown-linux-gnu'
PREFIX = '/home/andrew/.virtualenvs/cardet'
PYC = 1
PYCMD = '"import sys, py_compile;py_compile.compile(sys.argv[1], sys.argv[2])"'
PYFLAGS = ''
PYFLAGS_OPT = '-O'
PYO = 1
PYTHON = ['/home/andrew/.virtualenvs/cardet/bin/python']
PYTHONARCHDIR = '/home/andrew/.virtualenvs/cardet/lib64/python2.7/site-packages'
PYTHONDIR = '/home/andrew/.virtualenvs/cardet/lib/python2.7/site-packages'
PYTHON_CONFIG = '/usr/bin/python2.7-config'
PYTHON_VERSION = '2.7'
RPATH_ST = '-Wl,-rpath,%s'
SHLIB_MARKER = '-Wl,-Bdynamic'
SONAME_ST = '-Wl,-h,%s'
STLIBPATH_ST = '-L%s'
STLIB_MARKER = '-Wl,-Bstatic'
STLIB_ST = '-l%s'
VARIANT = 'x86_64-unknown-linux-gnu-debug-64'
VERSION = '2.7'
cprogram_PATTERN = '%s'
cshlib_PATTERN = 'lib%s.so'
cstlib_PATTERN = 'lib%s.a'
cxxprogram_PATTERN = '%s'
cxxshlib_PATTERN = 'lib%s.so'
cxxstlib_PATTERN = 'lib%s.a'
define_key = ['HAVE_INTTYPES_H', 'HAVE_UNISTD_H', 'HAVE_GETOPT_H', 'HAVE_MALLOC_H', 'HAVE_SYS_TIME_H', 'HAVE_DLFCN_H', 'HAVE_FCNTL_H', 'HAVE_CHECK_H', 'HAVE_MEMORY_H', 'HAVE_STRING_H', 'HAVE_STRINGS_H', 'HAVE_STDBOOL_H', 'HAVE_STDLIB_H', 'HAVE_STDDEF_H', 'HAVE_LOCALTIME_R', 'HAVE_GMTIME_R', 'HAVE_MMAP', 'HAVE_MEMMOVE', 'HAVE_STRERROR', 'HAVE_BCOPY', 'HAVE_SIZE_T', 'HAVE_CONST', 'HAVE_UNSIGNED_SHORT', 'HAVE_UNSIGNED_CHAR', 'HAVE_ERF', 'HAVE_ERFF', 'HAVE_GETTIMEOFDAY', 'HAVE_CLOCK_GETTIME', 'HAVE_BSDGETTIMEOFDAY', 'HAVE_GETHRTIME', 'HAVE_GETPAGESIZE', 'HAVE_GETOPT', 'HAVE_GETOPT_LONG', 'HAVE_ISNAN', 'HAVE_HRTIME_T', 'SIZEOF_LONG_LONG', 'SIZEOF_LONG', 'BIGENDIAN', 'SIZEOF_DOUBLE', 'SIZEOF_SHORT', 'SIZEOF_INT', 'SIZEOF_FLOAT', 'PYTHONDIR', 'PYTHONARCHDIR', 'HAVE_PYTHON_H']
install_headers = True
install_libs = True
install_source = False
macbundle_PATTERN = '%s.bundle'
pyext_PATTERN = '%s.so'
