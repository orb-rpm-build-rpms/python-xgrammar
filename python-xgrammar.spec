Name:           python-xgrammar
# Pinned to 0.2.1, vLLM's exact frozen pin (requirements/test/rocm.txt), which
# is validated against transformers 5.16.1. 0.2.5.post1 briefly capped
# transformers <5 (a regression not present in 0.2.1 or the later 0.2.6), which
# clashes with the transformers 5.16.1 the rest of the stack needs. 0.2.1's only
# transformers constraint is >=4.38.0 (the <4.50 cap is macOS test-only).
Version:        0.2.1
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Efficient, Flexible and Portable Structured Generation

# No license information obtained, it's up to the packager to fill it in
License:        ...
URL:            https://xgrammar.mlc.ai/
Source:         %{pypi_source xgrammar}

BuildRequires:  python3-devel
BuildRequires:  gcc


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'xgrammar' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-xgrammar
Summary:        %{summary}

%description -n python3-xgrammar %_description

# No extras are packaged: "metal" is macOS-only (mlx-lm) and "test" pulls
# huggingface-hub[cli] (an extra our huggingface-hub build does not provide) plus
# pytest tooling that the import-only %%check does not use. xgrammar's core deps
# (apache-tvm-ffi, torch, transformers, pydantic, triton, numpy) are enough.


%prep
%autosetup -p1 -n xgrammar-%{version}


%generate_buildrequires
%pyproject_buildrequires


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
