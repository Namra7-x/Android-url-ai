// Pando teaching simulator, source 3e44e8105248c7ff5df21db4060e7a42ce3427bd. See custom_components/PandoComparisonFigure/README.md.
import {
  ContributorComparison,
  importContributorWorker
} from "./contributor-comparison.js";
import {
  config
} from "./model.js";
const ctx = globalThis;
let comparison;
const loading = [];
// Run, seek and Results must use the same simulation. Reject an unsupported configuration here;
// silently substituting another scheduler would confound the effect of changing a setting.
ctx.onmessage = ({
  data: m
}) => {
  try {
    if (m.type === "loadModules" && !comparison) {
      while (loading.length < Math.min(3, m.count)) loading.push(importContributorWorker());
    } else if (m.type === "init") {
      const c = config(m.config);
      if (!ContributorComparison.supports(c)) throw Error("These settings are not supported by the contributor comparison.");
      const pause = m.pauseAtFinish ?? {
        enabled: false
      };
      if (comparison?.configureBeforeRun(c, m.experimentId, pause)) return;
      comparison?.cancel();
      comparison = new ContributorComparison(c, m.experimentId, (data, transfer) => ctx.postMessage(data, transfer ?? []), pause, () => loading.shift() ?? importContributorWorker());
      for (const worker of loading.splice(0)) worker.terminate();
    } else comparison?.handle(m);
  } catch (error) {
    comparison?.cancel();
    comparison = undefined;
    ctx.postMessage({
      type: "error",
      experimentId: m.experimentId,
      message: error instanceof Error ? error.message : String(error)
    });
  }
};