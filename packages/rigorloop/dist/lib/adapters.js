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
  opencode: {
    name: "opencode",
    displayName: "opencode",
    installRoots: {
      skills: ".opencode/skills",
      commands: ".opencode/commands",
    },
    directoryPlan: [".opencode", ".opencode/skills", ".opencode/commands"],
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
  const descriptor = ADAPTERS[name];
  return descriptor ? cloneDescriptor(descriptor) : undefined;
}

export function supportedAdapterNames() {
  return Object.keys(ADAPTERS);
}
