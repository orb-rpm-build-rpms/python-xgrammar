Name:           python-xgrammar
Version:        0.2.5^post1
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Efficient, Flexible and Portable Structured Generation

# No license information obtained, it's up to the packager to fill it in
License:        ...
URL:            https://xgrammar.mlc.ai/
Source:         %{pypi_source xgrammar 0.2.5.post1}

BuildRequires:  python3-devel
BuildRequires:  gcc


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'xgrammar' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-xgrammar
Summary:        %{summary}

%description -n python3-xgrammar %_description

# For official Fedora packages, review which extras should be actually packaged
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Extras
%pyproject_extras_subpkg -n python3-xgrammar metal,test


%prep
%autosetup -p1 -n xgrammar-0.2.5.post1


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x metal,test


%build
%pyproject_wheel


%install
%pyproject_install
# Automatically extracted from wheel
%pyproject_save_files xgrammar


%check
%pyproject_check_import


%files -n python3-xgrammar -f %{pyproject_files}


%changelog
%autochangelog
