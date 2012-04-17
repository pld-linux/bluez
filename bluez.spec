Summary:	Bluetooth utilities
Summary(pl.UTF-8):	Narzędzia Bluetooth
Name:		bluez
Version:	4.99
Release:	4
License:	GPL v2+
Group:		Applications/System
#Source0Download: http://www.bluez.org/download.html
Source0:	http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.bz2
# Source0-md5:	2387053eb5a7b02f37df4871df022a02
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	dund.init
Source4:	pand.init
Source5:	rfcomm.init
Patch0:		%{name}-etc_dir.patch
Patch1:		%{name}-wacom-mode-2.patch
Patch2:		%{name}-systemd.patch
Patch3:		%{name}-audio_socket.patch
URL:		http://www.bluez.org/
BuildRequires:	alsa-lib-devel >= 1.0.10-1
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	check-devel >= 0.9.6
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	glib2-devel >= 1:2.16
BuildRequires:	gstreamer-devel >= 0.10.30
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	libcap-ng-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.626
BuildRequires:	udev-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.16
Requires:	hwdata >= 0.225
Requires:	rc-scripts
Requires:	systemd-units >= 38
Provides:	bluez-utils = %{version}-%{release}
Obsoletes:	bluez-hciemu
Obsoletes:	bluez-pan
Obsoletes:	bluez-sdp
Obsoletes:	bluez-systemd
Obsoletes:	bluez-utils
Obsoletes:	bluez-utils-init
Conflicts:	bluez-bluefw
ExcludeArch:	s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# currently lib, not %{_lib} (see cups.spec)
%define		cupsdir		/usr/lib/cups/backend
%define		udevdir		/lib/udev

%description
Bluetooth utilities:
 - bluetoothd
 - dund
 - hcitool
 - hciattach
 - hciconfig
 - hciemu
 - hidd
 - l2ping
 - pand
 - start scripts (PLD)
 - PCMCIA configuration files

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%description -l pl.UTF-8
Narzędzia Bluetooth:
 - bluetoothd
 - dund
 - hcitool
 - hciattach
 - hciconfig
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
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib >= 1.0.10-1

%description -n alsa-plugins-bluetooth
ALSA plugins for Bluetooth audio devices.

%description -n alsa-plugins-bluetooth -l pl.UTF-8
Wtyczki systemu ALSA dla urządzeń dźwiękowych Bluetooth.

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

%package -n gstreamer-bluetooth
Summary:	Bluetooth support for gstreamer
Summary(pl.UTF-8):	Obsługa Bluetooth dla gstreamera
Group:		Libraries
Requires:	bluez-libs >= %{version}-%{release}
Requires:	gstreamer >= 0.10.30
Requires:	gstreamer-plugins-base >= 0.10

%description -n gstreamer-bluetooth
Bluetooth support for gstreamer.

%description -n gstreamer-bluetooth -l pl.UTF-8
Obsługa Bluetooth dla gstreamera.

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-ouifile=%{_datadir}/hwdata/oui.txt \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	--disable-silent-rules \
	--enable-shared \
	--enable-static \
	--enable-alsa \
	--enable-audio \
	--enable-bccmd \
	--enable-capng \
	--enable-cups \
	--enable-dbusoob \
	--enable-dfutool \
	--enable-dund \
	--enable-gstreamer \
	--enable-health \
	--enable-hid2hci \
	--enable-hidd \
	--enable-input \
	--enable-network \
	--enable-pand \
	--enable-pcmcia \
	--enable-pnat \
	--enable-serial \
	--enable-thermometer \
	--enable-tools \
	--enable-usb \
	--enable-wiimote

%{__make} \
	cupsdir=%{cupsdir} \
	rulesdir=%{udevdir}/rules.d \
	udevdir=%{udevdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_libdir}/bluetooth/plugins

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir} \
	rulesdir=%{udevdir}/rules.d \
	udevdir=%{udevdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bluetooth
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bluetooth
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/dund
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/pand
install %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/rfcomm

install audio/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth
install input/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth
install network/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth
install serial/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/bluetooth

mv -fT $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/alsa

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{alsa-lib/*.{la,a},gstreamer*/libgstbluetooth.{la,a},libbluetooth.la}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bluetooth
/sbin/chkconfig --add dund
/sbin/chkconfig --add pand
/sbin/chkconfig --add rfcomm
%service bluetooth restart
%service dund restart
%service pand restart
%service rfcomm restart
%systemd_post bluetooth.service

%preun
if [ "$1" = "0" ]; then
	%service bluetooth stop
	%service dund stop
	%service pand stop
	%service rfcomm stop
	/sbin/chkconfig --del bluetooth
	/sbin/chkconfig --del dund
	/sbin/chkconfig --del pand
	/sbin/chkconfig --del rfcomm
fi
%systemd_preun bluetooth.service

%postun
%systemd_reload

%triggerpostun -- bluez < 4.98-3
%systemd_trigger bluetooth.service

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/ciptool
%attr(755,root,root) %{_bindir}/dfutool
%attr(755,root,root) %{_bindir}/dund
%attr(755,root,root) %{_bindir}/gatttool
%attr(755,root,root) %{_bindir}/hcitool
%attr(755,root,root) %{_bindir}/hidd
%attr(755,root,root) %{_bindir}/l2ping
%attr(755,root,root) %{_bindir}/pand
%attr(755,root,root) %{_bindir}/rfcomm
%attr(755,root,root) %{_bindir}/sdptool
%attr(755,root,root) %{_sbindir}/bccmd
%attr(755,root,root) %{_sbindir}/bluetoothd
%attr(755,root,root) %{_sbindir}/hciattach
%attr(755,root,root) %{_sbindir}/hciconfig
%dir %{_libdir}/bluetooth
%dir %{_libdir}/bluetooth/plugins
%dir %{_sysconfdir}/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/*.conf
%attr(754,root,root) /etc/rc.d/init.d/bluetooth
%attr(754,root,root) /etc/rc.d/init.d/dund
%attr(754,root,root) /etc/rc.d/init.d/pand
%attr(754,root,root) /etc/rc.d/init.d/rfcomm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bluetooth
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/bluetooth.conf
%{systemdunitdir}/bluetooth.service
%{_datadir}/dbus-1/system-services/org.bluez.service
%attr(755,root,root) %{udevdir}/bluetooth_serial
%attr(755,root,root) %{udevdir}/hid2hci
%{udevdir}/rules.d/97-bluetooth.rules
%{udevdir}/rules.d/97-bluetooth-hid2hci.rules
%{udevdir}/rules.d/97-bluetooth-serial.rules
%{_mandir}/man1/ciptool.1*
%{_mandir}/man1/dfutool.1*
%{_mandir}/man1/dund.1*
%{_mandir}/man1/hcitool.1*
%{_mandir}/man1/hidd.1*
%{_mandir}/man1/pand.1*
%{_mandir}/man1/rfcomm.1*
%{_mandir}/man1/sdptool.1*
%{_mandir}/man8/bccmd.8*
%{_mandir}/man8/bluetoothd.8*
%{_mandir}/man8/hciattach.8*
%{_mandir}/man8/hciconfig.8*
%{_mandir}/man8/hid2hci.8*
%{_mandir}/man8/l2ping.8*

%files -n alsa-plugins-bluetooth
%defattr(644,root,root,755)
%{_sysconfdir}/alsa/bluetooth.conf
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
%attr(755,root,root) %ghost %{_libdir}/libbluetooth.so.3

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluetooth.so
%{_includedir}/bluetooth
%{_pkgconfigdir}/bluez.pc

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libbluetooth.a
