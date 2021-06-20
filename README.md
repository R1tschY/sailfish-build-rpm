# sailfish-build-rpm

*Github Action for building RPMs for Sailfish OS*

This project uses mb2 in [dockerized](https://github.com/R1tschY/docker-sailfishos-sdk) [Sailfish OS Platfrom SDK](https://sailfishos.org/wiki/Platform_SDK) to build RPMs.

## Example

```yaml
- uses: R1tschY/sailfish-build-rpm@v1
  with:
    arch: "armv7hl"
    release: "4.1.0.24"
    fix-version: false
```
For a example project look at https://github.com/R1tschY/sailfish-sdk-action-test

## Usage
```yaml
- uses: R1tschY/sailfish-build-rpm@v1
  with:
    # Architecture to compile for (`armv7hl`, `i486` or `aarch64`).
    arch: ""

    # Version of Sailfish to compile for. For example, 4.1.0.24
    release: ""

    # Perform quality checks. (See `mb2 check --help` for more information)
    check: ""
    
    # Source directory using as working directory for mb2.
    # Default: checkout directory
    source-dir: ""
    
    # Basename of Docker image to use (name without tag).
    # Default: ghcr.io/r1tschy/sailfishos-platform-sdk
    image: ""
    
    # Enable debug build (passes --enabled-debug to mb2).
    # Default: false
    enable-debug: ""
    
    # Directory the resulting RPM artifacts are placed in.
    # Default: ./RPMS
    output-dir: ""
    
    # Path to `.spec` file to use for building RPM.
    # Default: Uses `.spec` file from `rpm` directory
    specfile: ""
    
    # Overwrite version from git information.
    # `true` or `false` are allowed.
    # (passes --fix-version to mb2)
    # Default: false
    fix-version: ""
```

## Example

```yaml
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    name: Build
    steps:
    - uses: actions/checkout@v2

    - id: build
      uses: R1tschY/sailfish-sdk-action@v1
      with:
        arch: 'armv7hl'
        release: '4.1.0.24'
        fix-version: false
        check: true

    - name: Upload build result
      uses: actions/upload-artifact@v2
      with:
        name: rpms
        path: RPMS
```
