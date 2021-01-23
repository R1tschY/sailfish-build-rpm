# sailfish-sdk-action

*Github Action for building RPMs for Sailfish*

## Example

```yaml
- uses: R1tschY/sailfish-sdk-action@v1
  with:
    arch: "armv7hl"
    release: "3.4.0.24"
    fix-version: false
```
For a example project look at https://github.com/R1tschY/sailfish-sdk-action-test

## Usage
```yaml
- uses: R1tschY/sailfish-sdk-action@v1
  with:
    # Architecture to compile for (armv7hl or i486).
    arch: ""

    # Version of Sailfish to compile for. For example, 3.4.0.24
    release: ""

    # Perform quality checks. (See `mb2 check` for more information)
    check: ""
    
    # Source directory.
    # Default: current working directory
    source-dir: ""
    
    # Basename of Docker image to use (name without tag)
    # Default: ghcr.io/r1tschy/sailfishos-platform-sdk
    image: ""
    
    # Enable debug build (passes --enabled-debug to mb2)
    enable-debug: ""
    
    # Directory the resulting RPM artifacts are placed in.
    # Default: ./RPMS
    output-dir: ""
    
    # Path to *.spec file
    specfile: ""
    
    # Overwrite version from git information (`true` or `false` are allowed)
    # (see `mb2 --fix-version` for more information)
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
        release: '3.4.0.24'
        fix-version: false
        check: true

    - name: Upload build result
      uses: actions/upload-artifact@v2
      with:
        name: rpms
        path: RPMS
```
