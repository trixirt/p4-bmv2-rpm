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
# cleanup version string
Patch2:         0001-Remove-unknown-prefix-from-version-if-.git-is-not-fo.patch
# Fix rpmlint *.so version error
Patch3:         0002-Start-versioning-.so-s.patch
# python2 -> python3
Patch4:         0001-Add-support-for-systems-that-have-Python3-only-951.patch
# usr/bin/env python -> usr/bin/python3
Patch5:         0001-Replace-at-least-most-occurrences-of-python-with-pyt.patch
# Followon fixes for python3 change
Patch6:         0001-simple_switch_grpc-Use-Python-3-997.patch
Patch7:         0001-Fix-issues-in-p4dbg.py-after-switch-to-Python3-1017.patch

BuildRequires:  autoconf automake
BuildRequires:  boost-devel
BuildRequires:  gcc-c++ gmp-devel
BuildRequires:  Judy-devel json-c-devel
BuildRequires:  libpcap-devel libtool
BuildRequires:  nanomsg-devel

Requires:       boost
Requires:       gmp
Requires:       Judy json-c
Requires:       nanomsg
Requires:       python3-nnpy

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
cd behavioral-model-%{version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
cd behavioral-model-%{version}
./autogen.sh
mkdir build
cd build

# Neither static libraries nor thrift features are needed for p4c
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-static \
    --without-thrift

make %{?_smp_mflags} 

%install
cd behavioral-model-%{version}
# license
%{__mkdir_p} %{buildroot}%{_datadir}/p4-bmv2
%{__cp} LICENSE %{buildroot}%{_datadir}/p4-bmv2/LICENSE
cd build
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}/%{_libdir}

%files
%dir %{_datadir}/p4-bmv2
%license %{_datadir}/p4-bmv2/LICENSE
%{_bindir}/bm_nanomsg_events
%{_bindir}/bm_p4dbg
%{_libdir}/libbmall.so.0.1.0
%{_libdir}/libbmp4apps.so.0.1.0
%{_libdir}/libsimpleswitch_runner.so.0.1.0
%{python3_sitelib}/nanomsg_client.py
%{python3_sitelib}/p4dbg.py

%files devel
%dir %{_includedir}/bm
%{_includedir}/bm/*
%{_libdir}/libbmall.la
%{_libdir}/libbmall.so
%{_libdir}/libbmall.so.0
%{_libdir}/libbmp4apps.la
%{_libdir}/libbmp4apps.so
%{_libdir}/libbmp4apps.so.0
%{_libdir}/libsimpleswitch_runner.la
%{_libdir}/libsimpleswitch_runner.so
%{_libdir}/libsimpleswitch_runner.so.0

%exclude %{python3_sitelib}/__pycache__/*

%changelog
* Fri Nov 26 2021 <trix@redhat.com> - 1.14.0-1
- Initial release




