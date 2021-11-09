Name:           p4-bmv2
Summary:        P4 reference switch
Version:        1.14.0
Release:        1%{?dist}
License:        ASL 2.0
ExclusiveArch:  x86_64
URL:            https://p4.org/
Source0:        https://github.com/p4lang/behavioral-model/archive/refs/tags/%{version}.tar.gz
# change explict paths to third_party/libfoo.a to -lfoo
Patch1:         bmv2-no-third-party.patch

BuildRequires:  autoconf automake
BuildRequires:  boost-devel
BuildRequires:  gcc-c++ gmp-devel
BuildRequires:  Judy-devel json-c-devel
BuildRequires:  libpcap-devel libtool
BuildRequires:  nanomsg-devel

Requires:       boost
Requires:       gmp
Requires:       Judy json-c
Requires:       libpcap
Requires:       nanomsg

%description
This is the second version of the reference P4 software switch,
nicknamed bmv2 (for behavioral model version 2). The software
switch is written in C++11. It takes as input a JSON file
generated from your P4 program by a P4 compiler and interprets
it to implement the packet-processing behavior specified by
that P4 program.

%package devel
Summary: P4 BMv2 reference switch

%description devel
This is the second version of the reference P4 software switch,
nicknamed bmv2 (for behavioral model version 2). The software
switch is written in C++11. It takes as input a JSON file
generated from your P4 program by a P4 compiler and interprets
it to implement the packet-processing behavior specified by
that P4 program.

%prep
%setup -q -c -n %{name}-%{version}
# Remove all the third_party src
rm -rf %{name}-%{version}/behavioral-model-%{version}/third_party
# Fixup makefiles from third_party removal, use normal libs
%patch1 -p1

%build
cd behavioral-model-%{version}
./autogen.sh
mkdir build
cd build
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-static \
    --without-thrift

make %{?_smp_mflags} 

%install
cd behavioral-model-%{version}/build
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir}

%files devel
%{_bindir}/bm_*
%dir %{_includedir}/bm
%{_includedir}/bm/*
%{_libdir}/*

%exclude   /usr/lib/python2.7/site-packages/nanomsg_client.py
%exclude   /usr/lib/python2.7/site-packages/nanomsg_client.pyc
%exclude   /usr/lib/python2.7/site-packages/nanomsg_client.pyo
%exclude   /usr/lib/python2.7/site-packages/p4dbg.py
%exclude   /usr/lib/python2.7/site-packages/p4dbg.pyc
%exclude   /usr/lib/python2.7/site-packages/p4dbg.pyo
   
#%{_python2_sitelib}/nanomsg_client.py*
#%{_python2_sitelib}/p4dbg.py*


%changelog
* Wed Nov 3 2021 <trix@redhat.com> - 1.2.2-1
- Initial release




