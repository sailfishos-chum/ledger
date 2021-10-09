%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:             ledger
Version:          3.2.1
Release:          1%{?dist}
Summary:          A powerful command-line double-entry accounting system
License:          BSD
URL:              http://ledger-cli.org/
Source0:          https://github.com/ledger/ledger/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:    boost-devel
BuildRequires:    cmake
BuildRequires:    make
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    gettext-devel
BuildRequires:    gmp-devel
BuildRequires:    libedit-devel
BuildRequires:    mpfr-devel
BuildRequires:    /usr/bin/python

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Ledger is a powerful, double-entry accounting system that is accessed
from the UNIX command-line. This may put off some users as there is
no flashy UI but for those who want unparalleled reporting access to
their data, there really is no alternative.

%package devel
Summary: Libraries and header files for %{name} development
Requires: %{name} = %{version}-%{release}
%description devel
Libraries and header files for %{name} development.

%prep
%setup -qn %{name}-%{version}/ledger

%build
python ./acprep --no-git --prefix=%{_prefix} update

%install
make install DESTDIR=%{buildroot}

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -p -m0644 contrib/ledger-completion.bash \
    %{buildroot}%{_sysconfdir}/bash_completion.d/ledger

# Install documentation manually to a convenient directory layout
rm -rf %{buildroot}%{_docdir}

# Contrib scripts
mkdir -p %{buildroot}%{_pkgdocdir}/contrib
for i in bal bal-huquq entry getquote.pl getquote-uk.py ledger-du ParseCcStmt.cs README repl.sh report tc ti to trend; do
    install -p -m0644 contrib/${i} %{buildroot}%{_pkgdocdir}/contrib/${i}
done

# Input samples
mkdir -p %{buildroot}%{_pkgdocdir}/samples
for i in demo.ledger drewr3.dat drewr.dat sample.dat wow.dat; do
    install -p -m0644 test/input/${i} %{buildroot}%{_pkgdocdir}/samples/${i}
done

%check

%postun -p /sbin/ldconfig
%post
/sbin/ldconfig

%files
%doc %{_pkgdocdir}/contrib
%doc %{_pkgdocdir}/samples
%{_bindir}/ledger
%{_libdir}/libledger.so.3
%{_mandir}/man1/ledger.1*
%config(noreplace) %{_sysconfdir}/bash_completion.d/ledger
%license LICENSE.md

%files devel
%{_includedir}/ledger
%{_libdir}/libledger.so

%changelog
* Sat Oct 09 2021 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 3.2.1-1
- New upstream release
- Adapt for OBS
* Wed May 01 2019 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 3.1.3-1
- New upstream release
* Sun Jan 06 2019 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 3.1.1-1
- Initial release for sailfishos
