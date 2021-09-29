from snapcraft.plugins.v2 import PluginV2
from typing import Any, Dict, List, Set


class PluginImpl(PluginV2):

	@classmethod
	def get_schema(cls) -> Dict[str, Any]:
		return {
			"$schema": "http://json-schema.org/draft-04/schema#",
			"type": "object",
			"additionalProperties": False,
		}

	def get_build_snaps(self) -> Set[str]:
		return {"node/16/stable"}

	def get_build_packages(self) -> Set[str]:
		return {"python", "rsync", "libsecret-1-dev", "curl"}

	def get_build_environment(self) -> Dict[str, str]:
		return dict(
			npm_config_unsafe_perm="true",
			SUDO_UID="0",
			SUDO_GID="0",
			SUDO_USER="root",
			npm_config_prefer_offline="true"
		)


	@staticmethod
	def _launchpad_proxy_workaround() -> List[str]:
		return [
			# ${var-} to work around potential unbound variable.
			'if [[ -n "${http_proxy-}" ]]; then',
				'export ELECTRON_GET_USE_PROXY=1',
				'export GLOBAL_AGENT_HTTP_PROXY="${http_proxy}"',
				'export GLOBAL_AGENT_HTTPS_PROXY="${http_proxy}"',
			'fi'
		]

	@staticmethod
	def _apply_patches() -> List[str]:
		return [
			"patch -i $SNAPCRAFT_PROJECT_DIR/snap/local/patches/disable_updates.patch -p 1",
			"patch -i $SNAPCRAFT_PROJECT_DIR/snap/local/patches/hide_dev_command.patch -p 1",
			"patch -i $SNAPCRAFT_PROJECT_DIR/snap/local/patches/detect_updates.patch -p 1",
			"patch -i $SNAPCRAFT_PROJECT_DIR/snap/local/patches/force_custom_xdg-open.patch -p 1"
		]

	@staticmethod
	def _build_commands() -> List[str]:
		return [
			"unset PYTHONPATH",
			"npm cache verify",
			"npm install",
			"cd packages/app-desktop",
			"node_modules/.bin/electron-rebuild",
			"node_modules/.bin/electron-builder",
			"mkdir ${SNAPCRAFT_PART_INSTALL}/opt -p",
			"cp -r dist/*unpacked ${SNAPCRAFT_PART_INSTALL}/opt/joplin-desktop",
			"mv ${SNAPCRAFT_PART_INSTALL}/opt/joplin-desktop/@joplinapp-desktop ${SNAPCRAFT_PART_INSTALL}/opt/joplin-desktop/joplin"
		]

	def get_build_commands(self) -> List[str]:
		return self._launchpad_proxy_workaround() + self._apply_patches() + self._build_commands()
