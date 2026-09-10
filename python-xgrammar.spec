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

# xgrammar loads its compiled extension libxgrammar_bindings.so through
# tvm_ffi.load_lib_module("xgrammar", ...), which locates the .so by reading the
# dist-info RECORD manifest (importlib.metadata) and resolving the listed path
# under site-packages -- there is no other discovery path for a bundled library
# in a *consumer* package (tvm_ffi's fallback only searches its own package
# directory). Fedora's brp-python-rpm-in-distinfo normally deletes RECORD (RPM
# owns file tracking), which would make xgrammar unimportable at run time, not
# just in %%check. Disable that one BRP so RECORD survives; the file is packaged
# explicitly below. (Its side effect of rewriting INSTALLER pip->rpm is cosmetic
# and irrelevant to a localrepo build.)
%global __brp_python_rpm_in_distinfo %{nil}


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
# xgrammar compiles its C++ core with -Werror. GCC 16 emits a false-positive
# -Warray-bounds in cpp/compiled_grammar.cc (deep in the std::optional path of
# LogFatalError, reached only when NDEBUG/-O2 inlines libstdc++'s basic_string),
# which -Werror turns fatal. The redhat build flags are placed after xgrammar's
# own flags on the compiler command line, so appending -Wno-error=array-bounds
# to CXXFLAGS demotes just that one diagnostic back to a warning; every other
# warning is still an error. Upstream tested against an older GCC that did not
# raise it.
CXXFLAGS="${CXXFLAGS} -Wno-error=array-bounds"
export CXXFLAGS
%pyproject_wheel


%install
%pyproject_install
# Automatically extracted from wheel
%pyproject_save_files xgrammar


%check
%pyproject_check_import


%files -n python3-xgrammar -f %{pyproject_files}
# RECORD is normally stripped by brp-python-rpm-in-distinfo (disabled above);
# tvm_ffi reads it at import time to locate libxgrammar_bindings.so, so keep it.
%{python3_sitearch}/xgrammar-%{version}.dist-info/RECORD


%changelog
%autochangelog
