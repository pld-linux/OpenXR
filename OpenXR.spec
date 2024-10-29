Summary:	OpenXR loader and validation layers implementation
Summary(pl.UTF-8):	Implementacja loadera i warstw kontroli poprawności standardu OpenXR
Name:		OpenXR
Version:	1.1.42
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/KhronosGroup/OpenXR-SDK-Source/releases
Source0:	https://github.com/KhronosGroup/OpenXR-SDK-Source/releases/download/release-%{version}/%{name}-SDK-Source-release-%{version}.tar.gz
# Source0-md5:	6d4fdbe88938bdebc70f0d336a303a1a
Patch0:		%{name}-jsoncpp.patch
URL:		https://www.khronos.org/openxr/
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGLESv2-devel
BuildRequires:	OpenGLESv3-devel
BuildRequires:	Vulkan-Headers
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	glslang
BuildRequires:	jsoncpp-devel
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-jinja2
BuildRequires:	shaderc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenXR is a royalty-free, open standard that provides high-performance
access to Augmented Reality (AR) and Virtual Reality (VR)
(collectively known as XR) platforms and devices.

This SDK contains the implementation of loader, validation layers and
code samples.

%description -l pl.UTF-8
OpenXR to otwarty, wolny od opłat licencyjnych standard zapewniający
wydajny dostęp do platform i urządzeń AR (Augmented Reality) oraz VR
(Virtual Reality), wspólnie określanych jako XR.

To SDK zawiera implementację loadera, warstw sprawdzania poparwności
oraz przykładowy kod.

%package devel
Summary:	Header files for OpenXR library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenXR
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenXR library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenXR.

%prep
%setup -q -n %{name}-SDK-Source-release-%{version}
%patch0 -p1

%build
%cmake -B build \
	-DBUILD_ALL_EXTENSIONS=ON \
	-DBUILD_WITH_SYSTEM_JSONCPP=ON \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.SDK.md COPYING.adoc README.md
%attr(755,root,root) %{_bindir}/hello_xr
%attr(755,root,root) %{_bindir}/openxr_runtime_list
%attr(755,root,root) %{_bindir}/openxr_runtime_list_json
%attr(755,root,root) %{_libdir}/libXrApiLayer_api_dump.so
%attr(755,root,root) %{_libdir}/libXrApiLayer_core_validation.so
%attr(755,root,root) %{_libdir}/libopenxr_loader.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenxr_loader.so.1
%{_datadir}/openxr
%{_mandir}/man1/hello_xr.1*
%{_mandir}/man1/openxr_runtime_list.1*
%{_mandir}/man1/openxr_runtime_list_json.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenxr_loader.so
%{_includedir}/openxr
%{_pkgconfigdir}/openxr.pc
%{_libdir}/cmake/openxr
