Summary:	Program that emulates mouse clicks
Name:		mouseemu
Version:	0.15
Release:	%mkrel 2
License:	GPL
Group:		System/Configuration/Hardware
URL:		http://www.geekounet.org/powerbook/files
Source0:	http://www.geekounet.org/powerbook/files/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.rules

Patch1:		%{name}-nousb-noadb.patch.bz2
Patch2:		%{name}-makefile.patch
Patch3:		%{name}-nofork.patch
Patch4:		%{name}-usage-cleanup.patch
Patch5:		%{name}-manpage.patch
Patch6:		%{name}-rescan.patch
Patch7:		%{name}-syslog.patch
Patch8:		%{name}-pidfile.patch
Requires(pre):  /sbin/chkconfig
Requires(pre):	rpm-helper
Requires:	procps, udev

%description
A program that will allows the keyboard to send mouse events.
It can be used to configure right, middle and scroll buttons via 
the keyboard when you do not have a mouse with these buttons 
available (like for example on iBooks, pBooks, and macBooks).

%prep
%setup -q -n %{name}
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}

install -d %{buildroot}/{%{_sbindir},%{_sysconfdir}/{rc.d/init.d,sysconfig,udev/rules.d,modprobe.preload.d},%{_mandir}/man8}

install mouseemu %{buildroot}/%{_sbindir}
install -m644 %{SOURCE1}	%{buildroot}/%{_sysconfdir}/rc.d/init.d/%{name}
install -m644 %{SOURCE2}	%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -m644 %{SOURCE3}	%{buildroot}/%{_sysconfdir}/udev/rules.d/90-mouseemu.rules
install -m644 mouseemu.8	%{buildroot}/%{_mandir}/man8/mouseemu.8

cat >  %{buildroot}/%{_sysconfdir}/modprobe.preload.d/%{name} <<EOF
evdev
uinput
EOF

%clean
rm -rf %{buildroot}

%post
%_post_service mouseemu

%preun
%_preun_service mouseemu

%files
%defattr(644,root,root,755)
%doc README
%attr(744,root,root) %{_sbindir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(744,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%{_sysconfdir}/udev/rules.d/90-%{name}.rules
%{_sysconfdir}/modprobe.preload.d/%{name}
%{_mandir}/man8/mouseemu*

