const ADAPTERS = {
  codex: {
    name: "codex",
    displayName: "Codex",
    installRoots: {
      skills: ".agents/skills",
    },
    directoryPlan: [".agents", ".agents/skills"],
  },
  claude: {
    name: "claude",
    displayName: "Claude Code",
    installRoots: {
      skills: ".claude/skills",
    },
    directoryPlan: [".claude", ".claude/skills"],
  },

};

function cloneDescriptor(descriptor) {
  return {
    ...descriptor,
    installRoots: { ...descriptor.installRoots },
    directoryPlan: [...descriptor.directoryPlan],
    archiveName(releaseTag) {
      return `rigorloop-adapter-${descriptor.name}-${releaseTag}.zip`;
    },
    primaryInstallRoot() {
      return descriptor.installRoots.skills;
    },
  };
}

export function adapterDescriptor(name) {
  const descriptor = Object.hasOwn(ADAPTERS, name) ? ADAPTERS[name] : undefined;
  return descriptor ? cloneDescriptor(descriptor) : undefined;
}

export function supportedAdapterNames() {
  return Object.keys(ADAPTERS);
}
