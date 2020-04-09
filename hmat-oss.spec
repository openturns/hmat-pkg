# norootforbuild

%define __cmake %{_bindir}/cmake
%define _cmake_lib_suffix64 -DLIB_SUFFIX=64
%define cmake \
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
%__cmake \\\
-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \\\
%if "%{?_lib}" == "lib64" \
%{?_cmake_lib_suffix64} \\\
%endif \
-DBUILD_SHARED_LIBS:BOOL=ON

Name:           hmat-oss 
Version:        1.6.1
Release:        1%{?dist}
Summary:        A hierarchical matrix C/C++ library
Group:          System Environment/Libraries
License:        GPL2
URL:            https://github.com/jeromerobert/hmat-oss
Source0:        https://github.com/jeromerobert/hmat-oss/archive/%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  gcc-c++, cmake
BuildRequires:  lapack-devel
%if 0%{?suse_version}
BuildRequires:  cblas-devel
%endif
%if 0%{?centos_version} || 0%{?fedora_version}
BuildRequires:  atlas-devel
%endif
Requires:       libhmat-oss1

%description
A hierarchical matrix C/C++ library including a LU solver.

%package -n libhmat-oss1
Summary:        A hierarchical matrix C/C++ library 
Group:          Development/Libraries/C and C++
%if 0%{?mageia}
Requires:       lib64lapack3
%else
Requires:       lapack
%endif
%if 0%{?suse_version}
Requires:       cblas
%endif
%if 0%{?centos_version} || 0%{?fedora_version}
Requires:       atlas
%endif

%description -n libhmat-oss1
A hierarchical matrix C/C++ library (binaries) 

%package devel
Summary:        A hierarchical matrix C/C++ library 
Group:          Development/Libraries/C and C++
Requires:       libhmat-oss1 = %{version}
Requires:       lapack-devel

%description devel
A hierarchical matrix C/C++ library (development files)

%prep
%setup -q

%build
%if 0%{?suse_version}
%cmake -DCBLAS_LIBRARIES="cblas;blas" -DBUILD_EXAMPLES=ON .
%else
%cmake -DCBLAS_cblas_INCLUDE=/usr/include/cblas -DBUILD_EXAMPLES=ON .
%endif
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -n libhmat-oss1 -p /sbin/ldconfig 
%postun -n libhmat-oss1 -p /sbin/ldconfig  

%files -n libhmat-oss1
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/hmat/
%{_includedir}/hmat/*.h
%{_includedir}/*.hpp
%{_libdir}/*.so
%dir %{_libdir}/cmake/hmat/
%{_libdir}/cmake/hmat/*.cmake

%changelog
* Sat Nov 22 2014 Julien Schueller <schueller at phimeca dot com> 1.0-1
- Initial package creation
