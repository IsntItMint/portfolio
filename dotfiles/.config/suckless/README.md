# install

clone these git repositories

    git clone https://git.suckless.org/dwm
    git clone https://git.suckless.org/dmenu
    git clone https://git.suckless.org/st
    git clone https://git.suckless.org/scroll
    git clone https://git.suckless.org/slock
    git clone https://git.suckless.org/slstatus

and make

    sudo make install

# patch
first, switch to mypatch branch, _DO NOT MODIFY ON master BRANCH_

    git switch mypatch

patches are in patch/ directory

    git apply [.diff file]

if error occured use either of these commands

    git apply -3 [.diff file]
    patch -p1 < [.diff file]

to make a patch

    git diff master > toolname-patchname-YYYYMMDD-SHORTHASH.diff
