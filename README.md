# tzim

Convert Tomboy / Gnote notes to zim notes

## Usage

In an empty target directory, execute following while typing RETURN-key at each
prompt.

```
 $ prthon3 /path/to/tzim.py
```

If you need non-default behavior, enter pertinent path to the prompt.

This converts Tomboy / Gnote notes under a single target directory.

You can import each page to `zim` one by one via `File` -> `Import page...`.

Also you can move this target directory content to some path where you keep
`zim` data using `cp` or `mc` commands.  Then restart `zim` and you are all
set.


## License

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Copyright

  * Copyright 2007,2008 Bengt J. Olsson
  * Copyright 2020      Osamu Aoki

## Repository

This python3 code is hosted at: https://github.com/osamuaoki/tzim


## Changes

* Rev:      1.2.1-oa01
  * Date:     2020-06-13  (OA)
  * Changes:  Updated to python3 and adjust default behavior to modern path choices
    (original from https://github.com/jaap-karssenberg/zim-wiki/wiki/Tomboy-import-script)
    (original upstream URL http://blafs.com/diverse.html was unreachable)
* Rev:      1.2.1
  * Date:     2008-03-25
  * Changes:  Corrected typo in dialog. Translates tomboy's monospace to zim verbatim
* Rev:      1.2
  * Date:     2008-03-24
  * Changes:  Much revised code. Should be more robust against Tomboy note format now. Also added
          support for the new "Notebooks" concept (i.e. two-level name-spaces)
* Rev:      1.1
  * Date:     2008-03-08
  * Changes:  Fixed an issue when Create date on tomboy note does not exist. Now displays both
          "Last changed" and "Create date" (if these exists) and conversion date. Fixed
          various issues with that could hang the script. Added a few character subs.
* Rev:      1.0
  * Date:     2007-07-28
  * Changes:  First version
