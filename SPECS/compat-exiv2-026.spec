Name:    compat-exiv2-026
Version: 0.26
Release: 7%{?dist}
Summary: Compatibility package with the exiv2 library in version 0.26

License: GPLv2+
URL:     http://www.exiv2.org/
Source0: https://github.com/Exiv2/%{name}/archive/exiv2-%{version}.tar.gz

Patch0:  exiv2-simplify-compiler-info-in-cmake.patch
Patch1:  exiv2-do-not-build-documentation.patch

## upstream patches (lookaside cache)
Patch6:  0006-1296-Fix-submitted.patch

# Security fixes
Patch10: exiv2-CVE-2017-17723-1.patch
Patch11: exiv2-CVE-2017-17723-2.patch
Patch12: exiv2-wrong-brackets.patch
Patch13: exiv2-CVE-2017-11683.patch
Patch14: exiv2-CVE-2017-14860.patch
Patch15: exiv2-CVE-2017-14864-CVE-2017-14862-CVE-2017-14859.patch
Patch16: exiv2-CVE-2017-17725.patch
Patch17: exiv2-CVE-2017-17669.patch
Patch18: exiv2-additional-security-fixes.patch
Patch19: exiv2-CVE-2018-10958.patch
Patch20: exiv2-CVE-2018-10998.patch
Patch21: exiv2-CVE-2018-11531.patch
Patch22: exiv2-CVE-2018-12264-CVE-2018-12265.patch
Patch23: exiv2-CVE-2018-14046.patch
Patch24: exiv2-CVE-2018-5772.patch
Patch25: exiv2-CVE-2018-8976.patch
Patch26: exiv2-CVE-2018-8977.patch
Patch27: exiv2-CVE-2018-16336.patch
Patch28: exiv2-CVE-2021-31291.patch
Patch29: exiv2-CVE-2021-31292.patch
Patch30: exiv2-CVE-2021-37618.patch
Patch31: exiv2-CVE-2021-37619.patch
Patch32: exiv2-CVE-2020-18898.patch

## upstreamable patches

BuildRequires: cmake
BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libssh)
BuildRequires: zlib-devel

Conflicts: exiv2-libs < 0.27

%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments

%prep
%autosetup -n exiv2-%{version} -p1


%build
# exiv2: embedded copy of exempi should be compiled with BanAllEntityUsage
# https://bugzilla.redhat.com/show_bug.cgi?id=888769
export CPPFLAGS="-DBanAllEntityUsage=1"

%{cmake} \
  -DEXIV2_ENABLE_BUILD_PO:BOOL=OFF \
  -DEXIV2_ENABLE_BUILD_SAMPLES:BOOL=OFF \
  -DEXIV2_ENABLE_LIBXMP:BOOL=ON .
  # FIXME: build this because it adds Threads library and it doesn't build without
  #        it from some reason

make %{?_smp_mflags}

%install
make install/fast DESTDIR=%{buildroot}

## unpackaged files
rm -rf %{buildroot}%{_bindir}/exiv2
rm -rf %{buildroot}%{_includedir}/exiv2
rm -rf %{buildroot}%{_libdir}/libexiv2.la
rm -rf %{buildroot}%{_libdir}/libxmp.a
rm -rf %{buildroot}%{_libdir}/pkgconfig/exiv2.pc
rm -rf %{buildroot}%{_libdir}/pkgconfig/exiv2.lsm
rm -rf %{buildroot}%{_datadir}/locale/*
rm -rf %{buildroot}%{_mandir}/*
rm -rf mv %{buildroot}%{_libdir}/libexiv2.so


%files
%doc COPYING README
%{_libdir}/libexiv2.so.26*


%changelog
* Wed Oct 13 2021 Jan Grulich <jgrulich@redhat.com> - 0.26-7
- Fix stack exhaustion issue in the printIFDStructure function
  Resolves: bz#2003669

* Wed Aug 18 2021 Jan Grulich <jgrulich@redhat.com> - 0.26-6
- Fix out-of-bounds read in Exiv2::Jp2Image::printStructure
  Resolves: bz#1993283

- Fix out-of-bounds read in Exiv2::Jp2Image::encodeJp2Header
  Resolves: bz#1993246

* Thu Aug 05 2021 Jan Grulich <jgrulich@redhat.com> - 0.26-4
- Fix heap-based buffer overflow vulnerability in jp2image.cpp that may lead to DoS
  Resolves: bz#1990398

- Integer overflow in CrwMap:encode0x1810 leading to heap-based buffer overflow and DoS
  Resolves: bz#1990399

* Thu Nov 21 2019 Jan Grulich <jgrulich@redhat.com> - 0.26-3
- Remove pre-built msvc binaries
  Resolves: bz#1757349

* Wed Oct 09 2019 Tomas Pelka <tpelka@redhat.com> - 0.26-2
- bump version in order to pick up with gating

* Mon Oct 07 2019 Jan Grulich <jgrulich@redhat.com> - 0.26-1
- Spec file based on exiv2 package to provide old libraries before API change
  Resolves: bz#1757349
