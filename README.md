[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/joplin-desktop)

`sudo snap install joplin-desktop`

This repository contains the snapcraft build files that generate a snap build of Joplin desktop.

Joplins official site can be found at https://joplinapp.org/ and it's source repository at https://github.com/laurent22/joplin

# FAQ

## `joplin-james-carroll` -> `joplin-desktop` package migration

On 02/02/21, I published a new package `joplin-desktop`. This package is functionally identical to `joplin-james-carroll`.

I would like to deprecate `joplin-james-carroll`. I will continue to push updates to both package names until the users of `joplin-james-carroll` drops overtime.
Eventually, I will unpublish `joplin-james-carroll` entirely, preventing new downloads. There's no specific time frame involved, it'll be based on usage stats.

`joplin-james-carroll` will not appear in the search results of the Snap Store any longer, but can still be accessed by the package name directly. Still if you're reading this, please avoid installing it in the future.

If you wish to migrate to `joplin-desktop` sooner, make use of Joplins export functionality and synchronisation capabilities. Both packages can be installed by side side, although it may look confusing due to duplicated desktop entries, after the data is migrated simply run `sudo snap remove joplin-james-carroll`.
Keep in mind however that the packages are for the time being identical in every aspect but name, so don't feel the need to rush this process just yet.

Remember, snaps are isolated. *DO NOT SIMPLY INSTALL THE NEW PACKAGE AND DELETE THE OLD PACKAGE WITHOUT ENSURING YOU CAN MIGRATE THE DATA ACROSS*, otherwise you will have to make use of snapshots below to attempt to recover the data.

## How often does the snap get rebuilt?

A bot should check for and build the latest stable release every night. This release is automatically pushed to the candidate channel, since it has gone through substantial testing upstream and is simply being repackaged. Being pushed from candidate to stable usually takes hours to days to confirm it isn't a clearly defective package.

## I can't access files outside of $HOME
This is expected of snaps, they are heavily sandboxed and a snap usually cannot access files outside of $HOME. You can grant the removable-media interfaces to allow the snap to access `/mnt` and `/media`, which should allow it to access USB drives and other OS drives, provided they're under these paths.

`sudo snap connect joplin-desktop:removable-media :removable-media`

In the future, improvements in the Electron backend should facilitate accessing any filesystem without having to worry about permissions, by making use of XDG desktop portals.

## I can't print
This is expected of snaps, they are heavily sandboxed and printer access is not usually available by default. You can enable printer access with:

`sudo snap connect joplin-desktop:cups-control :cups-control`

`sudo snap connect joplin-desktop:avahi-control :avahi-control`

In the future, this permission may become obsolete by making use of XDG desktop portals.

## The snap cannot access data from a none snap install / Data is missing after removing the snap and I expected it to work with the AppImage
Snaps cannot access hidden folders/files in the top level of $HOME. This means this snap cannot access `$HOME/.config/joplin-desktop`, the default location of the Joplin databases.
The database is instead located in `$HOME/snap/joplin-desktop/current/.config/joplin-desktop`, and you should be able to copy this into `$HOME/.config/joplin-desktop` completely fine. You can also access this location by clicking "open profile directory" in the tools menu.

Alternatively, consider exporting the data or synchronising it instead.

If you have already deleted the snap and need to get the data, by default snaps are kept in a limbo state backed up for 31 days after being removed, so you can try to recover an automatic snapshot. Look [here](https://snapcraft.io/docs/snapshots) for help.

## External editors don't work as expected.
Snaps exist in a heavy sandbox and can't directly open other applications. The snap should attempt to use XDG desktop portals to find suitable editors instead, and requires XDG desktop portal support in order to do so. Ensure the support is set up on your host environment and the shortcut control-e should work mostly fine.

If your expected editor is not showing in the dialog, it's likely because it does not have metadata in the form of the freedesktop `.desktop` files, or it's metadata is incomplete, e.g, not being registered as a handler for the MIME type.

The functionality in the settings to specifiy an editor by file location will not work because the snap won't see any other editors due to the sandboxing.
As a special exception, the path `/usr/bin/joplin-open` can be used, which accepts an argument of ``--ask``. 
If this combination is used, the application selection prompt will unconditionally appear for external editors the next time you attempt to use the functionality and until the `--ask` argument is removed.
This can be used to reset the learnt preference or kept active indefinitely if preferred.

The snap should also be aware of when the system defaults are changed and open a prompt if a change is detected.
For example, if the default image viewer is changed, the snap should ask which image viewer to use the next time you attempt to open an image.

In the worst case scenario, you can run the following command and log out and in again to reset the preferences for all snaps and flatpaks.
`rm $HOME/.local/share/flatpak/db/desktop-used-apps`

For advanced users, if the `flatpak` command is available you manually set specific associations. e.g, to set gedit to be the default application for markdown in the Joplin snap:

`flatpak permission-set desktop-used-apps text/markdown snap.joplin-desktop org.gnome.gedit 0 3`

## ARM support
Joplin does not officially have ARM support and I don't have the hardware to test it in an ARM environment sufficiently, so this snap is currently X86_64 only.

## The application icon doesn't change with my icon theme

Unfortunately, due to limitations in the design of Snap, it isn't currently possible for individual Snap applications to support icon theming on some Linux distributions without completely breaking the application icon on others. Until this underlying issue is fixed, you can manually change individual application icons with [MenuLibre](https://github.com/bluesabre/menulibre) or something similar.
