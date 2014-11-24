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
Version:        1.0
Release:        1%{?dist}
Summary:        A hierarchical matrix C/C++ library
Group:          System Environment/Libraries
License:        GPL
URL:            https://github.com/jeromerobert/hmat-oss
Source0:        https://github.com/jeromerobert/hmat-oss/archive/%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  gcc-c++, cmake
%if 0%{?suse_version}
BuildRequires:  lapack
BuildRequires:  atlas
%else
BuildRequires:  lapack-devel
BuildRequires:  atlas-devel
%endif
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif

%description
A hierarchical matrix C/C++ library including a LU solver.

%package libs
Summary:        Uncertainty treatment library
Group:          Development/Libraries/C and C++
Requires:       lapack
Requires:       atlas

%description libs
HMat library binaries 

%package devel
Summary:        OpenTURNS development files
Group:          Development/Libraries/C and C++
Requires:       %{name}-libs = %{version}
%if ! 0%{?suse_version}
Requires:       lapack-devel
%endif

%description devel
Development files for HMat 

%prep
%setup -q

%build
%cmake -DCBLAS_LIBRARIES=`find /usr/lib* -name libcblas.so`
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig 
%postun libs -p /sbin/ldconfig  

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/%{name}
%{_libdir}/*.so.*
%dir %{_datadir}/%{name}
%dir %{_libdir}/%{name}

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/hmat
%{_includedir}/hmat/*.h
%{_includedir}/*.hpp
%{_datadir}/hmat/
%{_libdir}/*.so


%changelog
* Sat Nov 22 2014 Julien Schueller <schueller at phimeca dot com> 1.0-1
- Initial package creation
