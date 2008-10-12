Summary:	Bluetooth utilities
Summary(pl.UTF-8):	Narzędzia Bluetooth
Name:		bluez
Version:	4.13
Release:	1
Epoch:		0
License:	GPL v2+
Group:		Applications/System
#Source0Download: http://www.bluez.org/download.html
Source0:	http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.gz
# Source0-md5:	7ce8ed3a586782aa48251f9a547e287f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}-udev.rules
Source4:	%{name}-udev.script
Patch0:		%{name}-etc_dir.patch
URL:		http://www.bluez.org/
BuildRequires:	alsa-lib-devel >= 1.0.10-1
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	openobex-devel >= 1.1
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	rc-scripts
Obsoletes:	bluez-hciemu
Obsoletes:	bluez-pan
Obsoletes:	bluez-sdp
Obsoletes:	bluez-utils
Obsoletes:	bluez-utils-init
Conflicts:	bluez-bluefw
Provides:	bluez-utils = %{epoch}:%{version}-%{release}
ExcludeArch:	s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# currently lib, not %{_lib} (see cups.spec)
%define		cupsdir		/usr/lib/cups/backend
%define		udevdir		/%{_lib}/udev

%description
Bluetooth utilities:
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - hciemu
 - hidd
 - l2ping
 - pand
 - start scripts (PLD)
 - PCMCIA configuration files

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%description -l pl.UTF-8
Narzędzia Bluetooth:
 - hcitool
 - hciattach
 - hciconfig
 - hcid
 - hciemu
 - hidd
 - l2ping
 - pand
 - skrypty startowe (PLD)
 - pliki konfiguracji PCMCIA

Znaki towarowe BLUETOOTH są własnością Bluetooth SIG, Inc. z USA.

%package -n alsa-plugins-bluetooth
Summary:	ALSA plugins for Bluetooth audio devices
Summary(pl.UTF-8):	Wtyczki systemu ALSA dla urządzeń dźwiękowych Bluetooth
Group:		Libraries
# bluetoothd + audio service
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	alsa-lib >= 1.0.10-1

%description -n alsa-plugins-bluetooth
ALSA plugins for Bluetooth audio devices.

%description -n alsa-plugins-bluetooth -l pl.UTF-8
Wtyczki systemu ALSA dla urządzeń dźwiękowych Bluetooth.

%package -n cups-backend-bluetooth
Summary:	Bluetooth backend for CUPS
Summary(pl.UTF-8):	Backend Bluetooth dla CUPS-a
Group:		Applications/Printing
Requires:	bluez-libs >= %{epoch}:%{version}-%{release}
Requires:	cups

%description -n cups-backend-bluetooth
Bluetooth backend for CUPS.

%description -n cups-backend-bluetooth -l pl.UTF-8
Backend Bluetooth dla CUPS-a.

%package -n gstreamer-bluetooth
Summary:	Bluetooth support for gstreamer
Summary(pl.UTF-8):	Obsługa Bluetooth dla gstreamera
Group:		Libraries
Requires:	bluez-libs >= %{epoch}:%{version}-%{release}
Requires:	gstreamer >= 0.10
Requires:	gstreamer-plugins-base >= 0.10

%description -n gstreamer-bluetooth
Bluetooth support for gstreamer.

%description -n gstreamer-bluetooth -l pl.UTF-8
Obsługa Bluetooth dla gstreamera.

%package libs
Summary:	Bluetooth libraries
Summary(pl.UTF-8):	Biblioteki Bluetooth
Group:		Development/Libraries
Obsoletes:	bluez-sdp

%description libs
Libraries for use in Bluetooth applications.

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%description libs -l pl.UTF-8
Biblioteki do używania w aplikacjach Bluetooth.

Znaki towarowe BLUETOOTH są własnością Bluetooth SIG, Inc. z USA.

%package libs-devel
Summary:	Header files for Bluetooth applications
Summary(pl.UTF-8):	Pliki nagłówkowe dla aplikacji Bluetooth
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	bluez-sdp-devel

%description libs-devel
bluez-libs-devel contains header files for use in Bluetooth
applications.

%description libs-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do używania w aplikacjach
Bluetooth.

%package libs-static
Summary:	Static Bluetooth libraries
Summary(pl.UTF-8):	Biblioteki statyczne Bluetooth
Group:		Development/Libraries
Requires:	%{name}-libs-devel = %{epoch}:%{version}-%{release}
Obsoletes:	bluez-sdp-static

%description libs-static
bluez-libs-static contains development static libraries for use in
Bluetooth applications.

%description libs-static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne, których można używać do
aplikacji Bluetooth.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	--enable-static \
	--enable-alsa \
	--enable-bccmd \
	--enable-configfiles \
	--enable-netlink \
	--enable-audio \
	--enable-bccmd \
	--enable-cups \
	--enable-dfutool \
	--enable-dund \
	--enable-gstreamer \
	--enable-hid2hci \
	--enable-hidd \
	--enable-input \
	--enable-manpages \
	--enable-network \
	--enable-pand \
	--enable-pcmciarules \
	--enable-serial \
	--enable-tools \
	--enable-test \
	--enable-usb

%{__make} \
	cupsdir=%{cupsdir} \
	udevdir=%{udevdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT{/etc/udev/rules.d,%{udevdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir} \
	udevdir=%{udevdir}

# noinst
#install sync/bluetoothd-service-sync $RPM_BUILD_ROOT%{_libdir}/bluetooth

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bluetooth
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bluetooth
install %{SOURCE3} $RPM_BUILD_ROOT/etc/udev/rules.d/70-bluetooth.rules
install %{SOURCE4} $RPM_BUILD_ROOT%{udevdir}/bluetooth.sh
mv $RPM_BUILD_ROOT/etc/udev/bluetooth.rules \
	$RPM_BUILD_ROOT/etc/udev/rules.d/71-bluetooth.rules

rm -f $RPM_BUILD_ROOT%{_libdir}/alsa-lib/*.{,l}a
rm -f $RPM_BUILD_ROOT%{_libdir}/bluetooth/plugins/*.{,l}a
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer*/libgstbluetooth.{,l}a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bluetooth
%service bluetooth restart

%preun
if [ "$1" = "0" ]; then
	%service bluetooth stop
	/sbin/chkconfig --del bluetooth
fi

%post libs   -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/bluetooth
%dir %{_libdir}/bluetooth/plugins
%attr(755,root,root) %{_libdir}/bluetooth/plugins/*.so
%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/main.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/rfcomm.conf
%attr(754,root,root) /etc/rc.d/init.d/bluetooth
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bluetooth
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/bluetooth.conf
%attr(755,root,root) %{udevdir}/bluetooth.sh
%attr(755,root,root) %{udevdir}/bluetooth_serial
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/70-bluetooth.rules
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/71-bluetooth.rules
%{_mandir}/man[18]/*

%files -n alsa-plugins-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/alsa-lib/libasound_module_ctl_bluetooth.so
%attr(755,root,root) %{_libdir}/alsa-lib/libasound_module_pcm_bluetooth.so

%files -n cups-backend-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth

%files -n gstreamer-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer*/libgstbluetooth.so

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbluetooth.so.[0-9]

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluetooth.so
%{_libdir}/libbluetooth.la
%{_includedir}/bluetooth
%{_pkgconfigdir}/bluez.pc

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libbluetooth.a
