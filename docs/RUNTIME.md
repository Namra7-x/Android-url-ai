# Optional runtime URL observation

Runtime inspection can reveal destinations assembled from fragments or supplied by remote configuration. It cannot reveal every endpoint unless every relevant state and flow is exercised.

Use only a device, test account and app session you control. The included Frida agent records URL destinations passed to common Java URL/URI and OkHttp constructors. It does not collect headers, request bodies, prompts, cookies, passwords or response bodies.

Install Frida using https://frida.re/docs/installation/ and follow the official Android setup. A compatible Frida server/Gadget and device configuration may be required. Do not bypass authentication, certificate pinning or other access controls.

Example:

    frida -U -f com.google.android.apps.bard -l runtime/frida_url_observer.js

Replace the package with com.openai.chatgpt or com.anthropic.claude for the other apps. Manually exercise normal features and record which flows were tested. Native networking stacks or custom clients may not pass through the included Java hooks.

Treat runtime records as separate evidence and redact sensitive query values before committing reports.
