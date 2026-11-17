#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	resolvelib
Summary:	Resolve abstract dependencies into concrete ones
Summary(pl.UTF-8):	Rozwiązywanie abstrakcyjnych zależności w konkretne
Name:		python3-%{module}
Version:	1.2.1
Release:	1
License:	ISC
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/resolvelib/
Source0:	https://files.pythonhosted.org/packages/source/r/resolvelib/%{module}-%{version}.tar.gz
# Source0-md5:	6ae59a4cbb332ddc695ea608e3c01e34
URL:		https://github.com/sarugaku/resolvelib
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:62
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-packaging
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Resolvelib at the highest level provides a Resolver class that
includes dependency resolution logic. You give it some things, and a
little information on how it should interact with them, and it will
spit out a resolution result. It is used by pip and ansible-galaxy.

%description -l pl.UTF-8
Resolvelib na najwyższym poziomie udostępnia klasę Resolver,
zawierającą logikę rozwiązywania zależności. Jest używany przez pip i
ansible-galaxy.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
# test_pin_conflict_with_self needs "reporter" fixture from tests/conftest.py, not included in sdist
%{__python3} -m pytest tests \
	--deselect tests/test_resolvers.py::test_pin_conflict_with_self
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
