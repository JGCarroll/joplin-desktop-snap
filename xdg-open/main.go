package main

import (
	"github.com/godbus/dbus"
	"os"
	"os/exec"
	"syscall"
)

func openFile(path string, ask bool, writable bool) error {
	var fd int

	conn, err := dbus.SessionBus()
	if err != nil {
		return err
	}
	defer conn.Close()

	if writable {
		fd, err = syscall.Open(path, syscall.O_RDWR, 0)
	}
	if err != nil {
		writable = false
		fd, err = syscall.Open(path, syscall.O_RDONLY, 0)
	}
	if err != nil {
		return err
	}

	obj := conn.Object("org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop")

	var response interface{}
	err = obj.Call("org.freedesktop.portal.OpenURI.OpenFile",
		0,
		"",
		dbus.UnixFD(fd),
		map[string]dbus.Variant{"ask": dbus.MakeVariant(ask), "writable": dbus.MakeVariant(writable)},
	).Store(&response)
	return err
}

func main() {
	var ask bool
	var path string

	if len(os.Args) == 1 {
		panic("No arguments passed")
	}
	if len(os.Args) > 3 {
		panic("Too many arguments passed")
	}
	if len(os.Args) == 2 {
		path = os.Args[1]
	}
	if len(os.Args) == 3 && os.Args[2] == "--ask" {
		ask = true
		path = os.Args[1]
	}
	if len(os.Args) == 3 && os.Args[1] == "--ask" {
		ask = true
		path = os.Args[2]
	}

	if path == "" {
		panic("Filepath couldn't be parsed")
	}

	err := openFile(path, ask, true)
	if err != nil {
		err = openFile(path, ask, false)
	}

	// Call for backup, user probably wanted a URI instead or is lacking portal support and needs Userd
	if err != nil {
		err = exec.Command("snapctl", "user-open", path).Run()
	}
	if err != nil {
		panic(err)
	}
}
