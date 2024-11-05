[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/joplin-desktop)

```bash
sudo snap install joplin-desktop
```

This repository contains the snapcraft build files that generate a snap build of Joplin desktop.

Joplins official site can be found [here](https://joplinapp.org/) and its source repository [here](https://github.com/laurent22/joplin)

# FAQ

## I can't access files outside of $HOME
This is expected of snaps, they are heavily sandboxed and a snap usually cannot access files outside of $HOME. 
You can grant the removable-media interfaces to allow the snap to access `/mnt` and `/media`.

```bash
sudo snap connect joplin-desktop:removable-media
```

If the `xdg-desktop-portals` package is installed, GUI filepickers will be able to access arbitrary files on the system.
(Folder selection via the xdg-portals requires Ubuntu 21.04+, Debian 11, etc).

## The snap cannot access data from a none snap installation
Snaps cannot access hidden folders/files in the top level of `$HOME`. 
This means this snap cannot access `$HOME/.config/joplin-desktop`, the default location of the Joplin databases.
The database is instead located in `$HOME/snap/joplin-desktop/current/.config/joplin-desktop`, and you should be able to copy this into `$HOME/.config/joplin-desktop`.
You can also access this location by clicking "open profile directory" in the tools menu.

Alternatively, consider exporting the data (e.g., via `.jex`) or using Joplin's built in synchronisation functionality.

## Data is missing after removing the snap
Snaps follow mobile app conventions and clear up their application specific data on uninstallation.
If you have already deleted the snap and need to recover the data, the data will be stored for up to a month by default.
Look [here](https://snapcraft.io/docs/snapshots) for help.

## External editors don't work as expected.
Snaps exist in a heavy sandbox and can't directly open other applications. 
The snap should attempt to use XDG desktop portals to find suitable editors instead, and requires XDG desktop portal support in order to do so.
Ensure the support is set up on your host  (e.g, installing an `xdg-desktop-portal` system package) and the shortcut control-e should work mostly fine.

If your expected editor is not showing in the dialog, it's likely because it does not have metadata in the form of the freedesktop `.desktop` files, or it's metadata is incomplete, e.g, not being registered as a handler for the MIME type.

The functionality in the settings to specifiy an editor by file location will not work because the snap won't see any other editors due to the sandboxing.
As a special exception, the path `xdg-open` can be used, which accepts an argument of ``--ask``. 
If this combination is used, the application selection prompt will unconditionally appear for external editors the next time you attempt to use the functionality and until the `--ask` argument is removed.
This can be used to reset the learnt preference or kept active indefinitely if preferred.

The snap should also be aware of when the system defaults are changed and open a prompt if a change is detected.
For example, if the default image viewer is changed, the snap should ask which image viewer to use the next time you attempt to open an image.

In the worst case scenario, you can run the following command and log out and in again to reset the preferences for all snaps and flatpaks.

```bash
rm $HOME/.local/share/flatpak/db/desktop-used-apps
```

For advanced users, if the `flatpak` command is available you manually set specific associations.
e.g, to set Gedit to be the default application for markdown in the Joplin snap:

```bash
flatpak permission-set desktop-used-apps text/markdown snap.joplin-desktop org.gnome.gedit 0 3
```
