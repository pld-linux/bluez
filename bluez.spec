# TODO:
# - verify/update bluetooth init script
# - separate obex?
Summary:	Bluetooth utilities
Summary(pl.UTF-8):	Narzędzia Bluetooth
Name:		bluez
Version:	5.42
Release:	2
License:	GPL v2+
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.xz
# Source0-md5:	cc8c53133d5be0d6c126e00cf2529028
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.bluez.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	check-devel >= 0.9.6
BuildRequires:	dbus-devel >= 1.6
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	libical-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.682
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:172
BuildRequires:	xz
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-libs >= 1.6
Requires:	glib2 >= 1:2.28
Requires:	hwdata >= 0.225
Requires:	rc-scripts
Requires:	systemd-units >= 38
Requires:	udev >= 1:172
Provides:	bluez-hcidump = %{version}
Provides:	bluez-utils = %{version}-%{release}
Provides:	obexd = %{version}
Provides:	dbus(org.openobex.client)
Provides:	obex-data-server = %{version}
# moved somewhere or dropped?
#Obsoletes:	alsa-plugins-bluetooth
Obsoletes:	bluez-hcidump
Obsoletes:	bluez-hciemu
Obsoletes:	bluez-pan
Obsoletes:	bluez-sdp
Obsoletes:	bluez-systemd
Obsoletes:	bluez-utils
Obsoletes:	bluez-utils-init
Obsoletes:	obexd
Obsoletes:	obex-data-server
# moved somewhere or dropped?
#Obsoletes:	gstreamer-bluetooth < 4.101-3
#Obsoletes:	gstreamer0.10-bluetooth < 5
Conflicts:	bluez-bluefw
ExcludeArch:	s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# currently lib, not %{_lib} (see cups.spec)
%define		cupsdir		/usr/lib/cups/backend
%define		udevdir		/lib/udev

%description
Bluetooth utilities:
 - bluetoothd
 - hciattach
 - hciconfig
 - hcidump
 - hcitool
 - l2ping
 - start scripts (PLD)

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%description -l pl.UTF-8
Narzędzia Bluetooth:
 - bluetoothd
 - hciattach
 - hciconfig
 - hcidump
 - hcitool
 - l2ping
 - skrypty startowe (PLD)

Znaki towarowe BLUETOOTH są własnością Bluetooth SIG, Inc. z USA.

%package -n cups-backend-bluetooth
Summary:	Bluetooth backend for CUPS
Summary(pl.UTF-8):	Backend Bluetooth dla CUPS-a
Group:		Applications/Printing
Requires:	bluez-libs >= %{version}-%{release}
Requires:	cups

%description -n cups-backend-bluetooth
Bluetooth backend for CUPS.

%description -n cups-backend-bluetooth -l pl.UTF-8
Backend Bluetooth dla CUPS-a.

%package libs
Summary:	Bluetooth libraries
Summary(pl.UTF-8):	Biblioteki Bluetooth
Group:		Libraries
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
Requires:	%{name}-libs = %{version}-%{release}
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
Requires:	%{name}-libs-devel = %{version}-%{release}
Obsoletes:	bluez-sdp-static

%description libs-static
bluez-libs-static contains development static libraries for use in
Bluetooth applications.

%description libs-static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne, których można używać do
aplikacji Bluetooth.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-experimental \
	--enable-library \
	--enable-sixaxis \
	--enable-static \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	--with-systemduserunitdir=%{systemduserunitdir}

%{__make} \
	cupsdir=%{cupsdir} \
	rulesdir=%{udevdir}/rules.d \
	udevdir=%{udevdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_libdir}/{bluetooth,obex}/plugins,%{_sysconfdir}/bluetooth}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir} \
	rulesdir=%{udevdir}/rules.d \
	udevdir=%{udevdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bluetooth/plugins/*.{la,a}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bluetooth
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bluetooth

install profiles/input/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth
install profiles/network/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth
install profiles/proximity/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbluetooth.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bluetooth
%service bluetooth restart
%systemd_post bluetooth.service

%preun
if [ "$1" = "0" ]; then
	%service bluetooth stop
	/sbin/chkconfig --del bluetooth
fi
%systemd_preun bluetooth.service

%postun
%systemd_reload

%triggerpostun -- bluez < 4.98-3
%systemd_trigger bluetooth.service

%triggerpostun -- bluez < 5.13-1
%service rfcomm stop
/sbin/chkconfig --del rfcomm

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/bccmd
%attr(755,root,root) %{_bindir}/bluemoon
%attr(755,root,root) %{_bindir}/bluetoothctl
%attr(755,root,root) %{_bindir}/btattach
%attr(755,root,root) %{_bindir}/btmon
%attr(755,root,root) %{_bindir}/ciptool
%attr(755,root,root) %{_bindir}/hciattach
%attr(755,root,root) %{_bindir}/hciconfig
%attr(755,root,root) %{_bindir}/hcidump
%attr(755,root,root) %{_bindir}/hcitool
%attr(755,root,root) %{_bindir}/hex2hcd
%attr(755,root,root) %{_bindir}/l2ping
%attr(755,root,root) %{_bindir}/l2test
%attr(755,root,root) %{_bindir}/mpris-proxy
%attr(755,root,root) %{_bindir}/rctest
%attr(755,root,root) %{_bindir}/rfcomm
%attr(755,root,root) %{_bindir}/sdptool
%dir %{_libdir}/bluetooth
%attr(755,root,root) %{_libdir}/bluetooth/bluetoothd
%attr(755,root,root) %{_libdir}/bluetooth/obexd
%dir %{_libdir}/bluetooth/plugins
%attr(755,root,root) %{_libdir}/bluetooth/plugins/sixaxis.so
%dir %{_libdir}/obex
%dir %{_libdir}/obex/plugins
%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/input.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/network.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/proximity.conf
%attr(754,root,root) /etc/rc.d/init.d/bluetooth
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bluetooth
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/bluetooth.conf
%{systemdunitdir}/bluetooth.service
%{systemduserunitdir}/obex.service
%{_datadir}/dbus-1/services/org.bluez.obex.service
%{_datadir}/dbus-1/system-services/org.bluez.service
%attr(755,root,root) %{udevdir}/hid2hci
%{udevdir}/rules.d/97-hid2hci.rules
%{_mandir}/man1/bccmd.1*
%{_mandir}/man1/btattach.1*
%{_mandir}/man1/ciptool.1*
%{_mandir}/man1/hciattach.1*
%{_mandir}/man1/hciconfig.1*
%{_mandir}/man1/hcidump.1*
%{_mandir}/man1/hcitool.1*
%{_mandir}/man1/hid2hci.1*
%{_mandir}/man1/l2ping.1*
%{_mandir}/man1/rctest.1*
%{_mandir}/man1/rfcomm.1*
%{_mandir}/man1/sdptool.1*
%{_mandir}/man8/bluetoothd.8*

%files -n cups-backend-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbluetooth.so.3

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluetooth.so
%{_includedir}/bluetooth
%{_pkgconfigdir}/bluez.pc

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libbluetooth.a
