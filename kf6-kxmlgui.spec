#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# Not packaged:
# /etc/xdg/ui
%define		kdeframever	6.0
%define		qtver		5.15.2
%define		kfname		kxmlgui

Summary:	Framework for managing menu and toolbar actions
Name:		kf6-%{kfname}
Version:	6.0.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	5de68ebf37021a60488388732388b76e
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6PrintSupport-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kconfigwidgets-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kglobalaccel-devel >= %{version}
BuildRequires:	kf6-kguiaddons-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	kf6-kiconthemes-devel >= %{version}
BuildRequires:	kf6-kitemviews-devel >= %{version}
BuildRequires:	kf6-ktextwidgets-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Network >= %{qtver}
Requires:	Qt6PrintSupport >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	Qt6Xml >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kconfig >= %{version}
Requires:	kf6-kconfigwidgets >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kglobalaccel >= %{version}
Requires:	kf6-kguiaddons >= %{version}
Requires:	kf6-ki18n >= %{version}
Requires:	kf6-kiconthemes >= %{version}
Requires:	kf6-kitemviews >= %{version}
Requires:	kf6-kwidgetsaddons >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KXMLGUI provides a framework for managing menu and toolbar actions in
an abstract way. The actions are configured through a XML description
and hooks in the application code. The framework supports merging of
multiple description for example for integrating actions from plugins.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6DBus-devel >= %{qtver}
Requires:	Qt6Widgets-devel >= %{qtver}
Requires:	Qt6Xml-devel >= %{qtver}
Requires:	cmake >= 3.16
Requires:	kf6-kconfig-devel >= %{version}
Requires:	kf6-kconfigwidgets-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -rf $RPM_BUILD_ROOT%{_localedir}/{ie,tok}

%find_lang %{kfname}6

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6XmlGui.so.6
%attr(755,root,root) %{_libdir}/libKF6XmlGui.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/kxmlgui6widgets.so
%{_datadir}/qlogging-categories6/kxmlgui.categories
%{_datadir}/qlogging-categories6/kxmlgui.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KXmlGui
%{_libdir}/cmake/KF6XmlGui
%{_libdir}/libKF6XmlGui.so
