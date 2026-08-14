import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("exports a complete portfolio page", async () => {
  const html = await readFile(new URL("dist/client/index.html", root), "utf8");

  assert.match(html, /Nandini Mehta/);
  assert.match(html, /Software Engineer/);
  assert.match(html, /Based in Germany/);
  assert.match(html, /Document Classification/);
  assert.match(html, /RAG-Based LLM Application/);
  assert.match(html, /Manufacturing Knowledge Graph/);
  assert.match(html, /Agentic AI Assistant/);
  assert.match(html, /ClaimVision AI/);
  assert.match(html, /Vehicle Fault &amp; Emission Anomaly Detection/);
  assert.match(html, /Languages \/ Technologies/);
  assert.doesNotMatch(html, /Six projects/);
  assert.match(html, /canvas/);
  assert.match(html, /og\.png/);
  assert.doesNotMatch(html, /Engineering data into systems that/);
  assert.doesNotMatch(html, /Chemnitz|Work Experience|ChargeHorizons/);
  assert.doesNotMatch(html, /Have a complex problem|Let's map it out|OPEN CHANNEL/);
  assert.doesNotMatch(html, /scene-dots|Project roadmap stations/);
  assert.match(html, /LinkedIn/);
  assert.match(html, /href="tel:\+4917634668019"/);
  assert.match(html, /href="mailto:nandimehta2204@gmail\.com"/);
  assert.match(html, /Send inquiry/);
  assert.doesNotMatch(html, /formsubmit\.co/);
  assert.match(html, /name="first_name"/);
  assert.match(html, /name="last_name"/);
  assert.match(html, /type="email"[^>]+name="email"/);
  assert.match(html, /name="message"/);
  assert.match(html, /Return to origin/);
  assert.doesNotMatch(html, /Nandini_Mehta_CV|Download CV|Full CV/);
  assert.doesNotMatch(html, /codex-preview|SkeletonPreview|react-loading-skeleton/);
});

test("connects the inquiry form to EmailJS", async () => {
  const source = await readFile(new URL("app/InquiryForm.tsx", root), "utf8");

  assert.match(source, /api\.emailjs\.com\/api\/v1\.0\/email\/send/);
  assert.match(source, /service_t2csn5s/);
  assert.match(source, /template_39i6qtd/);
  assert.match(source, /Your inquiry was sent successfully/);
  assert.doesNotMatch(source, /formsubmit\.co/);
});

test("ships portfolio assets and the GitHub Pages workflow", async () => {
  await Promise.all([
    access(new URL("dist/client/og.png", root)),
    access(new URL("dist/client/projects/document-ai/01-dashboard.png", root)),
    access(new URL("dist/client/projects/claimvision-ai/01-dashboard.png", root)),
    access(new URL("dist/client/projects/vehicle-anomaly/01-dashboard-healthy.png", root)),
    access(new URL(".github/workflows/deploy-pages.yml", root)),
  ]);
});
