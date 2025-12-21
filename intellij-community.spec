# setting some global constants
%global appname intellij
# The actual executable name in /usr/bin
%global command_name intellij-community

# disable debuginfo subpackage
%global debug_package %{nil}
# Disable build-id symlinks to avoid conflicts
%global _build_id_links none
# don't strip bundled binaries
%global __strip /bin/true
# dont repack jars
%global __jar_repack %{nil}
# disable rpath checks
%define __brp_check_rpaths %{nil}
# do not automatically detect and export provides and dependencies on bundled libraries and executables
%global __provides_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*
%global __requires_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*

Name:          %{appname}-community
Version:       2025.3.1
Release:       1%{?dist}

Summary:       IntelliJ IDEA Community Edition
License:       Apache-2.0
URL:           https://www.jetbrains.com/idea/

# Using the pre-built binary tarball hosted on GitHub Releases assets
# Based on user image: idea-2025.3.1.tar.gz (for generic/linux)
# Release tag format: idea/2025.3.1
Source0:       https://github.com/JetBrains/intellij-community/releases/download/idea/%{version}/idea-%{version}.tar.gz

Source101:     %{name}.xml
Source102:     %{name}.desktop
Source103:     %{name}.metainfo.xml

BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: librsvg2-tools
BuildRequires: javapackages-filesystem

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem
Requires:      git

ExclusiveArch: x86_64 aarch64

Obsoletes:     %{name}-jre < %{?epoch:%{epoch}:}%{version}-%{release}

%description
IntelliJ IDEA Community Edition is the open source version of IntelliJ IDEA,
an IDE for Java, Kotlin, Groovy, and other programming languages.

%package doc
Summary:       Documentation for IntelliJ IDEA Community Edition
BuildArch:     noarch
Requires:      %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description doc
This package contains documentation for IntelliJ IDEA Community Edition.

%prep
# Official binary tarball (from GitHub assets) usually extracts to 'idea-IC-<build-rev>'
# We use shell globbing to handle the build revision number directory
%setup -q -c

# Move contents from the versioned directory to the top level
# The directory name inside the tarball is unknown (usually idea-IC-<build>), so we glob it.
mv idea-IC-*/* .
mv idea-IC-*/.* . 2>/dev/null || :
rmdir idea-IC-*

# Removing trialware plugins or strict cleanup if needed
# rm -rf plugins/{...}

%install
# Installing application...
install -d %{buildroot}%{_javadir}/%{name}
cp -arf ./{bin,jbr,lib,plugins,build.txt,product-info.json} %{buildroot}%{_javadir}/%{name}/
if [ -d modules ]; then cp -arf ./modules %{buildroot}%{_javadir}/%{name}/; fi

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
if [ -f bin/idea.png ]; then
    install -m 0644 -p bin/idea.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
elif [ -f bin/idea.svg ]; then
    install -m 0644 -p bin/idea.svg %{buildroot}%{_datadir}/pixmaps/%{name}.svg
fi

install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
if [ -f bin/idea.svg ]; then
    install -m 0644 -p bin/idea.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
fi

# Creating additional PNG icons on the fly...
if [ -f bin/idea.svg ]; then
    for size in 16 22 24 32 48 64 128 256; do
        dest=%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
        install -d ${dest}
        rsvg-convert -w ${size} -h ${size} bin/idea.svg -o ${dest}/%{name}.png
        chmod 0644 ${dest}/%{name}.png
        touch -r bin/idea.svg ${dest}/%{name}.png
    done
fi

# Installing metainfo...
install -d %{buildroot}%{_metainfodir}
install -m 0644 -p %{SOURCE103} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/bin/idea.sh %{buildroot}%{_bindir}/%{command_name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE102} %{buildroot}%{_datadir}/applications/%{name}.desktop

# Installing mime package...
install -d %{buildroot}%{_datadir}/mime/packages
install -m 0644 -p %{SOURCE101} %{buildroot}%{_datadir}/mime/packages/%{name}.xml

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_javadir}/%{name}
%{_bindir}/%{command_name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{name}.metainfo.xml

%files doc
%doc help/
%doc Install-Linux-tar.txt

%changelog
* Sun Dec 21 2024 User <user@example.com> - 2025.3.1-1
- Update to version 2025.3.1
- Switch source to official GitHub binary asset (idea-2025.3.1.tar.gz)
