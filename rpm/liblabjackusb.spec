Name:           liblabjackusb
Version:        2.5.2
Release:        1
Summary:        LabJack I/O device driver
Group:          Hardware/Other
License:        MIT X11
URL:            http://labjack.com/
Source0:        %{name}-%{version}.tar.gz
Patch0001:      0001-remove-ldconfig.patch
BuildRequires:  libusb1-devel

%description
The exodriver library for accessing LabJack I/O-devices.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains header files and examples for developing
applications that use %{name} for accessing LabJack I/O-devices.

%prep
%setup -q
cd exodriver
%patch0001 -p1

%build
make -C exodriver/liblabjackusb DESTINATION=%{_libdir} HEADER_DESTINATION=%{_includedir}

%install
make -C exodriver/liblabjackusb DESTINATION=%{buildroot}%{_libdir} HEADER_DESTINATION=%{buildroot}%{_includedir} install
chmod a-x %{buildroot}%{_includedir}/*
install -D -m 644 exodriver/10-labjack.rules %{buildroot}%{_sysconfdir}/udev/rules.d/10-labjack.rules

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
test -x /sbin/udevadm && /sbin/udevadm control --reload-rules

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%doc README README.setup
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc INSTALL.Linux examples
%{_includedir}/*
%{_libdir}/*.so
