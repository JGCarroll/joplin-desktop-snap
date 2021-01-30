[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/joplin-james-carroll)

This repository contains the snapcraft build files that generate a snap build of Joplin. Precompiled binaries can be downloaded at https://snapcraft.io/joplin-james-carroll or via `sudo snap install joplin-james-carroll`

Joplins official site can be found at https://joplinapp.org/ and it's source repository at https://github.com/laurent22/joplin

# FAQ

## How often does the snap get rebuilt?

A bot should check for and build the latest stable release every night. This release is automatically pushed to the candidate channel, since it has gone through substantial testing upstream and is simply being repackaged. Being pushed from candidate to stable usually takes hours to days to confirm it isn't a clearly defective package.

## I can't access files outside of $HOME
This is expected of snaps, they are heavily sandboxed and a snap usually cannot access files outside of $HOME. You can grant the removable-media interfaces to allow the snap to access `/mnt` and `/media`, which should allow it to access USB drives and other OS drives, provided they're under these paths.

`sudo snap connect joplin-james-carroll:removable-media :removable-media`

In the future, improvements in the Electron backend should facilitate accessing any filesystem without having to worry about permissions, by making use of XDG desktop portals.

## I can't print
This is expected of snaps, they are heavily sandboxed and printer access is not usually available by default. You can enable printer access with:

`sudo snap connect joplin-james-carroll:cups-control :cups-control`

In the future, this permission may become obsolete by making use of XDG desktop portals.

## Fonts are showing as [][][] on certain (GTK) dialogues.
This is unfortunately a complex problem between font caches and container environments. Whilst improvements are constantly being made to alleviate this problem and most people don't experience it, for those who do there's little I can individually do to help other than to encourage you to refresh your systems font cache. The problem is not exclusive to this snap and is being tackled at an ecosystem level generally.

See [here](https://forum.snapcraft.io/t/snapped-app-not-loading-fonts-on-fedora-and-arch/12484) for some background

## The snap cannot access data from a none snap install / Data is missing after removing the snap and I expected it to work with the AppImage
Snaps cannot access hidden folders/files in the top level of $HOME. This means this snap cannot access `$HOME/.config/.joplin`, the default location of the Joplin databases.
The database is typically located in `$HOME/snap/joplin-james-carroll/current/.config/.joplin`, and you should be able to copy this into `$HOME/.config/.joplin` completely fine. You can also access this location by clicking "open profile directory" in the tools menu.

Alternatively, consider exporting the data or synchronising it instead.

If you have already deleted the snap and need to get the data, by default snaps are kept in a limbo state backed up for 31 days after being removed, so you can try to recover an automatic snapshot. Look [here](https://snapcraft.io/docs/snapshots) for help.

## External editors don't work as expected.
Snaps exist in a heavy sandbox and can't directly open other applications. The snap should attempt to use XDK desktop portals to find suitable editors instead, and requires XDG desktop portal support in order to do so. Ensure the support is set up on your host environment and the shortcut control-e should work mostly fine.

If your expected editor is not showing in the dialogue, it's likely because it does not have metadata in the form of the freedesktop .desktop files, or it's metadata is incomplete, E.G, not being registered as a handler for the MIME type. KDE fares better in this regard than GTK based desktops as it shows every app if requested.

The functionality in the settings to specificy an editor by file location will not work because the snap won't see any other editors due to the sandboxing.

Effectively this means external editors like Gedit, VSCode, Gimp, Pinta, etc, are likely to be fine; but CLI based such as Vim may not be possible without effort on the users side to create a .desktop file manually for it.

## ARM support
Joplin does not officially have ARM support and I don't have the hardware to test it in an ARM environment sufficiently, so this snap is currently X84_64 only.

## The Application icon doesn't change with my icon theme

If you are using an icon theme such as [`mint-y-icons`](https://github.com/linuxmint/mint-y-icons/) (e.g. on Linux Mint with the Cinnamon shell), in order for the shell to be able to replace the application icon, the `.desktop` file must use a "symbolic" reference for the icon name. Unfortunately, while `snapd` 2.42 and later do support symbolic icon names, distributions such as Debian and Solus still ship with older versions of `snapd`, so in order to maintain support for these users, the default `.desktop` for `joplin-snap` must still use an absolute path for the icon name, which precludes icon theming.

As a workaround, you can create your own local `.desktop` file at `~/.local/share/applications$ nano joplin-james-carroll_joplin.desktop`:
```
$ nano ~/.local/share/applications$ nano joplin-james-carroll_joplin.desktop
```
Then paste the following and save:
```
[Desktop Entry]
X-SnapInstanceName=joplin-james-carroll
Name=Joplin
Comment=The free and private note taking app
Exec=env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/joplin-james-carroll_joplin.desktop /snap/bin/joplin-james-carroll.joplin
Icon=joplin
Type=Application
Categories=Office;
StartupWMClass=Joplin
Terminal=false
```
Note this will by default break the included Joplin icon, and Joplin will use a generic application icon if you are not using an icon theme that includes an icon for Joplin.

To revert to the default application icon, delete the workaround as follows:
```
$ rm ~/.local/share/applications/joplin-james-carroll_joplin.desktop
```
