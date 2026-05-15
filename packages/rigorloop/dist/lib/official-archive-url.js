const OFFICIAL_HOST = "github.com";
const OFFICIAL_OWNER = "xiongxianfei";
const OFFICIAL_REPO = "rigorloop";

export function expectedArchiveUrl({ releaseTag, archive }) {
  return `https://${OFFICIAL_HOST}/${OFFICIAL_OWNER}/${OFFICIAL_REPO}/releases/download/${releaseTag}/${archive}`;
}

export function validateOfficialArchiveUrl({ url, releaseTag, archive }) {
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    return {
      ok: false,
      code: "invalid-archive-url",
      message: "Adapter archive URL is not a valid URL.",
    };
  }

  const expected = new URL(expectedArchiveUrl({ releaseTag, archive }));
  const isOfficial =
    parsed.protocol === "https:" &&
    parsed.hostname === expected.hostname &&
    parsed.pathname === expected.pathname &&
    parsed.search === "" &&
    parsed.hash === "" &&
    parsed.username === "" &&
    parsed.password === "" &&
    parsed.port === "";

  if (!isOfficial) {
    return {
      ok: false,
      code: "non-official-archive-url",
      message: "Network adapter install may fetch only official RigorLoop GitHub release archive URLs.",
      path: "metadata.artifacts[codex].url",
    };
  }

  return { ok: true };
}
