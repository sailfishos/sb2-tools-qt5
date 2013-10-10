%define __strip /bin/true
%define architecture_target mipsel
%define _build_name_fmt    %%{ARCH}/%%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.dontuse.rpm
%define packages_in_tools  qt-qmake qt5-qmake qt-tools qt5-tools qt5-qtcore libicu systemd
Name:          sb2-tools-qt5-mipsel
Version:       1.0
Release:       1
Source0:       %{name}-%{version}.tar.bz2
Source1:       baselibs.conf
Source2:       precheckin.sh
Source3:       sb2-tools-qt5-armv7hl-rpmlintrc
Source4:       sb2-tools-qt5-armv7l-rpmlintrc
Source5:       sb2-tools-qt5-mipsel-rpmlintrc
Source6:       sb2-tools-qt5-template-rpmlintrc

AutoReqProv:   0
BuildRequires: rpm grep tar patchelf sed fakeroot
BuildRequires: %packages_in_tools
ExclusiveArch: %{ix86}

# no auto requirements - they're generated
License:       BSD
Group:         Development/Tools
Summary:       SB2 cross tools for qt5

%description
This is a package providing %packages_in_tools for SB2 tools directory 
It is not intended to be used in a normal system!


%package dependency
Summary: Dependency for sb2 host side
Group: Development/Tools

%description dependency
This is a package providing %packages_in_tools SB2 tools directory
It is not intended to be used in a normal system!

%prep
%setup -q -n %{name}-%{version}

%build

%install

#set +x -e
mkdir -p %buildroot
rpm -ql %packages_in_tools > filestoinclude1
cat > filestoignore << EOF
/usr/share/man
/usr/share/doc
EOF
grep -vf filestoignore filestoinclude1 | sort | uniq > filestoinclude2
cat filestoinclude2
tar --no-recursion -T filestoinclude2 -cpf - | ( cd %buildroot && fakeroot tar -xvpf - )

shellquote()
{
    for arg; do
        arg=${arg//\\/\\\\}
#        arg=${arg//\$/\$}   # already needs quoting ;(
#        arg=${arg/\"/\\\"}  # dito
#        arg=${arg//\`/\`}   # dito
        arg=${arg//\\ |/\|}
        arg=${arg//\\|/|}
        echo "$arg"
    done
}

echo "Creating baselibs_new.conf"
echo ""
rm -rRf /tmp/baselibs_new.conf || true
shellquote "arch i486 targets mipsel:inject" >> /tmp/baselibs_new.conf
shellquote "%{name}" >> /tmp/baselibs_new.conf
shellquote "  targettype x86 block!" >> /tmp/baselibs_new.conf
shellquote "  targettype 32bit block!" >> /tmp/baselibs_new.conf
shellquote "  targettype inject autoreqprov off" >> /tmp/baselibs_new.conf
shellquote "  targettype inject extension -inject" >> /tmp/baselibs_new.conf
shellquote "  targettype inject +/" >> /tmp/baselibs_new.conf
shellquote "  targettype inject -%{_mandir}" >> /tmp/baselibs_new.conf
shellquote "  targettype inject -%{_docdir}" >> /tmp/baselibs_new.conf
shellquote "  targettype inject config    -/sb2-config$" >> /tmp/baselibs_new.conf

shellquote "arch i486 targets mipsel:inject" >> /tmp/baselibs_new.conf
shellquote "%{name}-dependency" >> /tmp/baselibs_new.conf
shellquote "  targettype x86 block!" >> /tmp/baselibs_new.conf
shellquote "  targettype 32bit block!" >> /tmp/baselibs_new.conf
shellquote "  targettype inject autoreqprov off" >> /tmp/baselibs_new.conf
shellquote "  targettype inject extension -inject" >> /tmp/baselibs_new.conf
shellquote "  targettype inject +/" >> /tmp/baselibs_new.conf
shellquote "  targettype inject -%{_mandir}" >> /tmp/baselibs_new.conf
shellquote "  targettype inject -%{_docdir}" >> /tmp/baselibs_new.conf
shellquote "  targettype inject config    -/sb2-config$" >> /tmp/baselibs_new.conf

cat /tmp/baselibs_new.conf > %{_sourcedir}/baselibs.conf
mkdir -p %buildroot/etc
touch %buildroot/etc/sb2-tools-qt5-template

%clean
rm -rf $RPM_BUILD_ROOT

%files dependency
%defattr(-,root,root)
/etc/sb2-tools-qt5-template

%files -f filestoinclude2
%defattr(-,root,root)


