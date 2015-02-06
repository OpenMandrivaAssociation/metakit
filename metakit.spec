%define major		1
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
%define soname		libmk4.so.1

Summary: 	Embeddable database
Name: 		metakit
Version: 	2.4.9.7
Release: 	9
License: 	MIT
Group: 		System/Libraries
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: 	http://www.equi4.com/pub/mk/%{name}-%{version}.tar.gz
Patch0:		metakit-2.4.9.7-flags.patch
Patch1:		metakit-2.4.9.6-alt-soname.patch
Patch2:		metakit-2.4.9.7-tcl8.6.patch
Patch3:		metakit-2.4.9.7-linkage.patch
URL: 		http://www.equi4.com/metakit/
BuildRequires:	tcl-devel
BuildRequires:	python-devel 

%description
MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n %{libname}
Summary:	Main library for %{name}, a embeddable database
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n %{develname}
Summary:	Files to compile programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname metakit 1 -d} < %{version}-%{release}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n python-%{name}
Summary:	Python bindings for %{name}, a embeddable database
Group:		System/Libraries
Requires:	%{libname} python
Provides:	Mk4py = %{version}-%{release}
Provides:	mk4py = %{version}-%{release}
Provides:	%{name}-python = %{version}-%{release}
Obsoletes:	%{name}-python < %{version}-%{release}

%description -n python-%{name}
Python bindings for %{name}

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%package -n %{name}-tcl
Summary:	Tcl bindings for %{name}, a embeddable database
Group:		System/Libraries
Requires:	%{libname} tcl
Provides:	Mk4tcl = %{version}-%{release}
Provides:	mk4tcl = %{version}-%{release}

%description -n %{name}-tcl
Tcl bindings for %{name}

MetaKit is an embeddable database which runs on Unix, Windows, Macintosh,
and other platforms. It lets you build applications which store their data
efficiently, in a portable way, and which will not need a complex runtime
installation. In terms of the data model, MetaKit takes the middle ground
between RDBMS, OODBMS, and flat-file databases - yet it is quite different
from each of them.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0
rm -rf builds/tests/CVS

%build
cd unix
sed -i -e "s/^CXXFLAGS.*/CXXFLAGS = %{optflags} -fPIC/" Makefile.in
cd ../builds
CONFIGURE_TOP="../unix" %configure2_5x --enable-python \
	--with-python="%{_includedir}/python%{python_version},%{py_platsitedir}" \
	--with-tcl=%{_includedir},%{tcl_sitearch}
%make MK4_SONAME=%{soname} TCL_LIB=-ltcl PYTHON_LIB=-lpython%{py_ver}

%check
cd builds
export LD_LIBRARY_PATH=`pwd`
make test 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{py_platsitedir}
%makeinstall_std -C builds MK4_SONAME=%{soname}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-, root, root)
%doc README
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-, root, root)
%doc README CHANGES doc demos examples 
%{_libdir}/*.so
%{_includedir}/*

%files -n python-%{name}
%defattr(-, root, root)
%doc README
%{py_platsitedir}/Mk4py.so
%{py_platsitedir}/metakit.py

%files -n %{name}-tcl
%defattr(-, root, root)
%doc doc/tcl.html doc/tcl.gif doc/e4s.gif
%{tcl_sitearch}/Mk4tcl



%changelog
* Tue Nov 02 2010 Michael Scherer <misc@mandriva.org> 2.4.9.7-8mdv2011.0
+ Revision: 592429
- rebuild for python 2.7

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 2.4.9.7-7mdv2010.0
+ Revision: 439800
- rebuild

* Sat Jan 24 2009 Funda Wang <fwang@mandriva.org> 2.4.9.7-6mdv2009.1
+ Revision: 333294
- finally fix build
- specify python via configure options
- rebuild

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 2.4.9.7-5mdv2009.1
+ Revision: 310861
- drop now useless (and broken) x86-64 workaround
- rebuild for new tcl
- move tcl stuff to new location per policy
- spec clean
- add tcl8.6.patch (fix build for Tcl 8.6)
- correct license (it's MIT not GPL)
- new devel policy

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 2.4.9.7-4mdv2009.0
+ Revision: 252345
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 2.4.9.7-2mdv2008.1
+ Revision: 140953
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Aug 26 2007 Pascal Terjan <pterjan@mandriva.org> 2.4.9.7-2mdv2008.0
+ Revision: 71486
- 2.4.9.7
- Add P1 to get again a soname (Patch from Alt)
- Move tcl lib in lib64 on 64 bits
- Add -fPIC
- Fix build (missing -I)


* Fri Nov 04 2005 Michael Scherer <misc@mandriva.org> 2.4.9.3-3mdk
- fix naming of python module
- enhance description
- use macro
- mkrel

* Mon Jan 10 2005 Austin Acton <austin@mandrake.org> 2.4.9.3-2mdk
- rebuild for python

* Sat Jul 17 2004 Michael Scherer <misc@mandrake.org> 2.4.9.3-1mdk
- New release 2.4.9.3
- rpmbuildupdate aware

* Mon Apr 07 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4.9.2-2mdk
- add another provides to the -devel

* Mon Mar 31 2003 Austin Acton <aacton@yorku.ca> 2.4.9.2-1mdk
- cleanup spec
- update
- use mklibname
- add docs, demos
- add python and tcl extensions
- redo patch

* Tue Jan 28 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.4.6-3mdk
- rebuild

* Thu Sep 05 2002 Lenny Cartier <lenny@mandrakesoft.com> 2.4.6-2mdk
- rebuild

* Mon Jun 03 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4.6-1mdk
- recompile against latest libstdc++
- new version
- provide library version so that we can use dynamic library as usual

* Mon Feb 18 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4.3-1mdk
- first mdk release as a separate package (was previously inside simgear)

